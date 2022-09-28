from pickle import TRUE
import socket
import random

ClientSocket = socket.socket()
host = '10.120.70.106'
port = 16001
inGame = 0 #0 for not in game, 1 for player, 2 for dealer
cards = []
visibleCards = 2
stock = ['A-D','2-D','3-D','4-D','5-D','6-D','7-D','8-D','9-D','10-D','J-D','Q-D','K-D',
    'A-H','2-H','3-H','4-H','5-H','6-H','7-H','8-H','9-H','10-H','J-H','Q-H','K-H',
    'A-S','2-S','3-S','4-S','5-S','6-S','7-S','8-S','9-S','10-S','J-S','Q-S','K-S',
    'A-C','2-C','3-C','4-C','5-C','6-C','7-C','8-C','9-C','10-C','J-C','Q-C','K-C']
random.shuffle(stock)                                 
discard = []
discard.append(stock[0])
stock.pop(0)
points = 0

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

ans = 'open'

Response = ClientSocket.recv(1024)
while ans != 'exit':
    ans = input('\nEnter a command:')
    #will check if any of the commands were used
    if ans == 'query games' or ans == 'query players':
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:12] == 'de-register ':
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:9] =='register ':
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:4] == 'end ':
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    elif ans[0:11] == 'start game ':
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
        if(Response == 'SUCCESS'):
            inGame = 2
    elif ans == "join game":
        #if not currently in game
        ClientSocket.send(str.encode(ans))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
        inGame = Response
    elif inGame == 1 or inGame == 2:#player
        print('Welcome to game')
        while inGame == 1 or inGame == 2:
            response = ClientSocket.recv(1024)
            decodedResp = response.decode('utf-8')
            for i in cards:
                #display if visible
                if i == 2:
                    print('\n')
                if i < visibleCards:
                    #print
                    print(cards[i])
                else:
                    print(' *** ')
                #do not display and instead print ***
            if visibleCards == 6:
                print('All card are turned, turn is passed')
                if(inGame == 2):
                    ClientSocket.send(str.encode('end'))
            elif decodedResp[0:10] == 'recvcards ':
                decodedResp.split(' ')#add cards to curr card list
                decodedResp.remove('recvcards')
                cards = decodedResp
            elif decodedResp == 'your turn':
                ans = input('\nEnter game command: ')#ask user for their input
                cmdsend = ans + cards[5]#face down card if any
                cards.pop(5)
                ClientSocket.send(str.encode(cmdsend))#send the command
                visibleCards += 1
                if ans == 'stock':
                    response = ClientSocket.recv(1024)
                    decodedResp = response.decode('utf-8')
                    cards.insert[visibleCards-1,decodedResp]
                elif ans[0:6] == 'steal ':
                    response = ClientSocket.recv(1024)
                    decodedResp = response.decode('utf-8')
                    cards.insert[visibleCards-1,decodedResp]
                elif ans == 'discard':
                    response = ClientSocket.recv(1024)
                    decodedResp = response.decode('utf-8')
                    cards.insert[visibleCards-1,decodedResp]
            elif decodedResp[0:10] == 'stockCard ':
                #dealer gets sent card to put in discard and sends card from stock
                newdis = decodedResp.split(' ')
                newdis.remove('stockCard')
                discard.insert[0,newdis]
                stkcrd = stock[0]
                stock.pop(0)
                ClientSocket.send(str.encode(stkcrd))
            elif decodedResp[0:12] == 'discardCard ':
                #dealer gets sent card to put in discard and sends card from discard
                newdis = decodedResp.split(' ')
                newdis.remove('discardCard')
                discard.insert[0,newdis]
                discrd = discard[0]
                discard.pop(0)
                ClientSocket.send(str.encode(discrd))
            elif decodedResp == 'sixcard':#dealer sends starting six card
                newcrd = 'recvcards'
                for x in range(0, 6):
                    newcrd = newcrd + ' ' + cards[x]
                ClientSocket.send(str.encode(newcrd))
            elif decodedResp[0:10] == 'stealcard ':#someone is stealing your card
                #give your card and replace with the card in steal card
                newcard = decodedResp.split(' ')
                newcard.remove('stealcard')
                sendcard = cards[0]
                cards.pop(0)
                cards.insert[0,newcard]
                ClientSocket.send(str.encode(sendcard))
            elif decodedResp == 'end'or decodedResp == 'exit':
                break
        
    elif ans != 'exit':
        print('not a valid command try again')

ClientSocket.close()