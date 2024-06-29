import random

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Deck():
    def __init__(self):
        self.deck = []
        for rank in ranks:
            for suit in suits:
                self.deck.append(f"{rank} of {suit}")
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        rank = card.split()[0]
        self.value += values[rank]
        if rank == "Ace":
            self.aces += 1
        self.adjust()

    def adjust(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


def deal_initial_cards(deck):
    player_hand = Hand()
    dealer_hand = Hand()
    for _ in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
    return player_hand, dealer_hand

