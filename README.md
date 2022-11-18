# Python-TCP-Communication
 CS164 - Python TCP Communication Protocols
 
In this Project I created multple python server/client files that will emulate various methods of TCP Communication.
The methods included are: "normal" TCP, Selective Repeat and Go-Back-N.

Python was used in order to import the networking libraries so that I could focus on the algorithms used to create
reliable communication.

After downloading the files you will first want to ensure that you are running the server and client files on two separate systems.
This can be two physical machines or two virtual machines on a single host.

Once the files are on two separate systems you will run it through command line using the following:

serverside:
python3 udpserver.py

clientside:
python3 udpclient.py

You'll want to make sure that the server is up and running first so that any packets being sent by the client get a response.
The client side will ask if you want to create a corrupt packet so that you can see how the system handles network errors.
Aside from that, the code itself will need to be modifed in order to adjust other settings such as the window size, amount of
packets sent from the client, timeout length, etc.
