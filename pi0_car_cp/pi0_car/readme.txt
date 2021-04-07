1) run webserver and connect to it
   
   python3 main.py to start the webserver

   connect to the server at 192.168.0.xx:5000

2) run socket server on the mother station

   python3 main_socket_server
   (edit IP address)

   the header in this file contains the list of tasks for the swarm

3) run socket client on the ROV

   python3 main_socket_client
   (edit IP address)
