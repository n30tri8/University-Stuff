from SearchStrategies.DLS import DLS


class IDS:
    dls = None

    stat_expanded_nodes = 0
    stat_max_memory = 0

    def solve(self, problem):
        for cut_off in range(200):
            self.dls = DLS(cut_off)
            solved = self.dls.solve(problem)

            self.stat_expanded_nodes += self.dls.stat_expanded_nodes
            self.stat_max_memory = max(self.stat_max_memory , self.dls.stat_max_memory)
            if solved:
                return solved
        return False
