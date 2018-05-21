import Player
import Deck


class GameManager:
    def __init__(self):
        self.deck = Deck()
        self.player1 = Player(self.deck, "Player1")
        self.player2 = Player(self.deck, "Player2")

    # def deal_cards(self):
    #     self.deck
