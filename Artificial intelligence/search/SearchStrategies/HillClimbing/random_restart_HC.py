from random import randint
from Misc.Node import Node


class RandomRestartHillClimbing:
    local_maximum = Node(state=None)
    local_maximum.heuristic_value = float('-inf')
    stat_visited_nodes = 0

    def evaluate(self, node):
        max_sum = float('-inf')
        for s in node.state.group_sum:
            max_sum = max(max_sum, s)
        self.stat_visited_nodes += 1
        return 5000-max_sum

    def solve(self, problem):
        random_start_state = problem.initial_state
        for i in range(5):
            random_move = randint(1, 10)
            for j in range(random_move):
                neighbors = problem.neighbors(random_start_state)
                random_bypass = randint(0, 50)
                for k in range(random_bypass):
                    next(neighbors)
                random_start_state = next(neighbors)

            current = Node(state=random_start_state)
            current.heuristic_value = self.evaluate(current)
            while True:
                best_neighbor = Node(state=None)
                best_neighbor.heuristic_value = float('-inf')
                for neighbor in problem.neighbors(current.state):
                    node = Node(state=neighbor)
                    node.heuristic_value = self.evaluate(node)
                    if node.heuristic_value > best_neighbor.heuristic_value:
                        best_neighbor = node
                if best_neighbor.heuristic_value <= current.heuristic_value:
                    if self.local_maximum.heuristic_value < current.heuristic_value:
                        self.local_maximum = current
                    break
                current = best_neighbor

        return self.local_maximum.state
