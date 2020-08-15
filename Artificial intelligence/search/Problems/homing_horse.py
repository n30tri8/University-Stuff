class State:
    horse_cell = 0

    def __init__(self, arr):
        self.horse_cell = arr

    def __hash__(self):
        return self.horse_cell

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return False
        if self.horse_cell != other.horse_cell:
            return False
        return True


class HomingHorse:
    #              1  2  3  4  5  6  7  8
    arrangement = [0, 0, 0, 0, 0, 0, 0, 0,   # 1
                   0, 0, 0, 0, 0, 0, 0, 0,   # 2
                   0, -1, 0, 0, 0, 0, 0, 0,  # 3
                   0, 0, 0, 0, 0, -1, 0, 0,  # 4
                   0, 0, 0, -1, 0, 0, 0, 0,  # 5
                   0, 0, 0, 0, -1, 0, 0, 0,  # 6
                   2, 0, 0, 0, 0, 0, 0, 0,   # 7
                   0, 0, 0, 0, 2, 0, 0, 0,   # 8
                   ]
    initial_state = State(5)
    goal_state = None

    def __init__(self, arr=None):
        if arr is not None:
            self.arrangement = arr.copy()
            for idx, e in enumerate(self.arrangement):
                if e == 1:
                    self.initial_state = State(idx)
                    break
        pass

    def goal_test(self, state):
        if self.arrangement[state.horse_cell] == 2:
            return True
        else:
            return False

    def actions(self, state):
        hc = state.horse_cell
        col = state.horse_cell % 8
        row = state.horse_cell // 8
        if col > 1 and row < 7 and self.arrangement[hc + 6] != -1:  # left, down(0)
            yield (0, 1)
        if col > 1 and row > 0 and self.arrangement[hc - 10] != -1:  # left, up(1)
            yield (1, 1)
        if col > 0 and row > 1 and self.arrangement[hc - 17] != -1:  # up, left(2)
            yield (2, 1)
        if col < 7 and row > 1 and self.arrangement[hc - 15] != -1:  # up, right(3)
            yield (3, 1)
        if col < 6 and row > 0 and self.arrangement[hc - 6] != -1:  # right, up(4)
            yield (4, 1)
        if col < 6 and row < 7 and self.arrangement[hc + 10] != -1:  # right, down(5)
            yield (5, 1)
        if col < 7 and row < 6 and self.arrangement[hc + 17] != -1:  # down, right(6)
            yield (6, 1)
        if col > 0 and row < 6 and self.arrangement[hc + 15] != -1:  # down, left(7)
            yield (7, 1)

    @staticmethod
    def child_state(state, action):
        new_child = State(state.horse_cell)
        if action == 0:
            new_child.horse_cell += 6
        elif action == 1:
            new_child.horse_cell -= 10
        elif action == 2:
            new_child.horse_cell -= 17
        elif action == 3:
            new_child.horse_cell -= 15
        elif action == 4:
            new_child.horse_cell -= 6
        elif action == 5:
            new_child.horse_cell += 10
        elif action == 6:
            new_child.horse_cell += 17
        elif action == 7:
            new_child.horse_cell += 15

        return new_child
