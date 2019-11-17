import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:

    def __init__ (self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def print_cards(self):
        for Card in self.deck:
            print(Card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        cardToDeal = self.deck.pop()
        return cardToDeal
    
    def count_cards(self):
        return print(len(self.deck))

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.value += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.ace:
            self.value -= 10
            self.ace -= 1

class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
         self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Place your bet:'))
        except:
            print('Please enter a valid bet')
        else:
            if chips.bet > chips.total:
                print("Sorry, you don't have enought chips")
            else:
                break

def hits(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):

    global playing

    while True:
        q = input("Would you like to hit or stand? Digit 'h' for hit and s for 'stand'")
        if q.lower() == 'h':
            hits(deck, hand)
        elif q.lower() == 's':
            print('Player stands, dealer is playing')
            playing = False
        else:
            print("Digit 'h' for hit and s for 'stand")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

# GAME
while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    playerHand = Hand()
    dealerHand = Hand()

    playerHand.add_card(deck.deal())
    playerHand.add_card(deck.deal())

    dealerHand.add_card(deck.deal())
    dealerHand.add_card(deck.deal())

    # Set up the Player's chips
    playerChips = Chips()

    # Prompt the player for his bet
    take_bet(playerChips)

    # Show cards (but keep one dealer card hidden)
    show_some(playerHand,dealerHand)

    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, playerHand)

        # Show cards (but keep one dealer card hidden)
        show_some(playerHand,dealerHand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if playerHand.value > 21:
            player_busts(playerHand, dealerHand, playerChips)
            break
        
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if playerHand.value <= 21:
        while dealerHand.value <= 17:
            hits(deck, dealerHand)

        # Show all cards
        show_all(playerHand, dealerHand)

        # Run different winning scenarios
        if dealerHand.value > 21:
            dealer_busts(playerHand, dealerHand, playerChips)
        elif dealerHand.value < playerHand.value:
            player_wins(playerHand, dealerHand, playerChips)
        elif dealerHand.value > playerHand.value:
            dealer_wins(playerHand, dealerHand, playerChips)
        else:
            push(playerHand, dealerHand)

    # Inform Player of their chips total
    print("\nPlayer's winning stand at", playerChips.total)

    #Ask to play again
    continueToPlay = input("Would you like to play again? Digit 'y' for yes or 'n' for no")

    if continueToPlay.lower() == 'y':
        playing = True
        continue

    if continueToPlay.lower() == 'n':
        print('Thanks for playing!')
        break
