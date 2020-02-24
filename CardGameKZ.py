# Mostly done by Kevin Zhu (asked for help in removing a few errors).

# This program hides the cards of human player 1 from human player 2 and vice versa so that multiple people can play on the same computer.

# The rules are at this link: https://en.wikipedia.org/wiki/Winner_(card_game)
# You can only play 1,2,3,4 of a kind. I did not implement straights or full houses, etc.

import random

def clear():
    print('\n' * 77)

from functools import total_ordering

@total_ordering
class Card:

    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self, name):
        self.name = name
        if name in Card.ranks:
            self.rank = Card.ranks.index(name)

    def __str__(self):
        return self.name
    
    
    def __gt__(self, other):

        return self.rank > other.rank

    def __eq__(self, other):
        return self.name == other.name

class Player:
    def __init__(self,name):
        self.hand = []
        self.name = name

    def __eq__(self, other):
        return self.name == other.name                                                                                                                                                                                                                                                                                                                                                                                                                                      
    
    def getHandString(self):
        string = ''
        for card in self.hand:
            string += (str(card) + ', ')
        return string

    def addCard(self, card):
        self.hand.append(card)

    def getName(self):
        return self.name

    def getHand(self):
        return self.hand

    def sortHand(self):
        self.hand.sort()

    def getAmountInHand(self, name):
        count = 0
        namedCard = Card(name)
        for card in self.hand:
            if card == namedCard:
                count += 1
        return count


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def takeTurn(self,pile):
        self.sortHand()
        print('It is ' + self.name + "'s turn.")
        input('Press Enter when you are ready.')
        if pile.getPlayer() == self:
            pile.clear()
            print('No one beat your cards. The pile is cleared.')
        print('Your hand is: ' + self.getHandString())
        if pile.getAmount() == 0:
            print('The pile is empty.')
        elif pile.getAmount() == 1:
            print('The pile is one ' + pile.getCardName() + '.')
        else:
            print('The pile is ' + str(pile.getAmount()) +
                  ' ' + pile.getCardName() + 's. ')
        passTurn = input('Do you want to pass the turn? (Y/N?)')
        if passTurn == ('Y') or passTurn == ('y'):
            summary = (self.name + ' passed the turn.')
        else:
            summary = self.playCards(pile)
        clear()
        print(summary)

    def playCards(self,pile):
        amount = 0
        passedTurn = False
        name = ''
        if pile.getAmount() == 0:
            while True:
                userString = input('Play how many cards? ')
                if userString.isnumeric():
                    amount = int(userString)
                else:
                    print('YOU must enter a legal number from 1 to 4!')
                    continue
                name = input('Play which card? Type "pass" to pass: ')
                if name == 'pass':
                    passedTurn = True
                    break
                elif not name in Card.ranks:
                    print('ENTER a correct card NAME.')
                    continue
                elif amount > self.getAmountInHand(name):
                    print('You do not have enough of that card in your hand.')
                else:
                    break
        else:
            while True:
                amount = pile.getAmount()
                name = input('Play which card? Type "pass" to pass: ')
                if name == 'pass':
                    passedTurn = True
                    break
                elif not name in Card.ranks:
                    print('ENTER a correct card NAME.')
                    continue
                if Card(name) <= Card(pile.getCardName()):
                    print('That card does not beat the current pile.')
                elif amount > self.getAmountInHand(name):
                    print('You do not have enough of that card in your hand.')
                else:
                    break
                
        if passedTurn == True:
            return self.name + ' passed the turn.'

        for i in range(amount):
            self.hand.remove(Card(name))
        pile.setCardName(name)
        pile.setAmount(amount)
        pile.setPlayer(self)

        
            
        
        return self.name + ' played ' + str(amount) + ' ' + name + ' cards.'
        

class RoboPlayer(Player):

    def __str__(self):
        return ('Robot ' + self.name)

    def takeTurn(self,pile):
        self.sortHand()
        if pile.getPlayer() == self:
            pile.clear()
            print('No one beat the cards of ' + self.getName() + '. The pile is cleared.')

        summary = self.playCards(pile)
        print(summary)

    def playCards(self,pile):
        amount = 0
        if pile.getAmount() == 0:
            played = self.hand.pop(0)
            name = str(played)
            amount = 1
            while len(self.hand) > 0:
                if played == self.hand[0]:
                    played = self.hand.pop(0)
                    amount += 1
                else:
                    break
        else:
            found = False
            choice = None
            for card in self.hand:
                if found == False:
                    if card > Card(pile.getCardName()):
                        if pile.getAmount() <= self.getAmountInHand(str(card)):
                            found = True
                            choice = card
                            amount = pile.getAmount()
            if found == False:
                return self.name + ' passed the turn.'
            for i in range(amount):
                self.hand.remove(choice)
            name = str(choice)
        pile.setCardName(name)
        pile.setAmount(amount)
        pile.setPlayer(self)
        
        return self.name + ' played ' + str(amount) + ' ' + name + ' cards.'

class Deck:

    def __init__(self):
        self.deck = []
    
        for rank in Card.ranks:
            for i in range(4):
                self.deck.append(Card(rank))

    def dealCard(self,player):
        if len(self.deck) > 0:
            player.addCard(self.deck.pop(random.randint(0, len(self.deck) - 1)))

class Pile:

    def __init__(self):
        self.card = ""
        self.amount = 0
        self.player = Player('')

    def __str__(self):
        return('There are ' + str(self.amount) + ' ' + str(self.card) + 's.')

    def getAmount(self):
        return self.amount

    def setAmount(self, value):
        self.amount = value

    def getCardName(self):
        return self.card
    
    def setCardName(self, value):
        self.card = value

    def setPlayer(self, value):
        self.player = value

    def getPlayer(self):
        return self.player

    def clear(self):
        self.card = ""
        self.amount = 0
        self.player = Player('')
    

def beginGame():
    deck = Deck()
    
    playerList = []

    pile = Pile()
    while True:
        numPlayersString = input('How many human players? (0-4) ')
        if numPlayersString.isnumeric():
            numPlayers = int(numPlayersString)
            if 0 <= numPlayers <= 4:
                break
            else:
                print('Between 0 and 4.')
        else:
            print('Type a number.')
    for i in range(numPlayers):
        while True:
            name = input('What is the name of player ' + str(i + 1) + '? ')
            if name == '':
                print('A player name cannot be blank.')
            elif HumanPlayer(name) in playerList:
                print('Someone already has that name in this GAME.')
            else:
                playerList.append(HumanPlayer(name))
                break


                
            
    for i in range(4):
        if len(playerList) >= 4:
            break
        playerList.append(RoboPlayer('Robot ' + 'ABCD'[i]))
    
    for i in range(13):
        for player in playerList:
            deck.dealCard(player)
        
    places = ['First', 'Second','Third','Fourth']
    n = 0
    while True:
        if len(playerList) >= 2:
            endThis = False
            toDelete = []
            while True:
                if endThis == True:
                    for i in toDelete:
                        playerList.remove(i)
                    toDelete = []
                    endThis == False
                    break
                for player in playerList:
                    if len(player.getHand()) > 0:
                        player.takeTurn(pile)
                    if len(player.getHand()) == 0:
                        print(player.getName() + ' gets ' + places[n] + ' Place! ')
                        n += 1
                        endThis = True
                        toDelete.append(player)
                        pile.clear()
                        
                        
        else:
            if len(playerList) > 0 and n < 4:
                for player in playerList:
                    print(player.getName() + ' gets ' + places[n] + ' Place! ')
            break

    print('Game Over')

def main():
    beginGame()
main()