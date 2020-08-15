from random import randint


class State:
    def __init__(self, arr, group_sum):
        self.arrangement = []
        for sub_list in arr:
            self.arrangement.append(sub_list.copy())
        self.group_sum = group_sum.copy()


class BalanceQueue:
    initial_state = None

    def __init__(self, arr):
        group_sum = []
        for t in arr:
            g_sum = sum(t)
            group_sum.append(g_sum)
        self.initial_state = State(arr, group_sum)

    @staticmethod
    def neighbors(state):
        state_copy = State(state.arrangement, state.group_sum)
        for t_idx, triple in enumerate(state_copy.arrangement[0:len(state_copy.arrangement) - 1]):
            for i_idx, i in enumerate(triple):
                triple.pop(i_idx)
                for j_idx, j in enumerate(state_copy.arrangement[t_idx + 1]):
                    state_copy.arrangement[t_idx + 1].pop(j_idx)
                    state_copy.arrangement[t_idx + 1].insert(j_idx, i)
                    triple.insert(i_idx, j)

                    state_copy.group_sum[t_idx] = state_copy.group_sum[t_idx] - i + j
                    state_copy.group_sum[t_idx + 1] = state_copy.group_sum[t_idx + 1] + i - j

                    new_state = State(state_copy.arrangement, state_copy.group_sum)
                    yield new_state

                    state_copy.arrangement[t_idx + 1].pop(j_idx)
                    state_copy.arrangement[t_idx + 1].insert(j_idx, j)
                    triple.pop(i_idx)

                    state_copy.group_sum[t_idx] = state_copy.group_sum[t_idx] + i - j
                    state_copy.group_sum[t_idx + 1] = state_copy.group_sum[t_idx + 1] - i + j

                triple.insert(i_idx, i)

    @staticmethod
    def next_random_neighbor(state):
        new_state = State(state.arrangement, state.group_sum)
        i_triple = randint(0, len(new_state.arrangement) - 1)
        j_triple = randint(0, len(new_state.arrangement) - 1)
        while j_triple == i_triple:
            j_triple = randint(0, len(new_state.arrangement) - 1)

        i_idx = randint(0, len(new_state.arrangement[i_triple]) - 1)
        j_idx = randint(0, len(new_state.arrangement[j_triple]) - 1)

        ti = new_state.arrangement[i_triple].pop(i_idx)
        tj = new_state.arrangement[j_triple].pop(j_idx)
        new_state.arrangement[i_triple].append(tj)
        new_state.arrangement[j_triple].append(ti)

        new_state.group_sum[i_triple] = new_state.group_sum[i_triple] - ti + tj
        new_state.group_sum[j_triple] = new_state.group_sum[j_triple] + ti - tj

        return new_state


