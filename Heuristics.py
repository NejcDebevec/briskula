def better_cards_in_game(used_card, used_cards, player_cards, all_cards, main_card):
    counter = 0

    for card in all_cards:
        if card in used_cards:
            continue
        elif card in player_cards:
            continue
        else:
            if card.color == main_card.color:
                if used_card.color != main_card.color:
                    counter += 1
                elif used_card.color == card.color and used_card.power < card.power:
                    counter += 1
            elif card.color == used_card.color:
                if card.power > used_card.power:
                    counter +=1

    print(used_card, counter, main_card)

def check_main_power(used_card, used_cards, player_cards, all_cards):
    all = 0
    print(player_cards)
    for card in used_cards:
        if card.color == used_card.color:
            if card.power> used_card.power:
                all += 1
    for card in player_cards:
        if card.value != used_card.value:
            if card.color == used_card.color:
                if card.power > used_card.power:
                    all += 1
    print(all)

def check_cards(card1_playing, card2_playing, main_card):
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