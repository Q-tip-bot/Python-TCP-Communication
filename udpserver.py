# udpserver.py hosts the udp connections to the clients

# Import Python network libraries
import socket
import sys
import threading
import time
from check import ip_checksum
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8519 # Arbitrary non-privileged port
 
# Datagram (udp) socket creation
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
ExpectedSeqNum = 0;
delay = True
which_packet = 0

# Input to delay the ACK of packet for testing
normal = raw_input("Do you want to delay the ACK? (Y or N)")
if normal == 'Y':
  delay = True
else:
  delay = False

# Talks to the clients indefinitely until closed
while 1:
      # receive data from client (data, addr)
      d = s.recvfrom(1024)
      packet = d[0]
      SeqNum = int(packet[0])
      datalength = int(packet[1])
      data = packet[2:datalength+2]
      check = packet[datalength+2:]
      addr = d[1]

      if not data:
        # Breaks the loop if no data is received 
        break
      elif check == ip_checksum(data) and ExpectedSeqNum == SeqNum:
        # If the data isn't corrupt create a new packet to send to the client
        msg = "ACK" + str(ExpectedSeqNum)
        check = ip_checksum(msg)
        packet = str(ExpectedSeqNum) + str(len(msg)) + msg + check

        # If we want to test delay then sleep
        if delay and which_packet == 1:
          time.sleep(3)
          delay = False

        # Keep track of number of packets sent
        which_packet+=1

        # Send packet to the client
        s.sendto(packet, addr)

        # Modify the seqnum for next message
        if ExpectedSeqNum == 1:
          ExpectedSeqNum = 0
        elif ExpectedSeqNum == 0:
          ExpectedSeqNum = 1
        print 'Message[' + str(addr[1]) + ':' + str(addr[1]) + '] - ' + data.strip()
      else:
        # If the message received is corrupt then resend the old message
        print 'Error: Message Corrupt or received duplicate packet'
        if ExpectedSeqNum != SeqNum:
          msg = "ACK" + str(SeqNum)
          check = ip_checksum(msg)
          packet = str(SeqNum) + str(len(msg)) + msg + check
          s.sendto(packet,addr)

s.close()
