from Card import Card
import Heuristics as heur
class MinMaxNode:
    def __init__(self,card,c_options,p_options,win,parent = None):
        self.value = None
        self.card = card
        self.c_options = c_options
        self.p_options = p_options
        self.parent = parent
        self.children = []
        self.win = win



class MinMax:

    def __init__(self,p_cards,c_cards,main_card,turn = None):
        self.player_cards = p_cards
        self.computer_cards = c_cards
        self.turn = turn
        self.main_card = main_card
        if turn:
            self.first_cards = p_cards
            self.second_cards = c_cards
            self.build(turn)
        else:
            self.first_cards = c_cards
            self.second_cards = p_cards
            self.build()

    def find_card(self,card):
        for x in self.tree.children:
            if x.card.color == card.color and x.card.power == card.power:
                return x

    def update(self,card):
        self.tree = self.find_card(card)

    def enemy_move(self,card):
        self.tree = self.find_card(card)

    def find_best(self):
        for x in self.tree.children:
            if x.value == self.tree.value:
                self.tree = x
                return x

    def build(self,card_down = None):
        root = MinMaxNode(None, self.first_cards, self.second_cards, True)
        last_level_nodes = []
        if card_down:
            self.first_cards.append(card_down)

        #prva karta - prvi krog
        for card in self.first_cards:

            first_cards_left = self.first_cards[:]
            second_cards_left = self.second_cards[:]

            first_cards_left.pop(first_cards_left.index(card))
            n = MinMaxNode(card, first_cards_left, second_cards_left, True, root)
            root.children.append(n)
            #druga karta - prvi krog
            for card_1 in self.second_cards:
                second_cards_left_1 = second_cards_left[:]
                second_cards_left_1.pop(second_cards_left_1.index(card_1))
                # vrednost prvega kroga
                val1 = get_value(card, card_1)
                turn_winner = heur.check_cards(card,card_1,self.main_card)

                if(turn_winner):
                    turn_1_winner_cards = first_cards_left
                    turn_1_loser_cards = second_cards_left_1

                else:
                    turn_1_winner_cards = second_cards_left_1
                    turn_1_loser_cards = first_cards_left

                # shrani kdo je zmagal v zgodovini in koliko točk je dobil računalnik
                if (not card_down and not turn_winner) or (card_down and turn_winner):
                    computer_level_winner = [True]
                    computer_values = [val1]
                else:
                    computer_level_winner = [False]
                    computer_values = [-val1]
                if computer_level_winner[0]:
                    n_1 = MinMaxNode(card_1, turn_1_winner_cards, turn_1_loser_cards, computer_level_winner[0], n)
                else:
                    n_1 = MinMaxNode(card_1, turn_1_loser_cards, turn_1_winner_cards, computer_level_winner[0], n)
                n.children.append(n_1)

                for card_2 in turn_1_winner_cards:
                    turn_1_winner_cards_2 = turn_1_winner_cards[:]
                    turn_1_winner_cards_2.pop(turn_1_winner_cards_2.index(card_2))

                    #preveri če je komp zmagal ali ne
                    if (computer_level_winner[0]):
                        n_2 = MinMaxNode(card_2, turn_1_winner_cards_2, turn_1_loser_cards, computer_level_winner[0], n_1)
                    else:
                        n_2 = MinMaxNode(card_2, turn_1_loser_cards, turn_1_winner_cards_2, computer_level_winner[0], n_1)
                    n_1.children.append(n_2)


                    for card_3 in turn_1_loser_cards:
                        turn_1_loser_cards_3 = turn_1_loser_cards[:]
                        turn_1_loser_cards_3.pop(turn_1_loser_cards_3.index(card_3))
                        computer_level_winner_2 = computer_level_winner[::]
                        computer_values_2 = computer_values[::]
                        # Shrani če je v drugem krogu zmagal računalnik in koliko točk je dobil
                        val2 = get_value(card_2, card_3)
                        turn_winner_1 = heur.check_cards(card_2, card_3, self.main_card)

                        if (not computer_level_winner[0] and not turn_winner_1) or (computer_level_winner[0] and turn_winner_1):
                            computer_level_winner_2.append(True)
                            computer_values_2.append(int(val2))
                        else:
                            computer_level_winner_2.append(False)
                            computer_values_2.append(-int(val2))


                        if(computer_level_winner_2[1]):
                            n_3 = MinMaxNode(card_3, turn_1_winner_cards_2, turn_1_loser_cards_3, turn_winner_1, n_2)
                            turn_winner_2 = heur.check_cards(turn_1_winner_cards_2[0], turn_1_loser_cards_3[0],
                                                             self.main_card)
                        else:
                            n_3 = MinMaxNode(card_3, turn_1_loser_cards_3, turn_1_winner_cards_2, turn_winner_1,n_2)
                            turn_winner_2 = heur.check_cards(turn_1_loser_cards_3[0], turn_1_winner_cards_2[0],
                                                             self.main_card)

                        n_2.children.append(n_3)

                        val3 = int(get_value(turn_1_loser_cards_3[0], turn_1_winner_cards_2[0]))

                        if (not computer_level_winner_2[1] and not turn_winner_2) or (
                                computer_level_winner_2[1] and turn_winner_2):
                            computer_level_winner_2.append(True)
                            computer_values_2.append(val3)
                        else:
                            computer_level_winner_2.append(False)
                            computer_values_2.append(-val3)


                        n_3.value = int(sum(computer_values_2))
                        last_level_nodes.append(n_3)
        if card_down:
            self.doMiniMax(last_level_nodes, True, 4)
        else:
            self.doMiniMax(last_level_nodes, False, 4)
        self.tree = root
        if self.turn:
            self.enemy_move(self.turn)
            self.first_cards.pop(len(self.first_cards)-1)
        print("")

    def doMiniMax(self,last, minOrMax, depth = 4):
        if minOrMax:
            # if minOrMax true find min value else look for max val
            pass
        for i in range(depth):
            parents = []
            if i >= 2:
                elements_list = list(zip(last,last[1:],last[2:]))[::3]
            else:
                elements_list = list(zip(last, last[1:]))[::2]
            for pair in elements_list:
                parent = pair[0].parent
                if (parent.win and i%2==1) or (not parent.win and i%2==0):
                    parent.value = max(pair[0].value, pair[1].value)
                    if len(pair) == 3:
                        parent.value = max(pair[0].value, pair[1].value,pair[2].value)
                else:
                    parent.value = min(pair[0].value, pair[1].value)
                    if len(pair) == 3:
                        parent.value = min(pair[0].value, pair[1].value, pair[2].value)

                parents.append(parent)
                last = parents



def get_value(c1,c2):
    return int(c1.value + c2.value)

#mm = MinMax([Card("3",10,"Denar",9),Card("5",0,"Kopa",3),Card("12",3,"Bašton",7)],[Card("3",10,"Bašton",9),Card("7",0,"Špada",5),Card("11",2,"Bašton",6)],Card("2",0,"Kopa",1))
# mm = MinMax([Card("5",0,"Kopa",3),Card("11",2,"Špada",6)],[Card("3",10,"Denar",9),Card("2",0,"Špada",5),Card("13",4,"Kopa",8)],Card("11",0,"Špada",1),Card("3",10,"Kopa",9))
# best = mm.find_best()
# best2 = mm.find_best()
# mm.enemy_move(Card("12",3,"Bašton",7))
#
#
# # Find_best poišče najboljšo za komp
# # Enemy_move naredi move enemyja
# # Če je enemy začel prvi krog(torej krogi so trije), je že vrgel karto, kar pomeni, da je to treba zapisati v tretji atribut classa MinMax
# # Z izpisom končnega rezultata treh krogov se nisem zajebaval, ker tega itak ne rabmo
# print(mm.tree.value)