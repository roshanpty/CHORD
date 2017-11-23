import argparse

# DHT peer application.
# Usage: ./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>

parser = argparse.ArgumentParser(usage='./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>',
                                 description='DHT Peer Application')
parser.add_argument('type',metavar='m',help='Specify 1 if the peer is root and 0 otherwise')
parser.add_argument('own_port',metavar='p',help='Specify the port for the peer')
parser.add_argument('own_hostname',metavar='h',help='Specify the hostname of the peer')
parser.add_argument('root_port',metavar='r',help='Specify the port of the root')
parser.add_argument('root_hostname',metavar='R',help='Specify the hostname of the root')

args = parser.parse_args()
print(args.accumulate)