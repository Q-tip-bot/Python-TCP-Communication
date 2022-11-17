# The below program is a client that uses Go-Back-N Protocol

# Import python networking libraries
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

# Define host and port to be used 
host = 'localhost'
port = 8519

# Define variables for the packet to be sent
N = 4 # This is the window size
base = 0
nextseqnum = 0
sndpkt = []
packet = ""

# Function used to handle a timeout when a response isn't received in time
def Timeout():
  t = threading.Timer(2.0,Timeout)
  t.start()
  for i in range(base,nextseqnum):
    print 'Timed Out: Retry sending Packet' + str(i)
    s.sendto(sndpkt[i], (host, port))

# Allows the user to manually trigger a corrupt packet
Corrupt = raw_input("Do you want there to be a corrupt packet?(Y or N)")

while(1):
    # Package all the data up to the window size
    while nextseqnum < base+N and nextseqnum < 8:
      t = threading.Timer(2.0, Timeout)
      msg = 'Hello ' + str(nextseqnum)
      if nextseqnum == 2 and Corrupt == 'Y':
        check = str(1) + ip_checksum(msg)
      else:
        check = ip_checksum(msg)
      packet = str(nextseqnum) + str(len(msg)) + msg + check
      sndpkt.append(packet)

      try :
        # Send the packet with all data
        s.sendto(packet, (host, port))

        # Start the timeout if the base is being sent
        if base == nextseqnum:
          t.start()

        # Defines which part of packet to corrupt
        if nextseqnum == 2 and Corrupt == 'Y':
          check = ip_checksum(msg)
          packet = str(nextseqnum) + str(len(msg)) + msg + check
          sndpkt[2] = packet
        nextseqnum+=1
        
      except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
    # Wait for a reply to increment the window
    d = s.recvfrom(1024)
    packet = d[0]
    AckNum = int(packet[0])
    replylength = int(packet[1])
    reply = packet[2:replylength+2]
    check = packet[replylength+2:]
    addr = d[1]

    # If the reply is received with now errors then stop the timer.
    if check == ip_checksum(reply) and AckNum == base:
      print 'Server reply : ' + reply
      base = AckNum + 1
      t.cancel()
      if base == nextseqnum:
        t.cancel()
      else:
        # Reset the timer to process the rest of the packet
        t = threading.Timer(2.0, Timeout)
        t.start()
    else:
      print 'Error: Message Corrupt or duplicate ACK, waiting for another ACK'
             
    if not d:
      break

s.close()
