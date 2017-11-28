# CHORD
An implementation of CHORD DHT P2P protocol

## GENERAL DESCRIPTION
____________________

CHORD is a simple Peer to Peer protocol which implements a Distributed Hash Table detailed as per the paper - [Stoica, Ion, Robert Morris, David Karger, M. Frans Kaashoek, and Hari Balakrishnan. "Chord: A scalable peer-to-peer lookup service for internet applications." ACM SIGCOMM Computer Communication Review 31, no. 4 (2001): 149-160.](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf)

This project has two components, DHT Peer (dht_peer.py) and DHT Client(dht_client.py).

### DHT Peer:

DHT Peer program defines a distributed network of nodes which are self aware of their postion in the CHORD architecture which is a ring. Each node of the CHORD architecture is aware of it's successor and predecessor. Each node joins the CHORD network by initiating communication with root node. Root node in this chord implementation is very similar to other nodes except for two significant capabilities - managing join requests and managing initial client requests.

### DHT Client:

DHT client program is used to connect to the CHORD network for storing and retreival of objects on the nodes. It supports two distinct modes for retreival - iterative and recursive queries to the nodes.

## USAGE & EXAMPLES
_________________

### DHT Peer:

*Usage:* `./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>`

*Arguments:*
```  -H, --help            Gives you the help documentation and details about optional arguments
  -m PEERTYPE, --peertype PEERTYPE
                        Specify 1 if the peer is root and 0 otherwise
  -p OWN_PORT, --own_port OWN_PORT
                        Specify the port for the peer
  -h OWN_HOSTNAME, --own_hostname OWN_HOSTNAME
                        Specify the hostname of the peer
  -r ROOT_PORT, --root_port ROOT_PORT
                        Specify the port of the root
  -R ROOT_HOSTNAME, --root_hostname ROOT_HOSTNAME
                        Specify the hostname of the root
```
Note: If -m is not specified the peer will run as a normal node.

*Example:*

To start the root
`$ ./dht_peer.py -m 1 -p 3400 -h hostname.tld`

To start a peer
`$ ./dht_peer.py -p 3402 -h normalhost.tld -r 3400 -R roothost.tld`

### DHT Client:

*Usage:* `./dht_client <-p client_port <-h client_hostname> <-r root_port> <-R root_hostname>`

*Arguments:*
```  -H, --help            Gives you the help documentation and details about
                        optional arguments
  -p CLIENT_PORT, --client_port CLIENT_PORT
                        Specify the port for the peer
  -h CLIENT_HOSTNAME, --client_hostname CLIENT_HOSTNAME
                        Specify the hostname of the peer
  -r ROOT_PORT, --root_port ROOT_PORT
                        Specify the port of the root
  -R ROOT_HOSTNAME, --root_hostname ROOT_HOSTNAME
                        Specify the hostname of the root
```
*Example:*

To start the client
`$ ./dht_client -p 3405 -h normalclient.tld -r 3400 -R roothost.tld`
