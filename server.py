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
	print(client._socket)
	client.send('ls')
	client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Binding on [{}]:{}...".format(socket.gethostname(), port))
server.bind((socket.gethostname(), port))
server.listen(5)

while True:
	# Accept a new client
	(client_socket, address) = server.accept()
	c = client(client_socket, address)
	clients.append(c)

	# Create a new thread to handle this new client
	threading.Thread(target=handle_client, args=[c]).start()
