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
                to_return.append('onload ' + str(i) + 'm')
        for i in [1, 2]:
            if i <= self.csame and self.mboat + self.cboat + i <= 2 and okay(self.mboat, self.cboat + i):
                to_return.append('onload ' + str(i) + 'c')
        return to_return

    def result(self, state, action):
        if action == 'move and offload':
