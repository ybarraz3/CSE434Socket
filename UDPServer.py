import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '10.120.70.106'
port = 8001
clients = []#client, IPv4
handles = []#handle, IPv4, ports, followers
handleconnec = []#handle, port info

try:
    ServerSocket.bind((host, 8000))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection...')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('Welcome to Tweeter!'))
    connec = True
    handleinfo = []
    while connec:
        data = connection.recv(2048)
        decodeddata = data.decode('utf-8')
        reply = 'Server Says: ' + data.decode('utf-8')
        if decodeddata[0:9] == 'register ':#checks if command used was register
            #register @<handle> <IPv4> <port>
            newhandleinfo = decodeddata.split(' ')
            newhandleinfo.remove('register')
            if(len(newhandleinfo) != 3):
                reply = 'FAILURE'
            else:
                for i in handles:
                    if i[0] == newhandleinfo[0]:
                        reply = 'FAILURE'
                if reply != 'FAILURE':
                    newhandleinfo.append([]) # this will represent the followers
                    handles.append(newhandleinfo)
                    reply = 'SUCCESS'
            connection.sendall(str.encode(reply))
        elif decodeddata == 'query handles':#checks if command used was query handles
            #query handles
            #returns the list of handles
            if handles:
                reply = str(len(handles)) + '\n' #the ammount of players
                reply += str(handles)
            else:
                reply = '0\n[]'#no handles
            connection.sendall(str.encode(reply))
        elif decodeddata[0:7] == 'follow ':#checks if command used was follow
            #follow @<handle1> @<handle2>
            #split into list
            followinfo = decodeddata.split(' ')
            #handle i wants to follow handle j
            #check if i isn't already in follow of handle j
            #if i is in j then failure
            for i in handles:
                if i[0] == followinfo[2]:
                    for j in i[3]:
                        if j == followinfo[1]:
                            reply = 'FAILURE'
            #else i is not in follow of j, then add and return success
            if reply != 'FAILURE':
                reply = 'FAILURE'
                for i in handles:
                    if i[0] == followinfo[2]:
                        i[3].append(followinfo[1])
                        reply = 'SUCCESS'
            connection.sendall(str.encode(reply))
        elif decodeddata[0:5] == 'drop ':#checks if command used was drop
            #drop @<handle1> @<handle2>
            #handle i wants to drop handle j
            #first check if i is in followers of j
            followinfo =  decodeddata.split(' ')
            for i in handles:
                if i[0] == followinfo[2]:
                    for j in i[3]:
                        if j == followinfo[1]:
                            reply = 'SUCCESS'#it is present
            if reply == 'SUCCESS':
                #then remove
                for i in handles:
                    if i[0] == followinfo[2]:
                        i[3].remove(followinfo[1])
            else:#if handle i is not a follower then FAILURE
                reply == 'FAILURE'
            connection.sendall(str.encode(reply))
        elif decodeddata[0:6] == 'tweet ':
            #tweet @<handle> "tweet"
            tweetinfo = decodeddata.split(' ')
            #recieve tweet command
            #return tuple of followers with port and IPv4 info
            for i in handles:
                if(i[0] == tweetinfo[1]):
                    #first send number of followers
                    reply = len(i[3])
                    connection.sendall(str.encode(reply))
                    #then send the tuple
                    reply = i[3]
                    connection.sendall(str.encode(reply))
            #then do end-tweet together
            data = connection.recv(2048)#recieve command
            decodeddata = data.decode('utf-8')
            reply = 'SUCCESS'
            connection.sendall(str.encode(reply))
        elif decodeddata[0:5] == 'exit ':
            #exit @<handle>
            #makes connection false
            #then removes them from handle list 
            #and from other handle's followers
            handles.remove(handleinfo)
            #fix ^






            for i in handles:
                for j in i[3]:
                    if j == handleinfo[3]:
                        handles[i][3].remove(handleinfo[3])
            connec = False;
        else:
            reply = 'error'
    
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0])# + ':' + str(address[1])
    clientinfo = []
    clientinfo.append(Client)
    clientinfo.append(address[0])
    clients.append(clientinfo) #client and address[0](IPv4) get saved
    start_new_thread(threaded_client, (Client, ))
    
ServerSocket.close()