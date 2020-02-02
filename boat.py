import heapq


class BoatState: 

    def __init__(self):
        self.left = True  # true if the boat is at the left bank
        self.msame = 3    # missionaries on the same bank as the boat
        self.csame = 3    # cannibals on the same bank as the boat
        self.mboat = 0    # missionaries in the boat
        self.cboat = 0    # cannibals in the boat
        self.mdiff = 0    # missionaries on the bank opposite from the boat
        self.cdiff = 0    # cannibals on the bank opposite from the boat

    # all validity checks are performed here, not in result()
    def actions(self):
        def okay(m, c):
            if m == 0:
                return True
            else:
                return m >= c
        to_return = []
        if self.mboat + self.cboat >= 1 and okay(self.mdiff + self.mboat, self.cdiff + self.cboat):
            to_return.append('move and offload')
        for i in [1, 2]:
            if i <= self.msame and self.mboat + self.cboat + i <= 2 and okay(self.msame - i, self.csame):
                to_return.append('onload ' + str(i) + 'M')
        for i in [1, 2]:
            if i <= self.csame and self.mboat + self.cboat + i <= 2 and okay(self.mboat, self.cboat + i):
                to_return.append('onload ' + str(i) + 'C')
        for i in [1, 2]:
            if i <= self.mboat and okay(self.mboat - i, self.csame):
                to_return.append('offload ' + str(i) + 'M')
        for i in [1, 2]:
            if i <= self.cboat and okay(self.msame, self.csame + i):
                to_return.append('offload ' + str(i) + 'C')
        return to_return

    def result(self, action):
        new_state = BoatState()
        if action == 'move and offload':
            new_state.left = not self.left
            new_state.msame = self.mdiff + self.mboat
            new_state.csame = self.cdiff + self.cboat
            new_state.mboat = 0
            new_state.cboat = 0
            new_state.mdiff = 3 - new_state.msame
            new_state.cdiff = 3 - new_state.csame
        elif action[1] == 'n' and action[-1] == 'M':
            i = int(action[-2])
            new_state.left = self.left
            new_state.msame = self.msame - i
            new_state.csame = self.csame
            new_state.mboat = self.mboat + i
            new_state.cboat = self.cboat
            new_state.mdiff = self.mdiff
            new_state.cdiff = self.cdiff
        elif action[1] == 'n' and action[-1] == 'C':
            i = int(action[-2])
            new_state.left = self.left
            new_state.msame = self.msame
            new_state.csame = self.csame - i
            new_state.mboat = self.mboat
            new_state.cboat = self.cboat + i
            new_state.mdiff = self.mdiff
            new_state.cdiff = self.cdiff
        elif action[1] == 'f' and action[-1] == 'M':
            i = int(action[-2])
            new_state.left = self.left
            new_state.msame = self.msame + i
            new_state.csame = self.csame
            new_state.mboat = self.mboat - i
            new_state.cboat = self.cboat
            new_state.mdiff = self.mdiff
            new_state.cdiff = self.cdiff
        elif action[1] == 'f' and action[-1] == 'C':
            i = int(action[-2])
            new_state.left = self.left
            new_state.msame = self.msame
            new_state.csame = self.csame + i
            new_state.mboat = self.mboat
            new_state.cboat = self.cboat - i
            new_state.mdiff = self.mdiff
            new_state.cdiff = self.cdiff
        return new_state

    def __str__(self):
        if self.left:
            left = ('M' * self.msame) + ('C' * self.csame)
            boat = ('M' * self.mboat) + ('C' * self.cboat)
            right = ('M' * self.mdiff) + ('C' * self.cdiff)
            return left.rjust(6) + '|' + boat.ljust(4) + '|' + right.ljust(6)
        else:
            left = ('M' * self.mdiff) + ('C' * self.cdiff)
            boat = ('M' * self.mboat) + ('C' * self.cboat)
            right = ('M' * self.msame) + ('C' * self.csame)
            return left.rjust(6) + '|' + boat.rjust(4) + '|' + right.ljust(6)


class Node:

    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


# returns the child formed by parent as a result of action
def child(parent, action):
    if action == 'move and offload':
        return Node(parent.state.result(action), parent, action, parent.path_cost + 1)
    else:
        return Node(parent.state.result(action), parent, action, parent.path_cost)


# returns the last node on an optimal path found by uniform-cost graph search
def UCS():

    def push(h, node, n):
        heapq.heappush(h, (node.path_cost, n, node))
    def pop(h):
        return heapq.heappop(h)[2]
    def tup(state):
        return (int(state.left), state.msame, state.csame, state.mboat, state.cboat, state.mdiff, state.cdiff)
    def goal(state):
        return tup(state) == (0, 3, 3, 0, 0, 0, 0)

    explored = set()  # add tuplized versions of boat states to this so equality check is easy
    counter = 0
    h = []

    start = Node(BoatState(), None, None, 0)
    print(start.state)
    push(h, start, counter)
    counter += 1
    while len(h) > 0:
        node = pop(h)
        explored.add(tup(node.state))
        if goal(node.state):
            return node
        else:
            for a in node.state.actions():
                c = child(node, a)
                if tup(c.state) not in explored:
                    push(h, c, counter)
                    counter += 1
            for e in h:
                print(e[2].state, end=' ')
            print()
    return None
