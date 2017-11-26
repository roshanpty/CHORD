import argparse
import socket
import sys
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
	print nn.pn,":", nn.pp, "--- me--->", nn.sn, nn.sp

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
	conn, addr = nsock.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	# Handling the incoming requests received
	req = conn.recv(1024)
	reqpro = req.split('|')
	# If the request is a join request
	if reqpro[0] == "JOIN":
		# 1. Update the predecessor of the current successor
		try:
			sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
    			print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    			sys.exit();

		print '\________________________\nSocket Created for updating the predecessor of current successor\n'
		try:
			remote_ip = socket.gethostbyname( rootnode.sn )
		except socket.gaierror:
    			#could not resolve
    			print 'Hostname could not be resolved. Exiting'
    			sys.exit()
		print 'Ip address of current successor %s is %s' %(rootnode.sn, remote_ip)
		#Connect to current successor of root
		sock2.connect((remote_ip , rootnode.sp))
		print 'Socket Connected to %s on port %d'  %(rootnode.sn, rootnode.sp)
		#Sending the UPDATE request"
		predupdata = "UPDATE|PRED|"+ reqpro[1]+"|"+reqpro[2]
		try :
		#Set the whole string
			sock2.sendall(predupdata)
		except socket.error:
    		#Send failed
			print 'Send failed'
			sys.exit()
		print 'Message send successfully \n %s to %s on %d'  %(predupdata,rootnode.sn,rootnode.sp)
		# 2. Update the successor of the joining node
		sucupdate = "UPDATE|SUCC|"+rootnode.sn+"|"+str(rootnode.sp)
		conn.sendall(sucupdate)
		# 3. Update the successor of the root node 
		rootnode.sn = reqpro[1]
		rootnode.sp = reqpro[2]

		printchord(rootnode)
		conn.close()

