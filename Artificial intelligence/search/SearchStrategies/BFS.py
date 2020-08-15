from Misc.Node import Node


class BFS:
    stat_expanded_nodes = 0
    stat_visited_nodes = 0
    stat_max_memory = 0
    stat_solution_depth = 0
    stat_solution_cost = 0

    frontier = list()
    explored = set()
    frontier_state_set = set()
    goal_node = None

    def add_frontier(self, node):
        self.frontier.append(node)
        self.frontier_state_set.add(hash(node.state))
        self.stat_visited_nodes += 1
        self.stat_max_memory = max(self.stat_max_memory, len(self.frontier))

    def select_next_frontier(self):
        next_node = self.frontier.pop(0)
        self.frontier_state_set.remove(hash(next_node.state))
        return next_node

    def stat(self, stat_expanded_nodes=None, stat_solution_depth=None, stat_solution_cost=None):
        if stat_expanded_nodes is not None:
            self.stat_expanded_nodes = stat_expanded_nodes
        if stat_solution_depth is not None:
            self.stat_solution_depth = stat_solution_depth
        if stat_solution_cost is not None:
            self.stat_solution_cost = stat_solution_cost

    def solution(self, node):
        self.stat(stat_expanded_nodes=len(self.explored))
        if not node:
            return False
        else:
            self.goal_node = node
            self.stat(stat_solution_cost=self.goal_node.cost)
            return True

    def solve(self, problem):
        node = Node(problem.initial_state, None, None, 0)
        if problem.goal_test(node.state):
            return self.solution(node)
        self.add_frontier(node)
        while True:
            if len(self.frontier) == 0:
                return self.solution(False)
            node = self.select_next_frontier()
            self.explored.add(hash(node.state))
            for action in problem.actions(node.state):
                child = Node(problem.child_state(node.state, action[0]), node, action[0], action[1] + node.cost)
                child_hash = hash(child.state)
                if child_hash not in self.explored and child_hash not in self.frontier_state_set:
                    if problem.goal_test(child.state):
                        return self.solution(child)
                    self.add_frontier(child)

    def return_action_seq(self):
        action_seq = list()
        node = self.goal_node
        while node is not None:
            action_seq.insert(0, node.pre_act)
            node = node.parent
        action_seq.pop(0)
        self.stat(stat_solution_depth=len(action_seq))
        return action_seq


