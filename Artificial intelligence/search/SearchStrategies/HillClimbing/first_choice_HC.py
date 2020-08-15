from Misc.Node import Node


class FirstChoiceHillClimbing:
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
            next_node = Node(state=None)
            next_node.heuristic_value = float('-inf')
            for i in range(5000):
                node = Node(state=problem.next_random_neighbor(current.state))
                node.heuristic_value = self.evaluate(node)
                if node.heuristic_value > current.heuristic_value:
                    next_node = node
                    break
            if next_node.heuristic_value <= current.heuristic_value:
                self.local_maximum = current
                return current.state
            current = next_node
