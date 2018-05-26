class Node:
    def __init__(self, state, parent=None):
        self.visits = 1
        self.value = 0.0
        self.wins = 0
        self.state = state
        self.children = []
        self.parent = parent
        self.turn = 0

    def visited(self):
        self.visits += 1

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, value, win):
        self.value += value
        self.visits += 1
        if win:
            self.wins +=1