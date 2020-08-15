from SearchStrategies.BFS import BFS
from SearchStrategies.DFS import DFS
from SearchStrategies.DLS import DLS
from SearchStrategies.A_star import AStar
from Problems.sliding_puzzle import SlidingPuzzle

arrangement =  [    1, 4, 2,
                   3, 0, 5,
                   6, 7, 8
                   ]

try:
    input_file = open('.\\input\\q2.txt', 'r')
    arrangement = []
    for line in input_file:
        arrangement += [int(s) for s in line.rstrip().split(', ')]
    input_file.close()
except FileNotFoundError:
    print('No input file. Continuing with default arrangement')

problem = SlidingPuzzle(arrangement)

bfs = BFS()
solved = bfs.solve(problem)
output = open('.\\solutions\\q2\\bfs.txt', 'w')
if solved:
    action_seq = bfs.return_action_seq()

    for act in action_seq:
        text = None
        if act == 0:  # To Right(0)
            text = 'Right'
        elif act == 2:  # To Left(2)
            text = 'Left'
        elif act == 1:
            text = 'Down'
        elif act == 3:
            text = 'Up'
        output.write(text + '\n')

    output.write('----------' + '\n')
    output.write('expanded nodes: ' + str(bfs.stat_expanded_nodes) + '\n')
    output.write('visited nodes: ' + str(bfs.stat_visited_nodes) + '\n')
    output.write('sol. depth: ' + str(bfs.stat_solution_depth) + '\n')
    output.write('max mem.: ' + str(bfs.stat_max_memory) + '\n')
else:
    output.write('could not solve...')
output.close()


dfs = DFS()
solved = dfs.solve(problem)
output = open('.\\solutions\\q2\\dfs.txt', 'w')
if solved:
    action_seq = dfs.return_action_seq()

    for act in action_seq:
        text = None
        if act == 0:  # To Right(0)
            text = 'Right'
        elif act == 2:  # To Left(2)
            text = 'Left'
        elif act == 1:
            text = 'Down'
        elif act == 3:
            text = 'Up'
        output.write(text + '\n')

    output.write('----------' + '\n')
    output.write('expanded nodes: ' + str(dfs.stat_expanded_nodes) + '\n')
    output.write('visited nodes: ' + str(dfs.stat_visited_nodes) + '\n')
    output.write('sol. depth: ' + str(dfs.stat_solution_depth) + '\n')
    output.write('max mem.: ' + str(dfs.stat_max_memory) + '\n')
else:
    output.write('could not solve...')
output.close()


dls = DLS(40)
solved = dls.solve(problem)
output = open('.\\solutions\\q2\\dls.txt', 'w')
if solved:
    action_seq = dls.return_action_seq()

    for act in action_seq:
        text = None
        if act == 0:  # To Right(0)
            text = 'Right'
        elif act == 2:  # To Left(2)
            text = 'Left'
        elif act == 1:
            text = 'Down'
        elif act == 3:
            text = 'Up'
        output.write(text + '\n')

    output.write('----------' + '\n')
    output.write('expanded nodes: ' + str(dls.stat_expanded_nodes) + '\n')
    output.write('visited nodes: ' + str(dls.stat_visited_nodes) + '\n')
    output.write('sol. depth: ' + str(dls.stat_solution_depth) + '\n')
    output.write('max mem.: ' + str(dls.stat_max_memory) + '\n')
else:
    output.write('could not solve...')
    if dls.cut_off_error:
        output.write('cut off error occurred')
output.close()


a_star = AStar()
solved = a_star.solve(problem)
output = open('.\\solutions\\q2\\a_star.txt', 'w')
if solved:
    action_seq = a_star.return_action_seq()

    for act in action_seq:
        text = None
        if act == 0:  # To Right(0)
            text = 'Right'
        elif act == 2:  # To Left(2)
            text = 'Left'
        elif act == 1:
            text = 'Down'
        elif act == 3:
            text = 'Up'
        output.write(text + '\n')

    output.write('----------' + '\n')
    output.write('expanded nodes: ' + str(a_star.stat_expanded_nodes) + '\n')
    output.write('visited nodes: ' + str(a_star.stat_visited_nodes) + '\n')
    output.write('sol. depth: ' + str(a_star.stat_solution_depth) + '\n')
    output.write('max mem.: ' + str(a_star.stat_max_memory) + '\n')
else:
    output.write('could not solve...')
output.close()


# plotting results
import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 4
stat_bfs = (bfs.stat_expanded_nodes, bfs.stat_visited_nodes, bfs.stat_solution_depth, bfs.stat_max_memory)
stat_dfs = (dfs.stat_expanded_nodes, dfs.stat_visited_nodes, dfs.stat_solution_depth, dfs.stat_max_memory)
stat_dls = (dls.stat_expanded_nodes, dls.stat_visited_nodes, dls.stat_solution_depth, dls.stat_max_memory)
stat_a_star = (a_star.stat_expanded_nodes, a_star.stat_visited_nodes, a_star.stat_solution_depth, a_star.stat_max_memory)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.15
opacity = 0.8

rects1 = plt.bar(index, stat_bfs, bar_width,
                 alpha=opacity,
                 color='b',
                 label='BFS')

rects2 = plt.bar(index + bar_width, stat_dfs, bar_width,
                 alpha=opacity,
                 color='g',
                 label='DFS')

rects3 = plt.bar(index + 2*bar_width, stat_dls, bar_width,
                 alpha=opacity,
                 color='r',
                 label='DLS')

rects4 = plt.bar(index + 3*bar_width, stat_a_star, bar_width,
                 alpha=opacity,
                 color='y',
                 label='A*')

plt.xlabel('Algorithm')
plt.ylabel('Stat')
plt.title('Statistics by Algorithm')
plt.xticks(index + bar_width, ('expanded nodes', 'visited nodes', 'sol. depth', 'max mem.'))
plt.legend()

plt.tight_layout()
plt.show()
