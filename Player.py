import Deck

class Player:
    def __init__(self, deck, name):
        self.name = name
        self.deck = deck
        self.cards_collected = []
        self.score = 0
        self.current_cards = []

    def __str__(self):
        print(self.name)

    def pickUp_card(self):
        self.current_cards.append("")

    def add_to_loot(self, card1, card2):
        self.cards_collected.append(card1)
        self.cards_collected.append(card2)

    def count_score(self):
        for card in self.cards_collected:
            self.score += card.value
        return self.score

    def set_cards(self, cards):
        self.current_cards = cards

    def throw_card(self, n):
        return self.current_cards.pop(n)






