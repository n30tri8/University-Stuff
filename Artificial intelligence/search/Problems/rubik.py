from random import randint


class State:
    def __init__(self, arr):
        self.arrangement = []
        for sub_list in arr:
            self.arrangement.append(sub_list.copy())


class Rubik:
    initial_state = None

    def __init__(self, arr):
        self.initial_state = State(arr)

    @staticmethod
    def next_random_neighbor(state):
        new_state = State(state.arrangement)
        movement = randint(0, 11)
        row = movement//2
        direction = movement % 2
        t0 = [0, 3, 6]
        t1 = [1, 4, 7]
        t2 = [2, 5, 8]

        u1 = [3, 4, 5]

        if row == 0:
            swap_0 = [new_state.arrangement[0][idx] for idx in t0]
            if direction == 0:
                Rubik.rotate_cross(new_state, 1, direction)
                for idx in t0:
                    t0_reverse = [6, 3, 0]
                    new_state.arrangement[0][t0_reverse[idx//3]] = new_state.arrangement[5][idx]
                for idx in t0:
                    new_state.arrangement[5][idx] = new_state.arrangement[4][idx]
                for idx in t0:
                    new_state.arrangement[4][idx] = new_state.arrangement[2][idx]
                for idx in t0:
                    new_state.arrangement[2][idx] = swap_0[idx//3]
            elif direction == 1:
                Rubik.rotate_cross(new_state, 1, direction)
                for idx in t0:
                    new_state.arrangement[0][idx] = new_state.arrangement[2][idx]
                for idx in t0:
                    new_state.arrangement[2][idx] = new_state.arrangement[4][idx]
                for idx in t0:
                    new_state.arrangement[4][idx] = new_state.arrangement[5][idx]
                for idx in t0:
                    new_state.arrangement[5][idx] = swap_0[2 - idx//3]
        elif row == 1:
            swap_0 = [new_state.arrangement[0][idx] for idx in t1]
            if direction == 0:
                for idx in t1:
                    t1_reverse = [7, 4, 1]
                    new_state.arrangement[0][t1_reverse[idx//3]] = new_state.arrangement[5][idx]
                for idx in t1:
                    new_state.arrangement[5][idx] = new_state.arrangement[4][idx]
                for idx in t1:
                    new_state.arrangement[4][idx] = new_state.arrangement[2][idx]
                for idx in t1:
                    new_state.arrangement[2][idx] = swap_0[idx//3]
            elif direction == 1:
                for idx in t1:
                    new_state.arrangement[0][idx] = new_state.arrangement[2][idx]
                for idx in t1:
                    new_state.arrangement[2][idx] = new_state.arrangement[4][idx]
                for idx in t1:
                    new_state.arrangement[4][idx] = new_state.arrangement[5][idx]
                for idx in t1:
                    new_state.arrangement[5][idx] = swap_0[2 - idx//3]
        elif row == 2:
            swap_0 = [new_state.arrangement[0][idx] for idx in t2]
            if direction == 0:
                Rubik.rotate_cross(new_state, 3, direction)
                for idx in t2:
                    t2_reverse = [6, 3, 0]
                    new_state.arrangement[0][t2_reverse[idx//3]] = new_state.arrangement[5][idx]
                for idx in t2:
                    new_state.arrangement[5][idx] = new_state.arrangement[4][idx]
                for idx in t2:
                    new_state.arrangement[4][idx] = new_state.arrangement[2][idx]
                for idx in t2:
                    new_state.arrangement[2][idx] = swap_0[idx//3]
            elif direction == 1:
                Rubik.rotate_cross(new_state, 3, direction)
                for idx in t2:
                    new_state.arrangement[0][idx] = new_state.arrangement[2][idx]
                for idx in t2:
                    new_state.arrangement[2][idx] = new_state.arrangement[4][idx]
                for idx in t2:
                    new_state.arrangement[4][idx] = new_state.arrangement[5][idx]
                for idx in t2:
                    new_state.arrangement[5][idx] = swap_0[2 - idx//3]
        elif row == 4:
            swap_0 = [new_state.arrangement[0][idx] for idx in t1]
            if direction == 0:
                for idx in t1:
                    t1_reverse = [7, 4, 1]
                    new_state.arrangement[0][t1_reverse[idx//3]] = new_state.arrangement[5][idx]
                for idx in t1:
                    new_state.arrangement[5][idx] = new_state.arrangement[4][idx]
                for idx in t1:
                    new_state.arrangement[4][idx] = new_state.arrangement[2][idx]
                for idx in t1:
                    new_state.arrangement[2][idx] = swap_0[idx//3]
            elif direction == 1:
                for idx in t1:
                    new_state.arrangement[0][idx] = new_state.arrangement[2][idx]
                for idx in t1:
                    new_state.arrangement[2][idx] = new_state.arrangement[4][idx]
                for idx in t1:
                    new_state.arrangement[4][idx] = new_state.arrangement[5][idx]
                for idx in t1:
                    new_state.arrangement[5][idx] = swap_0[2 - idx//3]


        return new_state

    @staticmethod
    def rotate_cross(state, cross_idx, direction):
        state.arrangement[]


