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
