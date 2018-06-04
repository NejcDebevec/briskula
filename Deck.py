from Card import Card
import random

class Deck:
    def __init__(self):
        colors = ["Spade", "Coppe", "Bastoni", "Danari"]
        cards = ["As", "Trojka", "Kralj", "Kaval", "Fant", "7", "6", "5", "4", "2"]
        values = ["11", "10", "4", "3", "2", "0", "0", "0", "0", "0"]
        self.deck = []
        self.all_cards= []
        for color in colors:
            for n in range(len(cards)):
                self.deck.append(Card(cards[n], values[n], color, 10-cards.index(cards[n])))
                self.all_cards.append(Card(cards[n], values[n], color, 10-cards.index(cards[n])))
        self.shuffle()

    def get_first_card(self):

        first_card = self.deck.pop(0)
        self.main_color = first_card.color
        self.deck.append(first_card)
        return first_card

    def deal_cards(self):

        player1_cards = [self.deck.pop(0) for _ in range(3)]
        player2_cards = [self.deck.pop(0) for _ in range(3)]

        return (player1_cards, player2_cards)

    def random_shuffle(self):
        main = self.deck.pop(len(self.deck)-1)

        self.deck = random.shuffle(self.deck)
        self.deck.append(main)


    def deal_cards_on_turn(self):

        return (self.deck.pop(0), self.deck.pop(0))

    def shuffle(self):
        random.shuffle(self.deck)

    def check_if_deck_empty(self):
        return True if len(self.deck) == 0 else False

d = Deck()
