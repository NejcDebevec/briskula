class Card:
    def __init__(self,card, value, color):
        self.card = card
        self.value = value
        self.color = color

    def __repr__(self):
        return (self.card + " " + self.color)