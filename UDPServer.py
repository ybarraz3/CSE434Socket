import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '10.120.70.106'
port = 8001
clients = []#client, IPv4
handles = []#handle, IPv4, ports, followers

try:
    ServerSocket.bind((host, port))
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
            handleinfo = decodeddata.split(' ')
            handleinfo.remove('register')
            handleinfo.append([]) # this will represent the followers
            if((str(len(handleinfo))) <= 4):
                reply = 'FAILURE'
            for i in handles:
                if i[0] == handles[0]:
                    reply = 'FAILURE'
            if reply != 'FAILURE':
                handles.append(handles)
                reply = 'SUCCESS'
            connection.sendall(str.encode(reply))
        elif decodeddata == 'query handles':#checks if command used was query handles
            #returns the list of handles
            if handles:
                reply = str(len(handles[0])) + '\n' #the ammount of players
                reply += str(handles[0])#returns list
            else:
                reply = '0\n[]'#no handles
            connection.sendall(str.encode(reply))
        elif decodeddata[0:7] == 'follow ':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata[0:5] == 'drop ':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata[0:6] == 'tweet ':
            #placeholder for full project


            connection.sendall(str.encode(reply))
        elif decodeddata[0:10] == 'end-tweet':
            #placeholder for full project


            connection.sendall(str.encode(reply))
        elif decodeddata == 'exit':
            #makes connection false
            #then removes them from handle list 
            #and from other handle's followers


            connec = False;
        else:
            reply = 'error'
    handles.remove(handleinfo)
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