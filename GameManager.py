from Player import Player
from Deck import Deck


class GameManager:
    def __init__(self):
        self.deck = Deck()
        self.player1 = Player(self.deck, "Player1")
        self.player2 = Player(self.deck, "Player2")

    def game(self):
        self.deal_cards()
        main_card = self.deck.get_first_card()
        first = self.player1
        second = self.player2
        while True:
            player1_pick = input("It's "+first.name+" turn to play,\n(Main card is "+str(main_card)+") select number from 1 to 3,\n"
                                            +str(first.current_cards) +" \nwhich card in deck you want to play: ")
            card1_playing = first.throw_card(int(player1_pick))
            print(card1_playing)
            player2_pick = input("It's "+second.name+" turn to play,\n(Main card is "+str(main_card)+") select number from 1 to 3,\n"
                                                                                + str(second.current_cards)+"\n which card in deck you want to play: ")
            card2_playing = second.throw_card(int(player2_pick))
            print(card2_playing)
            if card1_playing.color == main_card.color and card2_playing.color != main_card.color:
                print(first.name+" win the turn.")
                first.add_to_loot(card1_playing, card2_playing)
                print(first.count_score()+"\n\n")

            elif card1_playing.color != main_card.color and card2_playing.color == main_card.color:
                print(second.name + " win the turn.")
                second.add_to_loot(card1_playing, card2_playing)
                print(second.count_score()+"\n\n")

                tmp = first
                first = second
                second = tmp

            elif card1_playing.color == main_card.color and card2_playing.color == main_card.color:
                if card1_playing.power > card2_playing.power:
                    print(first.name + " win the turn.")
                    first.add_to_loot(card1_playing, card2_playing)
                    print(first.count_score() + "\n\n")

                elif card1_playing.power < card2_playing.power:
                    print(second.name + " win the turn.")
                    second.add_to_loot(card1_playing, card2_playing)
                    print(second.count_score() + "\n\n")

                    tmp = first
                    first = second
                    second = tmp

            elif card1_playing.color != main_card.color and card2_playing.color != main_card.color:
                if card1_playing.color != card2_playing.color:
                    print(first.name + " win the turn.")
                    first.add_to_loot(card1_playing, card2_playing)
                    print(first.count_score() + "\n\n")

                elif card1_playing.color == card2_playing.color:
                    if card1_playing.power > card2_playing.power:
                        print(first.name + " win the turn.")
                        first.add_to_loot(card1_playing, card2_playing)
                        print(first.count_score() + "\n\n")

                    elif card1_playing.power < card2_playing.power:
                        print(second.name + " win the turn.")
                        second.add_to_loot(card1_playing, card2_playing)
                        print(second.count_score() + "\n\n")

                        tmp = first
                        first = second
                        second = tmp

            if self.deck.check_if_deck_empty() is False:
                card1, card2 = self.deck.deal_cards_on_turn()
                first.pick_up_card(card1)
                second.pick_up_card(card2)
            if second.check_hand():
                break

        print("\n\n")
        print(first.name +" has collected "+ first.count_score()+" points.")
        print(second.name + " has collected " + second.count_score() + " points.")
        print("\n")

        if first.score > second.score:
            print(first.name+" has won the game because he collected more points!")
        elif first.score < second.score:
            print(second.name + " has won the game because he collected more points!")
        else:
            print("Game has finished with tied score!")

    def deal_cards(self):
        first, second = self.deck.deal_cards()
        self.player1.set_cards(first)
        self.player2.set_cards(second)


game = GameManager()

game.game()

# print(game.player1.current_cards)