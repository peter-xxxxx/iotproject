import socket
import time

#UDP_IP = "192.168.0.100"
UDP_IP = "192.168.0.8"
UDP_PORT = 3000
MESSAGE = str(time.asctime())+"Hello World!"

print "UDP Target IP:", UDP_IP
print "UDP Tartget Port:", UDP_PORT
print "Message:", MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
