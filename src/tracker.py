#!/usr/bin/env python3
import sys
import socket
import threading
import queue
import json


handleList = []       # list of handles
errNum = 0            # error number
dataQ = queue.Queue() # Queue of messages
jsonStrList = []      # Easy-to-Read list of handles

# Handle Object
class Handle:
    name = ""
    address = ""
    followers = []

    def __init__(self, name, address, leftPort, rightPort, followers):
        self.name = name
        self.address = address
        self.leftPort = leftPort
        self.rightPort = rightPort
        self.followers = followers
    
    # Sorts followers in alphabetical order
    def alphaOrder(followers):
        followers.sort(key=str.lower)

# Initialize buffer size
global bufferSize
bufferSize = 4096

# Error Handling Function
def Error(errNum):
    switch={
        1:print("Error 1: Must input with ip address as argument 1 and port as argument 2")
        }
    print("Error")

# Starting Server
def serverStart(port):
    # initiate udp socket object
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Initialize server Variables
    hostName = "localhost" #socket.gethostbyname(socket.gethostname())
    #port = 37500 #Port number according to group 73 in function leaves range from 37500 to 37999

    # bind socket
    s.bind((hostName, port))

    print(f'Tweeter Server online and listening to {hostName}:{port}')

# Start Server
"""
portNum = int(input("Please enter port number: "))
while portNum < 37500 or portNum > 37999:
    print("Please enter valid port between 37500 and 37999")
    portNum = int(input("Please enter port number: "))
"""
portNum = 37500
serverStart(portNum)


def receive():
    # Implement recvfrom()
    while True:
        data, addr = s.recvfrom(bufferSize)
        dataQ.put((data, addr))
    # Server now listening

# Implement sendto() and commands from users
def broadcast():
    while True:
        data, addr = dataQ.get()
        print(data.decode())

        # Split users' input into list of strings
        newdata = data.decode()
        userInLst = newdata.split()
        #print(userInLst)
        
        # Register command
        if userInLst[0] == "register":
            handleCount = 0
            newUser =  (userInLst[1])[1:]
            for handles in handleList:
                if handles.name == newUser:
                    handleCount = handleCount + 1
            if handleCount == 0:
                newHandle = Handle(newUser, addr, int(userInLst[4]), int(userInLst[5]), [])
                #print(userInLst[6]) #just testing tweet size
                #print(len(userInLst))
                handleList.append(newHandle)
                print(addr)
                s.sendto("SUCCESS".encode(), addr)
            else:
                s.sendto("FAILURE".encode(), addr)
            """
            if addr not in handleList:
                handleList.append([newUser,addr])
                #print(handleList)
                s.sendto("SUCCESS".encode(), addr)
            else:
                s.sendto("FAILURE".encode(), addr)
            """
        # Other Commands for users on Tweeter
        # Exit command
        elif userInLst[1] == "Exit" or userInLst[1] == "exit":
            s.sendto("Connection to Tweeter disconnected".encode(), addr)
            jsonStrList = []
            for handles in handleList:
                if handles.address == addr:
                    droppedName = handles.name
                    handleList.remove(handles)
            for handles in handleList:
                if droppedName in handles.followers:
                    handles.followers.remove(droppedName)
            for handles in handleList:  # could combine with for statement above it
                jsonStr = json.dumps(handles.__dict__)
                jsonStrList.append(jsonStr)
            print(jsonStrList)
        # Query handles command
        elif userInLst[1] ==  "query" and userInLst[2] == "handles":
            handleListnum = len(handleList)
            handleListNames = []
            jsonStrList = []
            for handles in handleList:
                handleListNames.append(handles.name)
                handles.followers.sort(key=str.lower)
                jsonStr = json.dumps(handles.__dict__)
                jsonStrList.append(jsonStr)
            s.sendto(f"Number of handles: {handleListnum}\nHandles List: {handleListNames}".encode(), addr)
            print(jsonStrList)
        # Follow command
        elif userInLst[1] == "follow":
            followerHandle = (userInLst[2])[1:] #first handle
            followedHandle = (userInLst[3])[1:] #second handle
            for handles in handleList:
                if handles.name == followedHandle:
                    if followerHandle in handles.followers:
                        s.sendto("FAILURE".encode(), addr)
                    else:
                        handles.followers.append(followerHandle)
                        s.sendto("SUCCESS".encode(), addr)
                else:
                    pass  
            for handles in handleList:
                handles.followers.sort(key=str.lower)
        # Drop command
        elif userInLst[1] == "drop":
            followerHandle = (userInLst[2])[1:] #first handle
            followedHandle = (userInLst[3])[1:] #second handle
            for handles in handleList:
                if handles.name == followedHandle:
                    if followerHandle in handles.followers:
                        handles.followers.remove(followerHandle)
                        s.sendto("SUCCESS".encode(), addr)
                    else:
                        s.sendto("FAILURE".encode(), addr)
                else:
                    pass  
            for handles in handleList:
                handles.followers.sort(key=str.lower)
        # tweet command
        elif userInLst[1] == "tweet":
            jsonStrList = []
            for handles in handleList:
                handles.followers.sort(key=str.lower)
                jsonStr = json.dumps(handles.__dict__)
                jsonStrList.append(jsonStr)
            s.sendto(f"Handle List: {jsonStrList}".encode(), addr)
        else:
            s.sendto(data, addr)

receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
broadcastThread = threading.Thread(target=broadcast)
broadcastThread.daemon = True
receiveThread.start()
broadcastThread.start()

# Server exit
while True:
    msg = input("")
    msgLst = msg.split()
    if msgLst[0] == "exit":
        sys.exit()
    else:
        pass
