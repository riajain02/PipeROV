#!/usr/bin/env python3

#The example client program uses two sockets to demonstrate how the server with select() manages multiple connections at the same time. The client starts by connecting each TCP/IP socket to the server.

import socket
import sys
from time import sleep
from mycar import mycar_drive, mycar_turn, mycar_stop
from mygps import mygps_get_coordinates
from mycompass import mycompass_get_heading

server_address = ('192.168.0.38', 10005)

# Create a TCP/IP socket
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          ]

# Connect the socket to the port where the server is listening
print ('connecting to %s port %s' % (server_address), file=sys.stderr)
for s in socks:
    s.connect(server_address)

   
task_done = False

while True:

   sleep (.25)

   #
   #  send ready signal with latitude, longitude, direction
   #
   lat, long = mygps_get_coordinates() # in deg
   dir = mycompass_get_heading()       # in deg
   if task_done:
      mesg1 = "done %s %s %s"%(lat,long,dir)
      task_done = False
   else :
      mesg1 = "ready %s %s %s"%(lat,long,dir)
   messages = [ str.encode(mesg1) ]

   for message in messages:
   
       # Send messages on sockets
       for s in socks:
          # print ('%s: sending "%s"' % (s.getsockname(), message), file=sys.stderr)
           s.send(message)

   #
   #  receive the signal to drive, turn, stop and its duration
   #
   # Read responses on sockets
   for s in socks:
       data = s.recv(1024)
       #print ('%s: received "%s"' % (s.getsockname(), data), file=sys.stderr)
       
       #
       # decode message and send instruction for this ROV
       #
       #   decode
       data2  = data.decode()
       data3  = data2.split()
       action = data3[0]

       if action == 'turn' :
          task_done = False
          turndir   = float(data3[1])
          duration  = float(data3[2])
          if turndir != 0 and duration > 0:
             mycar_turn(turndir)
             sleep (duration)
             mycar_stop()

       elif action == 'drive':
          task_done = False
          drivedir   = float(data3[1])
          duration  = float(data3[2])
          mycar_drive(drivedir)
          sleep (duration)
          task_done = True
          mycar_stop()

       elif action == 'stop':
          task_done = True
          mycar_stop()

       else :
          print ("waiting")

       if not data:
          print ('closing socket %s' % (s.getsockname()), file=sys.stderr)
          s.close()
