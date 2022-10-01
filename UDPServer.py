import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '10.120.70.106'
port = 16001
clients = []#client, IPv4
gameId = 100

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('Welcome to Tweeter!'))
    connec = True
    while connec:
        data = connection.recv(2048)
        decodeddata = data.decode('utf-8')
        reply = 'Server Says: ' + data.decode('utf-8')
        if decodeddata[0:9] == 'register ':#checks if command used was register
            player = decodeddata.split(' ')
            player.remove('register')
            player.append('0') # this number will represent 1 if in game 2 if dealer and 0 if not in game
            if(str(len(player)) != 4):
                reply = 'FAILURE'
            for i in players:
                if i[2] == players[2]:
                    reply = 'FAILURE'
            for i in players:
                if i[0] == players[0]:
                    reply = 'FAILURE'
            if reply != 'FAILURE':
                players.append(player)
                reply = 'SUCCESS'
            connection.sendall(str.encode(reply))
        elif decodeddata == 'query handles':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata == 'follow':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata == 'drop':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata == 'tweet':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata == 'end-tweet':
            #

            connection.sendall(str.encode(reply))
        elif decodeddata == 'exit':
            #

            connection.sendall(str.encode(reply))
        else:
            reply = 'error'
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    clientinfo = []
    clientinfo.append(Client)
    clientinfo.append(address[0])
    clients.append(clientinfo) #client and address[0](IPv4) get saved
    start_new_thread(threaded_client, (Client, ))
    
ServerSocket.close()