#!/usr/bin/env python3
import binascii
import hashlib
import os
import signal
import socketserver
import string
import sys

from flag import FLAG

HOST = "127.0.0.1"
PORT = 6051

N = 128
assert N % 8 == 0
OUTPUT = 32
HIDDEN = N-OUTPUT
TIME = 120

def gcd(u, v):
    while v:
        u, v = v, u % v
    return abs(u)

def nextstate(state, mult, inc, modulus):
    return (state*mult + inc) % modulus

def gen_prefix(n):
    # can't use random module due to forking :(
    alphabet = string.digits+string.ascii_letters
    p = os.urandom(n)
    return ''.join(alphabet[i % len(alphabet)] for i in p)

class lcgHandler(socketserver.BaseRequestHandler):
    def myrecv(self, n):
        x = self.request.recv(1)
        if n > 0 and x == b'':
            sys.exit(1)
        return x

    def recvline(self, limit):
        s = b""
        while not s.endswith(b"\n") and len(s) <= limit:
            s += self.myrecv(1)
        return s

    def handle(self):
        # proof of work
        '''
        prefix = gen_prefix(10)
        self.request.sendall("Give me a string starting with {} of length {} so its sha256sum ends in ffffff.\n".format(prefix, len(prefix)+6).encode('utf8'))
        l = self.recvline(len(prefix)+6+1).strip()
        if len(l) != len(prefix)+6 or not l.startswith(prefix.encode('utf8')) or hashlib.sha256(l).hexdigest()[-6:] != "ffffff":
            self.request.sendall(b"Nope.\n")
            return
        '''

        # the good stuff
        self.request.sendall("Guess my numbers for the flag! You have {} seconds.\n".format(TIME).encode('utf8'))

        self.MODULUS = int(binascii.hexlify(os.urandom(N // 8)), 16)
        self.MULT = 0
        self.INC = 0
        self.STATE = 0

        while not (1 <= self.MULT < self.MODULUS and gcd(self.MULT, self.MODULUS) == 1):
            self.MULT = int(binascii.hexlify(os.urandom(N // 8)), 16)
        while not (1 <= self.INC < self.MODULUS and gcd(self.INC, self.MODULUS) == 1):
            self.INC = int(binascii.hexlify(os.urandom(N // 8)), 16)
        while not (1 <= self.STATE < self.MODULUS):
            self.STATE = int(binascii.hexlify(os.urandom(N // 8)), 16)

        # outputs
        s = b""
        for i in range(40):
            output = self.STATE >> HIDDEN
            s += str(output).encode("utf8") + b" "
            self.STATE = nextstate(self.STATE, self.MULT, self.INC, self.MODULUS)
        self.request.sendall(b"Outputs: " + s + b"\n")

        signal.alarm(TIME)

        # predict
        failures = 0
        for i in range(200):
            l = int(self.recvline(30).strip())
            output = self.STATE >> HIDDEN
            if output != l:
                self.request.sendall("Nope. (Expected {}.)\n".format(output).encode('utf8'))
                failures += 1
                if failures >= 5:
                    self.request.sendall(b"Too many failures. Better luck next time!\n")
                    return
            else:
                self.request.sendall(b"Good.\n")
            self.STATE = nextstate(self.STATE, self.MULT, self.INC, self.MODULUS)

        self.request.sendall("Congrats! {}\n".format(FLAG).encode('utf8'))

if __name__ == '__main__':
    socketserver.ForkingTCPServer.allow_reuse_address = True
    server = socketserver.ForkingTCPServer((HOST, PORT), lcgHandler)
    server.serve_forever()
