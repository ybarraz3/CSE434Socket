import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '10.120.70.106'
port = 16001
players = [] #user, IPv4, port, inGame: 0=no 1=yes&player 2=yes&dealer
games = []#user, k, gameId
clients = []#client, IPv4
gameId = 100

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def sortPlayers(list):
    return list[3]

def threadded_game(playerList, dealer, gameIdnum):
    print('Started a new game')
    #make sure players get marked as players
    for i in players:
        for j in playerList: # has the same thing as players but player[4] has client
            if(j[0] == i[0]):
                i[3] = 1
    
    #add the dealer to the player list to loop through
    playerList.insert(0,dealer)

    #add a special connection for dealer messages
    dealerClient
    for i in clients:
        if i[1] == dealer[1]:
            dealerClient = i[0]

    #initialize cards
    for i in playerList:
        for j in clients:
            if i[1] == j[1]:
                i.append(j[0])
                j[i].sendall(str.encode('player'))
                msg = 'sixCard'#command to recieve starting cards
                dealerClient.sendall(str.encode(msg))#sends msg
                msgRecv = dealerClient.recv(2048)#recieve card from dealer
                decodedmsg = msgRecv.decode('utf-8')#decode msg
                j[i].sendall(str.encode(decodedmsg))#send the player their cards

    #loop through turns
    turn = 0
    game = True
    while game:
        for currPlayer in playerList:
            #maybe add a loop to ask user turn for input
            msg = 'your turn'
            currPlayer[4].sendall(str.encode(msg))#sends msg
            msgRecv = currPlayer[4].recv(2048)#recieve player command
            decodedmsg = msgRecv.decode('utf-8')#decode msg
            if decodedmsg[0:6] == 'stock ':#stock cardToBeExchanged
                #request a stock card from dealer
                card = decodedmsg.split(' ')#split the message into the stock and card
                newmsg = 'stockCard ' + card[1]#add the card to message
                dealerClient.sendall(str.encode(newmsg))#send the command and card to dealer
                msgRecv = dealerClient.recv(2048)#recieve new card from dealer
                decodedmsg = msgRecv.decode('utc-8')#decode msg
                currPlayer[4].sendall(str.encode(decodedmsg))#send card to player
            elif decodedmsg[0:8] == 'discard ':
                #request the discarded card
                card = decodedmsg.split(' ')#split the message into the discard and card
                newmsg = 'discardCard ' + card[1]
                dealerClient.sendall(str.encode(newmsg))#send the command and card to dealer
                msgRecv = dealerClient.recv(2048)#recieve new card from dealer
                decodedmsg = msgRecv.decode('utc-8')#decode msg
                currPlayer[4].sendall(str.encode(decodedmsg))#send card to player
            elif decodedmsg[0:5] == "steal ":#steal the card from the specified player
                card = decodedmsg.split(' ')#split msg into steal name and card
                newmsg = 'stealcard ' + card[2]
                for i in playerList:#send msg to player with card to swap
                    if i[0] == card[1]:
                        i[4].sendall(str.encode(newmsg))#send msg
                        msgRecv = i[4].recv(2048)#receive new card from other player
                        decodedmsg = msgRecv.decode('utc-8')
                        currPlayer[4].sendall(str.encode(decodedmsg))#send the card back to og player
            elif decodedmsg[0:4] == 'end ':#checks if command used was end game
                reply = 'FAILURE'
                initialLength = len(games)
                games = [i for i in games if i[0] != decodedmsg[12:]]
                if initialLength != len(games):
                    reply = 'SUCCESS'
                    game = False

    #make sure playerList players get set to 0

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server!'))
    connec = True
    while connec:
        data = connection.recv(2048)
        decodeddata = data.decode('utf-8')
        reply = 'Server Says: ' + data.decode('utf-8')
        if decodeddata == 'query games':#checks if command used was query games
            if games:
                reply = str(len(games)) + '\n' #the ammount of players
                reply += str(games)#returns list
            else:
                reply = '0\n[]'#no games
            connection.sendall(str.encode(reply))
        elif decodeddata == 'query players':#checks if command used was query players
            global players
            if players:
                reply = str(len(players)) + '\n' #the ammount of players
                reply += str(players)#returns list
            else:
                reply = '0\n[]'#no players
            connection.sendall(str.encode(reply))
        elif decodeddata[0:9] == 'register ':#checks if command used was register
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
        elif decodeddata[0:12] == 'de-register ':#checks if command used was de-register
            reply = 'FAILURE'
            initialLength = len(players)
            players = [i for i in players if i[0] != decodeddata[12:]]
            resultLength = len(players)
            if initialLength != resultLength:
                reply = 'SUCCESS'
            connection.sendall(str.encode(reply))
        elif decodeddata == 'join game':
            reply = 0
            for i in players:
                if i[1] == address[0]:
                    reply == i[3]
            connection.sendall(str.encode(reply))
        elif decodeddata == 'exit':
            connec = False
        elif decodeddata[0:11] == 'start game ':
            reply = 'FAILURE'
            game = decodeddata.split(' ')
            game.remove('start')
            game.remove('game') # list becomes: user k
            gameStart = False
            dealer = []
            if 1 <= int(game[1]) <= 3:
                for i in players:# check if user is in player
                    if game[0] == player[0]:
                        j = 0
                        for i in players:#check if there are dealer is already in game
                            if i[0] == game[0]:
                                gameStart = True
                                i[3] = 2
                                dealer.append(i)
                        for i in players:#check if there are sufficient players available
                            if i[3] == '0':
                                j = j + 1
                        if j >= game[1]:
                            if gameStart == True: #start a new thread and begin game
                                players.sort(key=sortPlayers)
                                playerList = players[0:j]
                                gameId += 1
                                start_new_thread(threadded_game(playerList,dealer,gameId))
                                game.append(gameId)
                                games.append(game)
                                reply = 'SUCCESS'
                        else:
                            for i in players:#no game, set dealer back to 0
                                if i[0] == game[0]:
                                    gameStart = False
                                    i[3] = 0
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