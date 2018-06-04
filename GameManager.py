from Player import Player
from Deck import Deck
import random
import Heuristics as heur
import MonteCarlo as MC
from MinMax import MinMax as MM


class GameManager:
    def __init__(self):
        self.deck = Deck()
        self.allcards = self.deck.all_cards
        self.player = Player(self.deck, "Player")
        self.computer = Player(self.deck, "Computer", True)
        self.used_cards = []
        self.iteration = 1500

    def deal_cards(self):
        first, second = self.deck.deal_cards()
        self.player.set_cards(first)
        self.computer.set_cards(second)

    def random_starter(self,f,s):
        i = random.choice([0,1])
        if i == 0:
            return f,s
        return s,f

    def game(self):
        self.deal_cards()
        self.main_card = self.deck.get_first_card()
        self.first, self.second = self.random_starter(self.player,self.computer)
        mm = None
        while True:
            mc = MC.MonteCarlo(self, self.first.isComputer)

            if self.first.isComputer:
                if self.deck.check_if_deck_empty():
                    if mm is None:
                        comp = self.first.current_cards
                        player = self.second.current_cards
                        mm = MM(player, comp, self.main_card)
                        card_rand = mm.find_best().card
                    else:
                        if len(self.first.current_cards) != 1:
                            card_rand = mm.find_best().card
                        else:
                            card_rand = self.first.current_cards[0]

                else:
                    card_rand = mc.MC_random(self.iteration)

                index = -1
                for n,card in enumerate(self.first.current_cards):
                    if card.color == card_rand.color:
                        if card.power == card_rand.power:
                            index = n

                card1_playing = self.first.throw_card(int(index+1))
                self.first.card_down = card1_playing
                print("")
                print(self.first.name+" played: "+str(card1_playing))
                print("")

                player2_pick = input("It's " + self.second.name + " turn to play,\n(Main card is " + str(
                    self.main_card) + ") select number between 1 and "+str(len(self.second.current_cards))+",\n"+str(self.second.current_cards)
                                     + "\nwhich card in deck you want to play: ")
                while int(player2_pick) < 1 or int(player2_pick) > len(self.second.current_cards):
                    print("")
                    player2_pick = input("You have to select number between 1 and "+str(len(self.second.current_cards))+",\n" + str(self.second.current_cards)
                                         + " \nwhich card in deck you want to play: ")
                card2_playing = self.second.throw_card(int(player2_pick))
                if mm is not None and self.deck.check_if_deck_empty() and len(self.second.current_cards) != 1:
                    mm.enemy_move(card2_playing)
                print("")
                print(self.second.name+" played: "+str(card2_playing))
                print("")
                self.second.card_down = card2_playing
            else:

                player1_pick = input("It's "+self.first.name+" turn to play,\n(Main card is "+str(self.main_card)+
                                     ") select number between 1 and "+str(len(self.second.current_cards))+",\n"
                                                +str(self.first.current_cards) +" \nwhich card in deck you want to play: ")
                while int(player1_pick)< 1 or int(player1_pick)>len(self.first.current_cards):
                    print("")
                    player1_pick = input("You have to select number between 1 and "+str(len(self.second.current_cards))+",\n"
                                         + str(self.first.current_cards) + " \nwhich card in deck you want to play: ")

                card1_playing = self.first.throw_card(int(player1_pick))
                self.first.card_down = card1_playing
                print("")
                print(self.first.name + " played: " + str(card1_playing))
                print("")

                if self.deck.check_if_deck_empty():
                    if mm is None:
                            comp = self.second.current_cards
                            player = self.first.current_cards
                            mm = MM(player, comp, self.main_card, card1_playing)
                    else:
                        if len(self.first.current_cards) != 0:
                            mm.enemy_move(card1_playing)

                    if len(self.second.current_cards) != 1:
                        card_rand = mm.find_best().card
                    else:
                        card_rand = self.second.current_cards[0]
                else:
                    card_rand = mc.MC_random(self.iteration)
                index = -1
                for n, card in enumerate(self.second.current_cards):
                    if card.color == card_rand.color:
                        if card.power == card_rand.power:
                            index = n

                card2_playing = self.second.throw_card(int(index+1))
                self.second.card_down = card2_playing

                print("")
                print(self.second.name + " played: " + str(card2_playing))
                print("")

            if heur.check_cards(card1_playing,card2_playing, self.main_card):
                print(self.first.name + " win the turn.")
                self.first.add_to_loot(card1_playing, card2_playing)
                print(self.first.count_score()+"\n\n")
            else:
                print(self.second.name + " win the turn.")
                self.second.add_to_loot(card1_playing, card2_playing)
                print(self.second.count_score()+"\n\n")
                tmp = self.first
                self.first = self.second
                self.second = tmp

            self.used_cards.append(card1_playing)
            self.used_cards.append(card2_playing)

            if self.deck.check_if_deck_empty() is False:
                card1, card2 = self.deck.deal_cards_on_turn()
                self.first.pick_up_card(card1)
                self.second.pick_up_card(card2)

            if self.second.check_hand():
                break

        print("\n\n")
        print(self.first.name + " has collected " + self.first.count_score()+" points.")
        print(self.second.name + " has collected " + self.second.count_score() + " points.")
        print("\n")

        if self.first.score > self.second.score:
            print(self.first.name+" has won the game because he collected more points!")
        elif self.first.score < self.second.score:
            print(self.second.name + " has won the game because he collected more points!")
        else:
            print("Game has finished with tied score!")

game = GameManager()
game.game()


