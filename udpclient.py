# Import necessary python libraries for networking
import socket   #for sockets
import sys  #for exit
import threading
import time
import logging
from check import ip_checksum # Use Checksum function provided
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

# Prep the connection and the packet info 
host = 'localhost'
port = 8519
SeqNum = 0
packet = ""

# Number of packets to send at once
j = 3 # make this equal to 5 when testing delay

# Function used to resend packet if no response is received with the time limit
def Timeout():
  print 'Timed Out: Retry sending Packet' + str(SeqNum)
  msg = 'Hello ' + str(SeqNum)
  check = ip_checksum(msg)
  packet = str(SeqNum) + str(len(msg)) + msg + check
  s.sendto(packet, (host, port))

# Allows you to create a corrupt packet
Corrupt = raw_input("Do you want there to be a corrupt packet?(Y or N)")

while(1) :
    progress = raw_input("Press Enter to send more packets")

    for i in range(0, j):
      # Create the packet to send to the server
      t = threading.Timer(2.0, Timeout)
      msg = 'Hello ' + str(SeqNum)
      if i == 1 and Corrupt == 'Y':
        check = str(1) + ip_checksum(msg)
      else:
        check = ip_checksum(msg)
      packet = str(SeqNum) + str(len(msg)) + msg + check

      try :
        # Start the timer
        t.start()

        # Send the packet to the server
        s.sendto(packet, (host, port))

        # Receive response from the server
        d = s.recvfrom(1024)

        # Parse out the response from the server
        packet = d[0]
        AckNum = int(packet[0])
        replylength = int(packet[1])
        reply = packet[2:replylength+2]
        check = packet[replylength+2:]
        addr = d[1]

        # If the proper reply is received then cancel the timer and move seqnum
        # Otherwise the message is corrupt
        if check == ip_checksum(reply) and AckNum == SeqNum:
          t.cancel()
          print 'Server reply : ' + reply
          if SeqNum == 1:
            SeqNum = 0
          elif SeqNum == 0:
            SeqNum = 1
        else:
          print 'Error: Message Corrupt or has wrong sequence number, waiting for another ACK'

        # If not response is received then break the loop     
        if not d:
          break

      except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

s.close()
