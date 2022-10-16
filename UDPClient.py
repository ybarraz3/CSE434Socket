from pickle import TRUE
import socket
import random

ClientSocket = socket.socket()
ListeningSocket = socket.socket()
host = '10.120.70.117'
port = 8001
registered = 0 #0 for not registered, 1 for registred
exit = False

print('Waiting for connection')
try:
    ClientSocket.connect((host, 8000)) #host,8000 is the server info
except socket.error as e:
    print(str(e))

#accepts anyone listening
def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        print(data.decode('utf-8'))
    connection.close()

#starts a listening port
def threaded_port(connectionport):
    Client, address = ListeningSocket.accept()
    start_new_thread(threaded_client, (Client, ))

ans = 'open'
Response = ClientSocket.recv(1024)
while ans[0:5] != 'exit':
    ans = input('\nEnter a command:')
    #will check if any of the commands were used
    if ans[0:9] =='register ':
        #register @<handle> <IPv4-address> <port> 
        #port can be any number of ports
        if registed == 0:
            ClientSocket.send(str.encode(ans))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))
            #start listening port

            registered = 1
        else:
            print("FAILURE, you are already registred")
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
    else:
        print('not a valid command try again')

ClientSocket.send(str.encode(ans))
ClientSocket.close()