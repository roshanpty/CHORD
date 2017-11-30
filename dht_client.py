import argparse
import socket
import sys
import threading
import hashlib
import os

class client:
	def __init__(self,cname, cport, rname, rport):
		self.cn = cname
		self.cp = cport
		self.rn = rname
		self.rp = rport
		

	def listensocket(self):
		global sock		
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
			print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
			sys.exit();
		try:
			sock.bind((self.cn, self.cp))
		except socket.error , msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		sock.listen(10)
		print "Client is listening..."
		
		while 1:
			conn, addr = sock_root.accept()
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			req = conn.recv(1024)	
			reqpro = req.split('|')
			if not req:
				break	
			elif (reqpro[0] == "STORE") and (reqpro[0] == "RESP")
				# Send STORE OBJ request to the node
			elif reqpro[0] == "REC"
				#Display  and store the object returned
				objectname = reqpro[5]
				objectvalue = reqpro[6]
				objfile = open(objectname,'x')
				objfile.write(objectvalue)
				objfile.close
			elif reqpro[0] == "ITER"
				if reqpro[1] == "YES"
					#Display  and store the object returned
					objectname = reqpro[6]
					objectvalue = reqpro[7]
					objfile = open(objectname,'x')
					objfile.write(objectvalue)
					objfile.close
				elif reqpro[1] == "NO"
					#Send the query to successor node
					key = reqpro[1]
					nextnode = reqpro[2]
					nextport = int(reqpro[3])
					iter_req = "RETREIVE|ITER|"+key+"|"+dclient.cn+"|"+str(dclient.cp)
					rootlookup(nextnode,nextport,iter_req)
def menuopt(node):		
	while 1:
		menu_opt = raw_input("DHT Client Menu:\n \
		Enter the letter corresponding to the operation you are performing\n \
		1. Store an object - s\n \
		2. Retrieve an object in iterative fashion - i\n \
		3. Retrieve an object in recursive fashion - r\n \
		4. Exit the DHT Client program - e\n ")

		if menu_opt == "s":
			print "Entering object store operation"
			filepath = raw_input("Enter the full path of file you want to store:\nExample: /home/user/filename.txt\n")
			filename = os.path.basename(filepath)
			key = hashlib.sha1(filename).hexdigest()
			store_lookup = "STORE|POS|"+key+"|"+dclient.cn+"|"+str(dclient.cp)
			rootlookup(dclient.rn,dclient.rp,store_lookup)
		elif menu_opt == "i":
			print "Entering iterative retreival of object"
			keyval = raw_input("Enter the key value of the object to be retreived.")
			iter_lookup = "RETREIVE|ITER|"+keyval+"|"+dclient.cn+"|"+str(dclient.cp)
			rootlookup(dclient.rn,dclient.rp,iter_lookup)
		elif menu_opt == "r":
			print "Performing recursive retreival of object"
			keyval = raw_input("Enter the key value of the object to be retreived.")
			rec_lookup = "RETREIVE|REC|"+keyval+"|"+dclient.cn+"|"+str(dclient.cp)
			rootlookup(dclient.rn,dclient.rp,rec_lookup)
		elif menu_opt == "e":
			print "Exiting the program"
			sys.exit()
		else:
			print "Invalid Menu Entry\nExiting the program"
			sys.exit()

def rootlookup(remotehost, remoteport, senddata):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_ip = socket.gethostbyname( remotehost )
	sock.connect((remote_ip , int(remoteport)))
	sock.sendall(senddata)
	sock.close()

parser = argparse.ArgumentParser(usage='./dht_client <-p client_port <-h client_hostname> <-r root_port> <-R root_hostname>',
                                 description='DHT Client Application',add_help=False)
parser._add_action(argparse._HelpAction(
    option_strings=['-H', '--help'],
    help='Gives you the help documentation and details about optional arguments'
))
parser.add_argument('-p','--client_port', type = int, help='Specify the port for the peer')
parser.add_argument('-h','--client_hostname',help='Specify the hostname of the peer')
parser.add_argument('-r','--root_port', type = int, help='Specify the port of the root')
parser.add_argument('-R','--root_hostname',help='Specify the hostname of the root')
args = parser.parse_args()

ownport = args.client_port
ownhost = args.client_hostname
rootport = args.root_port
roothost = args.root_hostname

dclient = client(ownhost, ownport, roothost, rootport)

sockcl = threading.Thread(target=dclient.listensocket)
menu = threading.Thread(target=menuopt, args = (dclient,))
sockcl.start()
menu.start()
