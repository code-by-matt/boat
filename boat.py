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
            new_state.cdiff = 3 - new_state.cdiff
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
