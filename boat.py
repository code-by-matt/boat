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

    # push and pop are methods that make using heapq a little easier
    def push(h, node, n):  # we make n always increasing as a way to break ties
        heapq.heappush(h, (node.path_cost, n, node))
    def pop(h):
        return heapq.heappop(h)[2]
    def tup(state):
        return (int(state.left), state.msame, state.csame, state.mboat, state.cboat, state.mdiff, state.cdiff)
    def goal(state):
        return tup(state) == (0, 3, 3, 0, 0, 0, 0)

    # strategy implementation
    h = []  # uses heapq to order frontier nodes by cost
    n = 0   # increment n every time something is pushed

    # checking for duplicates
    explored = set()  # stores tuplized states of already expanded nodes
    frontier = set()  # stores tuplized states of nodes in the frontier

    start = Node(BoatState(), None, None, 0)
    print(start.state)
    push(h, start, n)
    n += 1
    frontier.add(tup(start.state))
    while len(h) > 0:
        node = pop(h)
        frontier.remove(tup(node.state))
        explored.add(tup(node.state))
        if goal(node.state):
            to_return = []
            curr = node
            while curr.action != None:
                to_return.append(curr.action)
                curr = curr.parent
            return to_return[::-1]
        else:
            for a in node.state.actions():
                c = child(node, a)
                if tup(c.state) not in explored and tup(c.state) not in frontier:
                    push(h, c, n)
                    n += 1
                    frontier.add(tup(c.state))
            # print the frontier; first thing printed is next to be expanded
            for e in h:
                print(e[2].state, end=',')
            print()
    return None
