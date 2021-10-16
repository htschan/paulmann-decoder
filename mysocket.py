import socket
import sys
import time


class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except socket.error:
            print("Failed to connect tp ip " +
                  host + " with port " + port)
            sys.exit()

    def close(self):
        self.sock.close()

    def send(self, msg):
        try:
            totalsent = 0
            msglen = len(msg)
            while totalsent < msglen:
                sent = self.sock.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
        except:
            print("Send failed")
            sys.exit()

    def receive(self):
        try:
            chunks = []
            bytes_recd = 0
            finished = False
            while not finished:
                chunk = self.sock.recv(4 * 2048)
                if chunk == b'' or len(chunk) < 2048:
                    finished = True
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            return b''.join(chunks)
        except:
            print("Receive failed")
            sys.exit()

    def query(self, msg):
        self.send(msg)
        time.sleep(1)
        return self.receive()
