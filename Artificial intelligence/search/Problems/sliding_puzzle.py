class State:
    arrangement = [0, 1, 2,
                   3, 4, 5,
                   6, 7, 8
                   ]
    empty_cell_index = 0

    def __init__(self, arr=None):
        if arr is not None:
            self.arrangement = arr.copy()
            for idx, cell in enumerate(self.arrangement):
                if cell == 0:
                    self.empty_cell_index = idx
                    break

    def __hash__(self):
        sum_state = 0
        for idx, e in enumerate(self.arrangement):
            sum_state += (10 ** idx) * e
        return sum_state

    def __eq__(self, other):
        if not isinstance(self, type(other)) or len(self.arrangement) != len(other.arrangement):
            return False
        for idx in range(len(self.arrangement)):
            if self.arrangement[idx] != other.arrangement[idx]:
                return False
        return True


class SlidingPuzzle:
    initial_state = State(None)
    goal_state = State([1, 2, 3,
                        4, 5, 6,
                        7, 8, 0
                        ])

    def __init__(self, arr=None):
        if arr is not None:
            arrangement = arr.copy()
            self.initial_state = State(arrangement)

    @staticmethod
    def goal_test(state):
        if state.arrangement[0] == 0:
            for idx, cell in enumerate(state.arrangement[1:]):
                if cell == idx+1:
                    continue
                else:
                    return False
        elif state.arrangement[0] == 1:
            for idx, cell in enumerate(state.arrangement[:8]):
                if cell == idx+1:
                    continue
                else:
                    return False
        else:
            return False
        return True

    @staticmethod
    def actions(state):
        if state.empty_cell_index % 3 != 2:  # To Right(0)
            yield (0, 1)
        if state.empty_cell_index % 3 != 0:  # To Left(2)
            yield (2, 1)
        if state.empty_cell_index < 6:  # Downward(1)
            yield (1, 1)
        if state.empty_cell_index > 2:  # Upward(3)
            yield (3, 1)

    @staticmethod
    def child_state(state, action):
        new_child = State(state.arrangement)
        if action == 0:  # To Right(0)
            new_loc = new_child.empty_cell_index + 1
            new_child.arrangement[new_child.empty_cell_index] = new_child.arrangement[new_loc]
            new_child.arrangement[new_loc] = 0
            new_child.empty_cell_index = new_loc
        elif action == 2:  # To Left(2)
            new_loc = new_child.empty_cell_index - 1
            new_child.arrangement[new_child.empty_cell_index] = new_child.arrangement[new_loc]
            new_child.arrangement[new_loc] = 0
            new_child.empty_cell_index = new_loc
        elif action == 1:  # Downward(1)
            new_loc = new_child.empty_cell_index + 3
            new_child.arrangement[new_child.empty_cell_index] = new_child.arrangement[new_loc]
            new_child.arrangement[new_loc] = 0
            new_child.empty_cell_index = new_loc
        elif action == 3:  # Upward(3)
            new_loc = new_child.empty_cell_index - 3
            new_child.arrangement[new_child.empty_cell_index] = new_child.arrangement[new_loc]
            new_child.arrangement[new_loc] = 0
            new_child.empty_cell_index = new_loc
        return new_child
