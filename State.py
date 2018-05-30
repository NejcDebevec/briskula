from Node import Node

class State(Node):
    def __init__(self, comp, player, move):
        Node.__init__(self)
        self.move = move
        self.comp = comp
        self.player = player