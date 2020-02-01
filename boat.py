class BoatState: 

    def __init__(self):
        self.ml = 3
        self.cl = 3
        self.mb = 0
        self.cb = 0
        self.pos = 0

    def actions(self):
        to_return = []
        if self.mb + self.cb >= 1:
            to_return.append('move and offload')
        return to_return

    def result(self, state, action):
        if action == 'move and offload':
