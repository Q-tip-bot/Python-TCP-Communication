# The below program is a server that uses Go-Back-N Protocol

# Import python networking libraries
import socket
import sys
import threading
import time
from check import ip_checksum
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8519 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

# Define the packet variables for the first message
ExpectedSeqNum = 0
msg = "ACK" + str(ExpectedSeqNum)
check = ip_checksum(msg)
packet = str(ExpectedSeqNum) + str(len(msg)) + msg + check

#now keep talking with the client
while 1:
      # receive data from client (data, addr)
      d = s.recvfrom(1024)

      # Parse out the packet
      packet = d[0]
      SeqNum = int(packet[0])
      datalength = int(packet[1])
      data = packet[2:datalength+2]
      check = packet[datalength+2:]
      addr = d[1]
 
      # Break loop if no data is received
      if not data: 
        break
      elif check == ip_checksum(data) and ExpectedSeqNum == SeqNum:
        # Send back acknowledgment if the packet isn't corrupted and the seqnum is expected
        msg = "ACK" + str(ExpectedSeqNum)
        check = ip_checksum(msg)
        packet = str(ExpectedSeqNum) + str(len(msg)) + msg + check
        s.sendto(packet, addr)
        ExpectedSeqNum+=1
        print 'Message[' + str(addr[1]) + ':' + str(addr[1]) + '] - ' + data.strip()
      else:
        print 'Error: Message Corrupt or received duplicate packet'
        print 'Throwing away packet and resending ACK' + str(ExpectedSeqNum)
        s.sendto(packet, addr)

s.close()
