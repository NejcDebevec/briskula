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
            while True:
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




                if self.turn:
                    winner = heur.check_cards(comp_card, player_card, GMcopy.main_card)
                else:
                    winner = heur.check_cards(player_card,comp_card,GMcopy.main_card)

                #computer wins
                if (winner and self.turn) or (not winner and not self.turn):
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

    def MC_random(self, iteration):
        root = Node(self.GM, None)
        for i in range(len(self.GM.computer.current_cards)):
            GMcopy = copy.deepcopy(root.state)
            card = GMcopy.computer.throw_card(i+1)
            node = Node(GMcopy, card)
            root.children.append(node)
        # for child in root.children:
        #     print(child.move)
        for itera in range(iteration):
            node = random.choice(root.children)
            # print(node.move)
            node.visits += 1
            state = copy.deepcopy(node.state)
            # print(itera)
            if len(state.player.current_cards) < 3:
                result = self.random_game(state, node.move, self.turn, True)
                if result == 1:
                    node.wins += 1
                elif result == 0:
                    node.wins += 0.5
            else:
                result = self.random_game(state, node.move, self.turn, False)
                if result == 1:
                    node.wins += 1
                elif result == 0:
                    node.wins += 0.5
        # print(iteration)
        results = []
        # if len(root.children)>0:
        for child in root.children:
            results.append(((child.wins/child.visits), child.visits, child.move))
            # print((child.wins/child.visits), child.move))
        print(results)
        result = sorted(results,key=lambda x: x[0], reverse=True)[0]
        # return max(results)[2]
        # return None
        return result[2]

    def backpropagate(self, node):
        score = True if node.state.computer.score > node.state.player.score else False
        while node != None:  # backpropagate from the expanded node and work back to the root node
            if (node.parent != None):
                node.update(score)  # state is terminal. Update node with result from POV of node.player_na_potezu
            else:
                node.update(score)
            node = node.parent


    # def check_moves(self):
    #     # print("pride")
    #     root = Node(State2(self.comp, self.player, None))
    #     for move in root.state.comp.current_cards:
    #         child = Node(State2(self.comp, move, self.player), root)
    #         root.add_child(child)
    #
    #     # print(root.children)
    #
    #     for a in range(1000):
    #         node = random.choice(root.children)
    #         print(node.move)
    #         if len(self.player.current_cards)<3:
    #             node.visits += 1
    #             if self.random_game(node.state,node.move, self.turn, True):
    #                 node.wins += 1
    #
    #         else:
    #             node.visits += 1
    #             if self.random_game(node.state,node.move, self.turn):
    #                 node.wins += 1
    #
    #     for child in root.children:
    #         print(child.wins)

            # print(a)

    def random_game(self, GM, move, turn, leftOver = False):
        # print(len(GM.player.current_cards), len(GM))
        main_card = GM.main_card
        deck = GM.deck
        # print(len(deck.deck))
        if leftOver:
            card1_playing = GM.player.card_down
            card2_playing = move
            # print(len(GM.player.current_cards), "zacetek1")
            # print(len(GM.computer.current_cards), "zacetek2")
            if heur.check_cards(card1_playing, card2_playing, main_card):
                GM.player.add_to_loot(card1_playing, card2_playing)
                turn = 2
                if deck.check_if_deck_empty() is False:
                    card1, card2 = deck.deal_cards_on_turn()
                    GM.player.pick_up_card(card1)
                    GM.computer.pick_up_card(card2)
            else:
                GM.computer.add_to_loot(card1_playing, card2_playing)
                turn = 1
                if deck.check_if_deck_empty() is False:
                    card1, card2 = deck.deal_cards_on_turn()
                    GM.computer.pick_up_card(card1)
                    GM.player.pick_up_card(card2)
            # random = randint(1, len(GM.computer.current_cards))
        if turn == 1:
            first = GM.computer
            second = GM.player
        else:
            second = GM.computer
            first = GM.player
        # if len(first.current_cards) == 0 or len(second.current_cards) == 0:

        first_turn = True
        while True:
            card1_playing = None
            card2_playing = None
            if first_turn:
                first_turn = False
                if turn == 1:
                    card1_playing = move
                    player2_pick = randint(1, len(second.current_cards))
                    card2_playing = second.throw_card(int(player2_pick))
                    # print(card1_playing, card2_playing)
                elif turn == 2:
                    card2_playing = move
                    player1_pick = randint(1, len(first.current_cards))
                    card1_playing = first.throw_card(int(player1_pick))
            else:
                # print(len(first.current_cards), len(second.current_cards))
                player1_pick = randint(1, len(first.current_cards))
                card1_playing = first.throw_card(int(player1_pick))
                # print(card1_playing)
                player2_pick = randint(1, len(second.current_cards))
                # print(player2_pick, len())
                card2_playing = second.throw_card(int(player2_pick))
                # print(card2_playing)

            if heur.check_cards(card1_playing, card2_playing, main_card):
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
            if first.check_hand() or second.check_hand():
                # print("pride")
                # print(deck.check_if_deck_empty())
                # print(len(first.current_cards),"prvi")
                # print(len(second.current_cards), "drugi")
                break

        if first.score > second.score:
            if first.name == 'Computer':
                return 1
            return -1
            # print(first.name+" has won the game because he collected more points!")
        elif first.score < second.score:
            if second.name == 'Computer':
                return 1
            return -1
            # print(second.name + " has won the game because he collected more points!")
        else:
            return 0
            # print("Game has finished with tied score!")

    def update(self):
        return 0

    def expansion(self):
        return 0

    def simulation(self):
        return 0

    def selection(self):
        return 0