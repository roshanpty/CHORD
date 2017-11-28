import argparse
import socket
import sys
import thread
import hashlib

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

while 1:
	menu_opt = raw_input("DHT Client Menu:\n \
	Enter the letter corresponding to the operation you are performing\n \
	1. Store an object - s\n \
	2. Retrieve an object in iterative fashion - i\n \
	3. Retrieve an object in recursive fashion - r\n \
	4. Exit the DHT Client program - e\n ")

	if menu_opt == "s":
		print "Entering object store operation"
		filename = raw_input("Enter the full path file you want to store:\nExample: /home/user/filename.txt\n")
	elif menu_opt == "i":
		print "Performing iterative retreival of object"
		sys.exit()
	elif menu_opt == "r":
		print "Performing recursive retreival of object"
		sys.exit()
	elif menu_opt == "e":
		print "Exiting the program"
		sys.exit()
	else:
		print "Invalid Menu Entry\nExiting the program"
		sys.exit()


