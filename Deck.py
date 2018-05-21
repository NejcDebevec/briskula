import Card
import random

class Deck:
    def __init__(self):
        barve = ["Spade", "Coppe", "Bastoni", "Danari"]
        karte = ["As", "Trojka", "Kralj", "Kaval", "Fant", "7", "6", "5", "4", "2"]
        vrednosti = ["11", "10", "4", "3", "2", "0", "0", "0", "0", "0"]
        self.deck = []
        for barva in barve:
            for n in range(len(karte)):
                self.deck.append(Card(karte[n], vrednosti[n], barva))

    def shuffle(self):
        return random.shuffle(self.deck)
    



