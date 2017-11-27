import argparse
import socket
import sys
import threading
import hashlib

parser = argparse.ArgumentParser(usage='./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>',
                                 description='DHT Peer Application',add_help=False)
parser._add_action(argparse._HelpAction(
    option_strings=['-H', '--help'],
    help='Gives you the help documentation and details about optional arguments'
))
parser.add_argument('-m','--peertype', type = int, help='Specify 1 if the peer is root and 0 otherwise')
parser.add_argument('-p','--own_port', type = int, help='Specify the port for the peer')
parser.add_argument('-h','--own_hostname',help='Specify the hostname of the peer')
parser.add_argument('-r','--root_port', type = int, help='Specify the port of the root')
parser.add_argument('-R','--root_hostname',help='Specify the hostname of the root')
args = parser.parse_args()

# Default is normal peer if the type is not specified.
if args.peertype is None:
    args.peertype = 0

peertype = args.peertype
ownport = args.own_port
ownhost = args.own_hostname
rootport = args.root_port
roothost = args.root_hostname

class node:
	def __init__(self,phname,phport,shname,shport):
		self.pn = phname
		self.pp = phport
		self.sn = shname
		self.sp = shport
def printchord(nn):
	print nn.pn,":", nn.pp, "--- me--->", nn.sn,":", nn.sp

def rootjoin(indata, nodeval, conn):
	# 1. Update the predecessor of the current successor
	sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket Created for updating the predecessor of current successor'
	remote_ip = socket.gethostbyname( nodeval.sn )
	print 'Ip address of current successor %s is %s' %(nodeval.sn, remote_ip)
	#Connect to current successor of root
	sock2.connect((remote_ip , int(nodeval.sp)))
	print 'Socket Connected to %s on port %d'  %(nodeval.sn,int(nodeval.sp))
	#Sending the UPDATE request"
	predupdata = "UPDATE|PRED|"+ indata[1]+"|"+indata[2]
	#Send the whole string
	sock2.sendall(predupdata)
	print 'Message sent successfully \n %s to %s on %d'  %(predupdata,nodeval.sn,int(nodeval.sp))
	# 2. Update the successor of the joining node
	sucupdate = "UPDATE|SUCC|"+nodeval.sn+"|"+str(nodeval.sp)
	conn.sendall(sucupdate)
	# 3. Update the successor of the root node 
	nodeval.sn = indata[1]
	nodeval.sp = indata[2]
	printchord(nodeval)
	conn.close()

def predup(indata,nodeval,conn):
	# Handling predecessor update requests
	nodeval.pn = indata[2]
	nodeval.pp = indata[3]
	printchord(nodeval)
	conn.close()

def succup(indata,nodeval,conn):
	# Handling predecessor update requests
	nodeval.sn = indata[2]
	nodeval.sp = indata[3]
	printchord(nodeval)
	conn.close()

def nodejoin(rh,rp,oh,op):
	# Sending JOIN request to root node
	sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket Created for updating the predecessor of current successor'
	rootip = socket.gethostbyname( roothost )
	print 'Ip address of root %s is %s' %(roothost, rootip)
	sock3.connect((rootip , rootport))
	print 'Socket Connected to %s on port %d'  %(roothost,rootport)
	joindata = "JOIN|"+ ownhost +"|"+ str(ownport)
	#Send the whole string
	sock3.sendall(joindata)
	print 'Message sent successfully \n %s to %s on %d'  %(joindata,roothost,rootport)



# If m = 1, the node initiated is considered as the root node. 
if peertype == 1:
	# Initiating root node
	rootnode = node(ownhost, ownport, ownhost, ownport)
	printchord(rootnode)
	# Creating a socket for root node
	try:
		nsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
		sys.exit();
	print "Socket created for root node!"

	#Binding the socket to specified ports
	try:
		nsock.bind((ownhost, ownport))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Socket bind complete'

	# Listening for incoming requests
	nsock.listen(10)
	print 'Socket now listening'

	while 1:
		conn, addr = nsock.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

		# Handling the incoming requests received
		req = conn.recv(1024)
		reqpro = req.split('|')
		if not req:
			break
		# If the request is a join request
		elif reqpro[0] == "JOIN":
			rootjoin(reqpro,rootnode,conn)
		elif (reqpro[0] == 'UPDATE') and (reqpro[1] == 'PRED'):
			predup(reqpro,rootnode,conn)
		else:
			print "invalid request type"
			sys.exit()
	conn.close()
	nsock.close()
elif peertype == 0:
	#Initiate a normal node with predecessor as root and successor as empty
	normalnode = node(roothost, rootport, '', 0)
	print "Current state of CHORD on the node %s:%d" %(ownhost,ownport)	
	printchord(normalnode)
	# Creating a socket for normal node
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
		sys.exit();
	print "Socket created for root node!"

	#Binding the socket to specified ports
	try:
		sock.bind((ownhost, ownport))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Socket bind complete'

	# Sending JOIN request to root node
	nodejoin(roothost,rootport,ownhost,ownport)

	# Listening for incoming requests
	sock.listen(10)
	print 'Socket now listening'
	while 1:
		conn, addr = sock.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

		# Handling the incoming requests received
		nreq = conn.recv(1024)
		nreqpro = nreq.split('|')
		if not nreq:
			break
		# If the request is a join request
		elif (nreqpro[0] == 'UPDATE') and (nreqpro[1] == 'SUCC'):
			succup(nreqpro,normalnode,conn)
		elif (nreqpro[0] == 'UPDATE') and (nreqpro[1] == 'PRED'):
			predup(nreqpro,normalnode,conn)
		else:
			print "invalid request type"
			sys.exit()
	conn.close()
	nsock.close()

else:
	print "Invalid peertype"
	sys.exit()



	
