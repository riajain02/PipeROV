#!/usr/bin/env python3

import select
import socket
import sys
import queue
from mygps import mygps_get_coordinates
from mycompass import mycompass_get_heading

####################
# swarm tasks
#
tasks = []
tasks.append (('turn',0.0))       # task 3
tasks.append (('drive',1,2.0))    # task 2
tasks.append (('turn',90.0))     # task 1
tasks.append (('drive',1,2.0))    # task 2
tasks.append (('turn',180.0))     # task 1
tasks.append (('drive',1,2.0))    # task 2
tasks.append (('turn',270.0))       # task 3
tasks.append (('drive',1,2.0))    # task 2
tasks.reverse()
####################

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('192.168.0.41', 10005)
print ('starting up on %s port %s' % (server_address), file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [ server ]

# Sockets to which we expect to write
outputs = [ ]

# Outgoing message queues (socket:queue)
message_queues = {}



#The main portion of the server program loops, calling select() to block and wait for network activity.

task_done = {}
task_get_next = True

while inputs:

    if task_get_next == True : 
       if len(tasks) > 0 :
          task = tasks.pop()
          print ("\n**** New task:" , task, "\n")
       else :
          task = ('stop')
       task_get_next = False
       for key in task_done :
          task_done[key] = False

    #
    # Wait for at least one of the sockets to be ready for processing
    #
    print ('\nwaiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    #
    # Handle inputs
    #
    for s in readable:

        if s is server:
            connection, client_address = s.accept()
            print ('new connection from %s %s' % (client_address), file=sys.stderr)
            connection.setblocking(0)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = queue.Queue()
            task_done[connection] = False

        else:
            data = s.recv(1024)
            if data:

                # A readable client socket has data
                print ('received "%s" from %s' % (data, s.getpeername()), file=sys.stderr)

                #
                # decode message and send instruction for this ROV
                #
                #   decode
                data2  = data.decode()
                data3  = data2.split()
                status = data3[0]
                lat    = float(data3[1])
                long   = float(data3[2])
                dir    = float(data3[3])

                if status == 'done' :
                   task_done[s] = True

                   # till next task tell this ROV to remain still
                   mesg1 = "wait"
                   mesg2 = str.encode(mesg1)
                   message_queues[s].put(mesg2)
                   # Add output channel for response
                   if s not in outputs:
                       outputs.append(s)

                else :
                   #
                   # prepare instructions to orient
                   #
                   if task[0] == 'turn':
                      targetdir = task[1]

                      diraccuracy = 2.0
                      maxduration = 0.5
                      minduration = 0.05
                      maxdir = 90.0
                      mindir = 10.0

                      #
                      # set turn direction (left or right) 
                      #
                      magdirR = targetdir - dir
                      if magdirR < 0: magdirR += 360

                      magdirL = dir - targetdir
                      if magdirL < 0: magdirL += 360

                      magdir = magdirR
                      turndir = 1
                      if magdirL < magdirR :
                         magdir = magdirL
                         turndir = -1

                      if magdir < diraccuracy:
                         turndir = 0
                         mesg1 = "stop"
                      else :
                         #
                         # set turn duration 
                         #
                         duration = 0.0
                         if magdir > maxdir:
                           duration = maxduration
                         elif magdir < mindir:
                           duration = minduration
                         else:
                           duration = minduration + (magdir-mindir)/(maxdir-mindir) * (maxduration - minduration)

                         mesg1 = "turn %d %f "%(turndir,duration)

                      mesg2 = str.encode(mesg1)
                      message_queues[s].put(mesg2)
                      # Add output channel for response
                      if s not in outputs:
                          outputs.append(s)

                   elif task[0] == 'drive':
                      drivedir = task[1]
                      duration = task[2]
                      mesg1 = "drive %d %f "%(drivedir,duration)
                      mesg2 = str.encode(mesg1)
                      message_queues[s].put(mesg2)
                      # Add output channel for response
                      if s not in outputs:
                          outputs.append(s)

                   elif task[0] == 'stop':
                      mesg1 = "stop"
                      mesg2 = str.encode(mesg1)
                      message_queues[s].put(mesg2)
                      # Add output channel for response
                      if s not in outputs:
                          outputs.append(s)


            else:

                # Interpret empty result as closed connection
                print ('closing', client_address, 'after reading no data', file=sys.stderr)

                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]

    #
    # Handle outputs
    #
    for s in writable:
        try:

            next_msg = message_queues[s].get_nowait()

        except queue.Empty:

            # No messages waiting so stop checking for writability.
            print ('output queue for', s.getpeername(), 'is empty', file=sys.stderr)
            outputs.remove(s)

        else:

            print ('sending "%s" to %s' % (next_msg, s.getpeername()), file=sys.stderr)
            s.send(next_msg)

    #
    # Handle "exceptional conditions"
    #
    for s in exceptional:
        print ('handling exceptional condition for', s.getpeername(), file=sys.srderr)

        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]

    # check if all ROV's are done
    all_done = True
    for key in task_done :
        if task_done[key] == False: all_done = False
    if all_done == True : task_get_next = True

