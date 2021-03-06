import socket
from _thread import *
import sys
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip_add = os.popen("curl ifconfig.me").read() #Used for linux server
ip_add = socket.gethostbyname(socket.gethostname())
print("IP: ", ip_add)
server = ip_add
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:200,200"]

def threaded_client(conn):
    global currentId, pos
    print(currentId)
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:

        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data: # If the player gets out
                conn.send(str.encode("Goodbye"))
                break

            else:

                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply
                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]

            time.sleep(0.001)
            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()
    currentId = str(int(currentId)-1)

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))