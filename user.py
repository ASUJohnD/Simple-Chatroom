#!/usr/bin/env python3
import sys
import socket
import threading
import queue
import json
import time

dataQ = queue.Queue() # Queue of messages

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("IPv4 Address: ", socket.gethostbyname(socket.gethostname()))
print("Use Register command to connect to Tweeter\nChoose port between 37600 and 37999: ")

# Register command to connect to server
msg = input("")
msgLst = msg.split()
if msgLst[0] == "register":
    name = (msgLst[1])[1:] # gets name without @
    ipAddr = msgLst[2]
    port = int(msgLst[3])
    leftPort = int(msgLst[4])
    rightPort = int(msgLst[5])

def reverse(n):
    return int(bin(n)[:1:-1], 2)

client.bind((ipAddr, port))
# Testing (sometimes doesn't work with just port, need htons when using different hosts)
#print(port)
#print(socket.htons(port))
#print(reverse(socket.htons(port)))

serverIP = "localhost"
client.sendto(msg.encode(), (serverIP, 37500))

def receive():
    while True:
        try:
            # Messages recieved from server
            msg, _ = client.recvfrom(4096)
            print(msg.decode())
        except:
            pass

# Left Port
lp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lp.bind((ipAddr, leftPort))
def leftReceive():
    while True:
        data, addr = lp.recvfrom(4096)
        dataQ.put((data,addr))

# Right Port
rp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rp.bind((ipAddr, rightPort))
def rightBroadcast():
    while True:
        data, addr = dataQ.get()
        print(data.decode())

receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
leftReceiveThread = threading.Thread(target=leftReceive)
leftReceiveThread.daemon = True
rightBroadcastThread = threading.Thread(target=rightBroadcast)
rightBroadcastThread.daemon = True
receiveThread.start()


while True:
    msg = input("")
    msgLst = msg.split()
    # Meesages get sent unless Exit command is issued
    if msgLst[0] == "exit":
        # Could change to only send meesage and add name on server side
        client.sendto(f"{name}: {msg}".encode(), (serverIP, 37500))  
        sys.exit()
    elif msgLst[0] == "tweet":
        tweetWordLength = len(msgLst) - 2
        tweetString = ""
        i = 2
        while len(msgLst) > i:
            tweetString = tweetString + msgLst[i]
            i = i + 1
        tweetCharNum = len(tweetString)
        tweetString = ""
        i = 2
        while len(msgLst) > i:
            if i == 2:
                tweetString = tweetString + msgLst[i]
            else:
                tweetString = tweetString + " " + msgLst[i]
            i = i + 1
        print("Tweet: ", tweetString)
        #charLength = len([ele for ele in tweetString if ele.isalpha()])
        #print(charLength)
        print(len(tweetString))
        print(tweetCharNum)
        #print(tweetWordLength)
        if len(tweetString) > 142:
            print("FAILURE: Message must be equal to or below 140 characters long.")
        else:
            leftReceiveThread.start()
            rightBroadcastThread.start()
            tweetSender = (msgLst[1])[1:] #handle sending tweet
            client.sendto(f"{name}: {msg}".encode(), (serverIP, 37500))
    else:
        client.sendto(f"{name}: {msg}".encode(), (serverIP, 37500))


#exitThread = threading.Thread(target=ifExit)
#exitThread.start()
