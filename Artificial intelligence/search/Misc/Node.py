class Node:
    def __init__(self, state, previous_node=None, pre_act=None, cost=None, depth=None):
        self.state = state
        self.parent = previous_node
        self.pre_act = pre_act
        self.cost = cost
        self.depth = depth
        self.heuristic_value = None
