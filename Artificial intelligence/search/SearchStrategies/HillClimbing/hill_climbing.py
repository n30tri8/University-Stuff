from Misc.Node import Node


class HillClimbing:
    local_maximum = None
    stat_visited_nodes = 0

    def evaluate(self, node):
        max_sum = float('-inf')
        for s in node.state.group_sum:
            max_sum = max(max_sum, s)
        self.stat_visited_nodes += 1
        return 5000-max_sum

    @staticmethod
    def evaluate_state(state):
        max_sum = float('-inf')
        for s in state.group_sum:
            max_sum = max(max_sum, s)
        return 5000-max_sum

    def solve(self, problem):
        current = Node(state=problem.initial_state)
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
                self.local_maximum = current
                return current.state
            current = best_neighbor
