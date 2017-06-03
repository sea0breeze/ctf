#!/usr/bin/env python
# coding=utf-8
from os import urandom
from secret_socket import socket_with_bob
import alice_private_key
import bob_public_key

def str2int(s):
    return int(s.encode('hex'), 16)

def int2str(i):
    tmp = hex(i)[2:].strip('L')
    tmp = ('0' if len(tmp)%2 else '') + tmp
    return tmp.decode('hex')

def sign_and_encrypt(m):
    m = urandom(126-len(m)) + '\x00' + m
    sig = pow(str2int(m), alice_private_key.d, alice_private_key.N2)
    assert sig < bob_public_key.N1
    sig_enc = pow(sig, bob_public_key.e, bob_public_key.N1)
    return int2str(sig_enc)

def decrypt_and_verify(c):
    sig = pow(str2int(c), alice_private_key.d, alice_private_key.N1)
    assert sig < bob_public_key.N2
    message = pow(sig, bob_public_key.e, bob_public_key.N2)
    message = int2str(message)
    message = message[message.rindex('\x00')+1:]
    return message

s = socket_with_bob()
recv_enc = s.recv()
recv_message = decrypt_and_verify(recv_enc)
assert recv_message == "Ooops, my flag have been encrypted by wannacry! Could you please send it to me again, Alice?"

with open('flag.txt') as f:
    flag = f.read()
send_message = "Well, OK... Here is what you what: {}".format(flag)
assert len(send_message) < 128
to_send = sign_and_encrypt(send_message)
s.send(to_send)
s.close()

with open('send.bak', 'wb') as f:
    f.write(to_send)
