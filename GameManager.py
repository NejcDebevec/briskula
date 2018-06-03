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

    def deal_cards(self):
        first, second = self.deck.deal_cards()
        self.player.set_cards(first)
        self.computer.set_cards(second)

    def test(self):
        self.deal_cards()
        main_card = self.deck.get_first_card()

        # for card in self.deck.deck:
        #     print(card)
        card = self.player.current_cards[0]
        # better_cards_in_game(card,self.used_cards,self.player1.current_cards,self.allcards, main_card)
        # print(main_card)
        # check_main_power(main_card,self.used_cards,self.player1.current_cards,self.allcards)

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
                        # else:
                        #     comp = self.second.current_cards
                        #     player = self.first.current_cards
                else:
                    # if len(self.first.current_cards) > 1:
                    card_rand = mc.MC_random(200)
                # else:
                #     card_rand = self.first.current_cards[0]
                # card_rand = mc.MC_random(200)
                index = -1
                for n,card in enumerate(self.first.current_cards):
                    if card.color == card_rand.color:
                        if card.power == card_rand.power:
                            index = n
                        # break

                card1_playing = self.first.throw_card(int(index+1))
                self.first.card_down = card1_playing
                print(card1_playing)

                player2_pick = input("It's " + self.second.name + " turn to play,\n(Main card is " + str(
                    self.main_card) + ") select number from 1 to 3,\n"+str(self.second.current_cards) +" \nwhich card in deck you want to play: ")
                card2_playing = self.second.throw_card(int(player2_pick))
                if mm is not None and self.deck.check_if_deck_empty() and len(self.second.current_cards) != 1:
                    mm.enemy_move(card2_playing)
                print(card2_playing)
                self.second.card_down = card2_playing
            else:
                if self.deck.check_if_deck_empty():
                    print(1)
                player1_pick = input("It's "+self.first.name+" turn to play,\n(Main card is "+str(self.main_card)+") select number from 1 to 3,\n"
                                                +str(self.first.current_cards) +" \nwhich card in deck you want to play: ")
                card1_playing = self.first.throw_card(int(player1_pick))
                self.first.card_down = card1_playing
                print(card1_playing)
                # player2_pick = najdi najboljšo karto za izbrat(poženi montecarlo)
                # player2_pick = mc.start_mc(card1_playing)
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
                # if len(self.second.current_cards) > 1:
                    card_rand = mc.MC_random(200)
                index = -1
                for n, card in enumerate(self.second.current_cards):
                    if card.color == card_rand.color:
                        if card.power == card_rand.power:
                            index = n
                            # break
                # print(card_rand, "card", self.second.current_cards)
                # player2_pick = self.second.current_cards.index(index+1)
                # print(player2_pick)

                card2_playing = self.second.throw_card(int(index+1))
                self.second.card_down = card2_playing

                print(card2_playing)

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

            # if card1_playing.color == main_card.color and card2_playing.color != main_card.color:
            #     print(self.first.name+" win the turn.")
            #     self.first.add_to_loot(card1_playing, card2_playing)
            #     print(self.first.count_score()+"\n\n")
            #
            # elif card1_playing.color != main_card.color and card2_playing.color == main_card.color:
            #     print(second.name + " win the turn.")
            #     second.add_to_loot(card1_playing, card2_playing)
            #     print(second.count_score()+"\n\n")
            #
            #     tmp = self.first
            #     self.first = second
            #     second = tmp
            #
            # elif card1_playing.color == main_card.color and card2_playing.color == main_card.color:
            #     if card1_playing.power > card2_playing.power:
            #         print(self.first.name + " win the turn.")
            #         self.first.add_to_loot(card1_playing, card2_playing)
            #         print(self.first.count_score() + "\n\n")
            #
            #     elif card1_playing.power < card2_playing.power:
            #         print(second.name + " win the turn.")
            #         second.add_to_loot(card1_playing, card2_playing)
            #         print(second.count_score() + "\n\n")
            #
            #         tmp = self.first
            #         self.first = second
            #         second = tmp
            #
            # elif card1_playing.color != main_card.color and card2_playing.color != main_card.color:
            #     if card1_playing.color != card2_playing.color:
            #         print(self.first.name + " win the turn.")
            #         self.first.add_to_loot(card1_playing, card2_playing)
            #         print(self.first.count_score() + "\n\n")
            #
            #     elif card1_playing.color == card2_playing.color:
            #         if card1_playing.power > card2_playing.power:
            #             print(self.first.name + " win the turn.")
            #             self.first.add_to_loot(card1_playing, card2_playing)
            #             print(self.first.count_score() + "\n\n")
            #
            #         elif card1_playing.power < card2_playing.power:
            #             print(second.name + " win the turn.")
            #             second.add_to_loot(card1_playing, card2_playing)
            #             print(second.count_score() + "\n\n")
            #
            #             tmp = self.first
            #             self.first = second
            #             second = tmp
            self.used_cards.append(card1_playing)
            self.used_cards.append(card2_playing)

            if self.deck.check_if_deck_empty() is False:
                card1, card2 = self.deck.deal_cards_on_turn()
                self.first.pick_up_card(card1)
                self.second.pick_up_card(card2)

            if self.second.check_hand():
                break

        print("\n\n")
        print(self.first.name +" has collected "+ self.first.count_score()+" points.")
        print(self.second.name + " has collected " + self.second.count_score() + " points.")
        print("\n")

        if self.first.score > self.second.score:
            print(self.first.name+" has won the game because he collected more points!")
        elif self.first.score < self.second.score:
            print(self.second.name + " has won the game because he collected more points!")
        else:
            print("Game has finished with tied score!")


    # def finish_with_min_max()
    # def random_game(self, move):
    #         self.deal_cards()
    #         main_card = self.deck.get_first_card()
    #         first = self.player1
    #         second = self.player2
    #
    #         random = move.move
    #         while True:
    #             # player1_pick = input("It's " + first.name + " turn to play,\n(Main card is " + str(
    #             #     main_card) + ") select number from 1 to 3,\n"
    #             #                      + str(first.current_cards) + " \nwhich card in deck you want to play: ")
    #             card1_playing = first.throw_card(int(random))
    #
    #             print(card1_playing)
    #             # player2_pick = input("It's " + second.name + " turn to play,\n(Main card is " + str(
    #             #     main_card) + ") select number from 1 to 3,\n"
    #             #                      + str(second.current_cards) + "\n which card in deck you want to play: ")
    #
    #             player2_pick = randint(1, len(second.current_cards))
    #
    #             card2_playing = second.throw_card(int(player2_pick))
    #             print(card2_playing)
    #
    #             if card1_playing.color == main_card.color and card2_playing.color != main_card.color:
    #                 print(first.name + " win the turn.")
    #                 first.add_to_loot(card1_playing, card2_playing)
    #                 print(first.count_score() + "\n\n")
    #
    #             elif card1_playing.color != main_card.color and card2_playing.color == main_card.color:
    #                 print(second.name + " win the turn.")
    #                 second.add_to_loot(card1_playing, card2_playing)
    #                 print(second.count_score() + "\n\n")
    #
    #                 tmp = first
    #                 first = second
    #                 second = tmp
    #
    #             elif card1_playing.color == main_card.color and card2_playing.color == main_card.color:
    #                 if card1_playing.power > card2_playing.power:
    #                     print(first.name + " win the turn.")
    #                     first.add_to_loot(card1_playing, card2_playing)
    #                     print(first.count_score() + "\n\n")
    #
    #                 elif card1_playing.power < card2_playing.power:
    #                     print(second.name + " win the turn.")
    #                     second.add_to_loot(card1_playing, card2_playing)
    #                     print(second.count_score() + "\n\n")
    #
    #                     tmp = first
    #                     first = second
    #                     second = tmp
    #
    #             elif card1_playing.color != main_card.color and card2_playing.color != main_card.color:
    #                 if card1_playing.color != card2_playing.color:
    #                     print(first.name + " win the turn.")
    #                     first.add_to_loot(card1_playing, card2_playing)
    #                     print(first.count_score() + "\n\n")
    #
    #                 elif card1_playing.color == card2_playing.color:
    #                     if card1_playing.power > card2_playing.power:
    #                         print(first.name + " win the turn.")
    #                         first.add_to_loot(card1_playing, card2_playing)
    #                         print(first.count_score() + "\n\n")
    #
    #                     elif card1_playing.power < card2_playing.power:
    #                         print(second.name + " win the turn.")
    #                         second.add_to_loot(card1_playing, card2_playing)
    #                         print(second.count_score() + "\n\n")
    #
    #                         tmp = first
    #                         first = second
    #                         second = tmp
    #
    #             if self.deck.check_if_deck_empty() is False:
    #                 card1, card2 = self.deck.deal_cards_on_turn()
    #                 first.pick_up_card(card1)
    #                 second.pick_up_card(card2)
    #             if second.check_hand():
    #                 break


game = GameManager()
game.game()


# print(game.player1.current_cards)