from pickle import TRUE
import socket
import random
from _thread import *

ClientSocket = socket.socket()
ListeningSocket = socket.socket()
host = '10.120.70.106'
myIPv4 = ''
myHandle = ''
port = 8001
registered = 0 #0 for not registered, 1 for registred

print('Waiting for connection')
try:
    ClientSocket.connect((host, 8000)) #host,8000 is the server info
except socket.error as e:
    print(str(e))

#accepts anyone listening
def threaded_client(connection):
    data = connection.recv(2048)
    print('\n')
    print(data.decode('utf-8'))
    print('\nEnter a command:')
    #connection.recv(2048)
    connection.close()

#starts a listening port
def threaded_port(connectionport):
    try:
        ListeningSocket.bind((myIPv4, int(connectionport)))
    except socket.error as e:
        print(str(e))

    ListeningSocket.listen(5)

    while True:
        Client, address = ListeningSocket.accept()
        start_new_thread(threaded_client, (Client, ))

ans = 'open'
Response = ClientSocket.recv(1024)
notExit = True
while notExit:
    ans = input('\nEnter a command:\n')
    #will check if any of the commands were used
    if ans[0:9] =='register ':#register @<handle> <IPv4-address> <port> 
        #only one port can be used
        if registered == 0:
            ClientSocket.send(str.encode(ans))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))
            if(Response.decode('utf-8') == 'SUCCESS'):
                #start listening port
                splitans = ans.split(' ')
                splitans.remove('register') 
                myIPv4 = splitans[1]
                myHandle = splitans[0]
                start_new_thread(threaded_port, (splitans[2], ))
                registered = 1
        else:
            print("FAILURE, you are already registred")
    elif ans == 'query handles':#query handles
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:7] == 'follow ':#follow @<handle1> @<handle2>
        if(registered == 1):
            ClientSocket.send(str.encode(ans))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))
        else:
            print('FAILURE, please register first')
    elif ans[0:5] == 'drop ':#drop @<handle1> @<handle2>
        if(registered == 1):
            ClientSocket.send(str.encode(ans))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))
        else:
            print('FAILURE, please register first')
    elif ans[0:6] == 'tweet ':#tweet @<handle> "tweet"
        #break tweet command
        anstuple = ans.split(' ')
        if((registered == 1) and (len(anstuple) >= 3)):
            ClientSocket.send(str.encode(ans))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))
            ClientSocket.send(str.encode('recv'))
            if(Response.decode('utf-8') == 'SUCCESS'):
                #get num of followers
                numOfFollowers = ClientSocket.recv(1024)
                ClientSocket.send(str.encode('recv'))
                if int(numOfFollowers.decode('utf-8')) != 0:
                    #then list(tuple of followers
                    response = ClientSocket.recv(1024)
                    listOfFollower = response.decode('utf-8')
                    listOfFollowers = listOfFollower.split(' ')
                    #then propagate tweet
                    if(int(numOfFollowers.decode('utf-8')) >= 1):
                        i = 0
                        while i < int(numOfFollowers):#IPv4, port
                            #make temp socket
                            tempSocket = socket.socket()
                            try:
                                tempSocket.connect((listOfFollowers[2*i], int(listOfFollowers[(2*i)+1]))) #conect to IPv4 and port
                            except socket.error as e:
                                print(str(e))
                            tempSocket.send(str.encode(anstuple[2]))
                            tempSocket.close()
                            i += 1  
                #send end-tweet command automatically without user input
                ans = 'end-tweet '
                ans += myHandle
                ClientSocket.send(str.encode(ans))
                Response = ClientSocket.recv(1024)
                print(Response.decode('utf-8'))
        else:
            print('FAILURE')
    elif ans[0:5] == 'exit ':#exit @<handle>
        if(registered == 1):
            ClientSocket.send(str.encode(ans))
            Response = ClientSocket.recv(1024)
            if(Response.decode('utf-8') == 'SUCCESS'):
                print(Response.decode('utf-8'))
                notExit = False
            else:
                print(Response.decode('utf-8'))
        else:
            print('FAILURE')
    else:
        print('not a valid command try again')
ClientSocket.close()