import Deck

class Player:
    def __init__(self, deck):
        self.deck = deck
        self.cards_collected = []
        self.score = 0
        self.current_cards = []

    def pickUp_card(self):
        self.current_cards.append("")

    def add_to_loot(self, card1, card2):
        self.cards_collected.append(card1)
        self.cards_collected.append(card2)

    def count_score(self):
        for card in self.cards_collected:
            self.score += card.value
        return self.score



