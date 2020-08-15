class State:
    arrangement = [False, False,
                   False, False,
                   False, False,
                   False, False,
                   False
                   ]

    def __init__(self, arr=None):
        if arr is not None:
            self.arrangement = arr.copy()

    def __hash__(self):
        sum_state = 0
        for idx, e in enumerate(self.arrangement):
            sum_state += (2 ** idx) * e
        return sum_state

    def __eq__(self, other):
        if not isinstance(self, type(other)) or len(self.arrangement) != len(other.arrangement):
            return False
        for idx in range(len(self.arrangement)):
            if self.arrangement[idx] != other.arrangement[idx]:
                return False
        return True


class PassTheRiver:
    initial_state = State(None)
    goal_state = State([True, True,
                        True, True,
                        True, True,
                        True, True,
                        True
                        ])

    @staticmethod
    def goal_test(state):
        for e in state.arrangement:
            if not e:
                return False

        return True

    @staticmethod
    def actions(state):
        for idx, e in enumerate(state.arrangement):
            if idx == 8:
                continue
            if e == state.arrangement[8]:
                yield ((idx, None, not e), 1)
                if idx % 2 == 0 and state.arrangement[idx + 1] == e:
                    yield ((idx, idx + 1, not e), 1)

    @staticmethod
    def child_state(state, action):
        new_child = State(state.arrangement)
        new_child.arrangement[action[0]] = action[2]
        new_child.arrangement[8] = action[2]
        if action[1] is not None:
            new_child.arrangement[action[1]] = action[2]
        return new_child
