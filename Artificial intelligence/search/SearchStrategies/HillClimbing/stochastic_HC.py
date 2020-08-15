from random import choices
from Misc.Node import Node


class StochasticHillClimbing:
    local_maximum = None
    stat_visited_nodes = 0

    def evaluate(self, node):
        max_sum = float('-inf')
        for s in node.state.group_sum:
            max_sum = max(max_sum, s)
        self.stat_visited_nodes += 1
        return 5000-max_sum

    def solve(self, problem):
        current = Node(state=problem.initial_state)
        current.heuristic_value = self.evaluate(current)
        while True:
            good_neighbors = list()
            for neighbor in problem.neighbors(current.state):
                node = Node(state=neighbor)
                node.heuristic_value = self.evaluate(node)
                if node.heuristic_value > current.heuristic_value:
                    good_neighbors.append(node)
            if len(good_neighbors) != 0:
                # next_node = choices(population=good_neighbors, weights=[n.heuristic_value for n in good_neighbors], k=1)[0]
                next_node = choices(population=good_neighbors, k=1)[0]
            else:
                next_node = Node(state=None)
                next_node.heuristic_value = float('-inf')
            if next_node.heuristic_value <= current.heuristic_value:
                self.local_maximum = current
                return current.state
            current = next_node

