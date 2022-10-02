from pickle import TRUE
import socket
import random

ClientSocket = socket.socket()
host = '10.120.70.106'
port = 8001

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

ans = 'open'

Response = ClientSocket.recv(1024)
while ans[0:5] != 'exit':
    ans = input('\nEnter a command:')
    #will check if any of the commands were used
    if ans[0:9] =='register ':
        #register @<handle> <IPv4-address> <port> 
        #port can be any number of ports
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans == 'query handles':
        #query handles
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:7] == 'follow ':
        #follow @<handle1> @<handle2>
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:5] == 'drop ':
        #drop @<handle1> @<handle2>
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:6] == 'tweet ':
        #tweet @<handle> "tweet"
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:10] == 'end-tweet ':
        #tweet @<handle>
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans != 'exit':
        print('not a valid command try again')

ClientSocket.send(str.encode(ans))
ClientSocket.close()