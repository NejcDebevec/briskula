from math import *
import random


class Node:
    def __init__(self, state, parent=None):
        self.visits = 1
        self.value = 0.0
        self.wins = 0
        self.state = state
        # self.move =
        self.children = []
        self.parent = parent
        self.turn = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.player_on_turn = state.player_na_potezu  # the only part of the state that the Node needs later
        self.points = state.bodovi
        self.player_starts = state.player_na_potezu

    def visited(self):
        self.visits += 1

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, value, win):
        # self.value += value
        self.visits += 1
        if win:
            self.wins += 1

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        maxNode = None
        maxi = -1.0
        mini = 1.1
        minNode = None
        for i in range(len(self.childNodes)):
            if (maxi < float(self.childNodes[i].wins) / float(self.childNodes[i].visits) + 100 * sqrt(
                            1 * log(self.visits) / self.childNodes[i].visits)):
                maxNode = self.childNodes[i]
                maxi = float(self.childNodes[i].wins) / float(self.childNodes[i].visits) + 100 * sqrt(
                    1 * log(self.visits) / self.childNodes[i].visits)
        return maxNode

    def UCT(self, rootstate, itermax, verbose=False, brojac=-1):
        """ Conduct a UCT search for itermax iterations starting from rootstate.
            Return the best move from the rootstate.
            Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

        rootnode = Node(state=rootstate)
        pobjednik = rootstate.pobjednik
        for i in range(itermax):
            node = rootnode
            state = rootstate.Clone()
            j = brojac
            j = brojac
            # Select
            while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
                node = node.UCTSelectChild()
                # print state.print1()+" "+str(node.move)+" select"
                state.DoMove(node.move)

                j += 1

                # Expand
            if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
                m = random.choice(node.untriedMoves)
                # print state.print1()+" "+str(node.move)+" expand "+str(j)
                state.DoMove(m)
                j += 1
                node = node.AddChild(m, state)  # add child and descend tree

            # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
            while state.GetMoves() != []:  # while state is non-terminal
                izbacujem_kartu = random.choice(state.GetMoves())
                # print state.print1()+str(node.move)+" rollout"
                state.DoMove(izbacujem_kartu)
                j += 1

            # Backpropagate
            while node != None:  # backpropagate from the expanded node and work back to the root node
                # print str(node.player_na_potezu)+" je prosao s "+str(state.GetResult(node.player_na_potezu))
                if (node.parentNode != None):
                    node.Update(state.GetResult(
                        node.parentNode.player_na_potezu))  # state is terminal. Update node with result from POV of node.player_na_potezu
                else:
                    node.Update(state.GetResult(1))
                node = node.parentNode

                # print "na kraju iteracije j je "+str(j)

        if (verbose == False): print
        rootnode.TreeToString(0)