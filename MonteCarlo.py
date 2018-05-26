from Node import Node
from State import State
from random import randint

class MonteCarlo:
    def __init__(self, comp, player, main_card, turn, deck):
        self.start = 0
        self.comp = comp
        self.player = player
        self.main_card = main_card
        self.turn = turn
        self.deck = deck

    def check_moves(self):
        root = Node(State(self.comp, self.player))
        for move in root.state.comp.current_cards:
            child = Node(State(self.comp, self.player), root)
            root.add_child(child)

        print(root.children)
        # root.children = [Node()]
        for a in range(1000):
            if len(self.player.current_cards)<3:
                self.random_game("", self.turn, True)
            else:
                self.random_game("", self.turn, True)

            # print(a)

    def random_game(self, move, turn, leftOver = False):
        main_card = self.main_card
        deck = self.deck
        if leftOver:
            card1_playing = self.player.card_down
            card2_playing = move
            if self.check_cards(card1_playing, card2_playing, main_card):
                turn = 2
            else:
                turn = 1

        if turn == 1:
            first = self.comp
            second = self.player
        else:
            second = self.comp
            first = self.player

        random = move.move
        while True:
            card1_playing = first.throw_card(int(random))

            print(card1_playing)

            player2_pick = randint(1, len(second.current_cards))

            card2_playing = second.throw_card(int(player2_pick))
            print(card2_playing)

            if self.check_cards(card1_playing, card2_playing):
                first.add_to_loot(card1_playing, card2_playing)
            else:
                second.add_to_loot(card1_playing, card2_playing)
                tmp = first
                first = second
                second = tmp

            if deck.check_if_deck_empty() is False:
                card1, card2 = deck.deal_cards_on_turn()
                first.pick_up_card(card1)
                second.pick_up_card(card2)
            if second.check_hand():
                break
        if first.score > second.score:
            print(first.name+" has won the game because he collected more points!")
        elif first.score < second.score:
            print(second.name + " has won the game because he collected more points!")
        else:
            print("Game has finished with tied score!")

    def check_cards(self, card1_playing, card2_playing, main_card):
        if card1_playing.color == main_card.color and card2_playing.color != main_card.color:
            return True

        elif card1_playing.color != main_card.color and card2_playing.color == main_card.color:
            return False

        elif card1_playing.color == main_card.color and card2_playing.color == main_card.color:
            if card1_playing.power > card2_playing.power:
                return True

            elif card1_playing.power < card2_playing.power:
                return False

        elif card1_playing.color != main_card.color and card2_playing.color != main_card.color:
            if card1_playing.color != card2_playing.color:
                return True

            elif card1_playing.color == card2_playing.color:
                if card1_playing.power > card2_playing.power:
                    return True

                elif card1_playing.power < card2_playing.power:
                    return False

    def update(self):
        return 0

    def expansion(self):
        return 0

    def simulation(self):
        return 0

    def selection(self):
        return 0