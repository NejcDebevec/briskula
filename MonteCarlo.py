import copy

from Node import Node
from State2 import State2
from random import randint
import random
import Heuristics as heur
from math import *

class MonteCarlo:
    def __init__(self, gameManager,turn):
        self.start = 0
        self.GM = gameManager
        self.comp = gameManager.computer
        self.player = gameManager.player
        self.main_card = gameManager.main_card
        # true if computer turn
        self.turn = turn
        self.deck = gameManager.deck

    def start_mc(self, player_played = None):
        root = Node(self.GM)

        for i,move in enumerate(self.comp.current_cards):
            c = 0
            parent = root
            while(True):
                print(c)
                c+=1

                GMcopy = copy.deepcopy(parent.state)
                if c == 1:
                    comp_card = GMcopy.computer.throw_card(i + 1)
                    if player_played:
                        player_card = player_played
                    else:
                        player_card = GMcopy.player.throw_card(
                            random.choice([i + 1 for i in range(len(GMcopy.player.current_cards))]))
                else:
                    player_card = GMcopy.player.throw_card(
                        random.choice([i + 1 for i in range(len(GMcopy.player.current_cards))]))

                    comp_card = GMcopy.computer.throw_card(random.choice([i+1 for i in range(len(GMcopy.computer.current_cards))]))




                if (self.turn):
                    winner = heur.check_cards(comp_card, player_card, GMcopy.main_card)
                else:
                    winner = heur.check_cards(player_card,comp_card,GMcopy.main_card)

                #computer wins
                if((winner and self.turn) or (not winner and not self.turn)):
                    GMcopy.computer.add_to_loot(comp_card, player_card)
                    GMcopy.first = GMcopy.computer
                    GMcopy.second = GMcopy.player
                    self.turn = True
                else:
                    GMcopy.player.add_to_loot(comp_card, player_card)
                    GMcopy.second = GMcopy.computer
                    GMcopy.first = GMcopy.player
                    self.turn = False


                GMcopy.used_cards.append(comp_card)
                GMcopy.used_cards.append(player_card)

                if GMcopy.deck.check_if_deck_empty() is False:
                    card1, card2 = GMcopy.deck.deal_cards_on_turn()
                    GMcopy.computer.pick_up_card(card1)
                    GMcopy.player.pick_up_card(card2)

                child = Node(GMcopy, parent)
                parent.add_child(child)
                if c == 17:
                    print(1)
                if GMcopy.second.check_hand():
                    self.backpropagate(child)
                    break
                parent = child



        pass

    def backpropagate(self,node):
        score = True if node.state.computer.score > node.state.player.score else False
        while node != None:  # backpropagate from the expanded node and work back to the root node
            if (node.parent != None):
                node.update(score)  # state is terminal. Update node with result from POV of node.player_na_potezu
            else:
                node.update(score)
            node = node.parent


    def check_moves(self):
        # print("pride")
        root = Node(State2(self.comp, self.player, None))
        for move in root.state.comp.current_cards:
            child = Node(State2(self.comp, self.player, move), root)
            root.add_child(child)

        # print(root.children)

        for a in range(1000):
            node = random.choice(root.children)
            print(node.state.move)
            if len(self.player.current_cards)<3:
                node.visits += 1
                if self.random_game(node.state.move, self.turn, True):
                    node.wins += 1

            else:
                node.visits += 1
                if self.random_game(node.state.move, self.turn):
                    node.wins += 1

        for child in root.children:
            print(child.wins)

            # print(a)

    def random_game(self, move, turn, leftOver = False):
        main_card = self.main_card
        deck = self.deck
        if leftOver:
            card1_playing = self.player.card_down
            card2_playing = move
            if heur.check_cards(card1_playing, card2_playing, main_card):
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

            if heur.check_cards(card1_playing, card2_playing):
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

    def update(self):
        return 0

    def expansion(self):
        return 0

    def simulation(self):
        return 0

    def selection(self):
        return 0