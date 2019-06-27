import random


class Poker(object):
    def __init__(self):
        self.cards = []
        self.suits = ['hearts', 'spades', 'diamonds', 'clubs']
        self.values = [value for value in range(2, 15)]

    def generate_cards(self):
        for value in self.values:
            for suit in self.suits:
                card = {"value": value, "suit": suit}
                self.cards.append(card)

    def riffle(self):
        random.shuffle(self.cards)

    def send_card(self, amount=1):
        new_cards = []
        for i in range(amount):
            new_cards.append(self.cards.pop())
        return new_cards