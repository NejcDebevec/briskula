
class State:
    def __init__(self, comp, player):
        self.moves = comp.current_cards
        self.comp = comp
        self.player = player