class Card:
    def __init__(self,card, value, color, power):
        self.card = card
        self.value = value
        self.color = color
        self.power = power

    def __repr__(self):
        return str(self.card + " " + self.color)

    # def __lt__(self, other):
    #     return self.