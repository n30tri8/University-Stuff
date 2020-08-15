from SearchStrategies.BFS import BFS
from SearchStrategies.DFS import DFS
from Problems.pass_the_river import PassTheRiver

problem = PassTheRiver()

bfs = BFS()
solved = bfs.solve(problem)
f1 = open('.\\solutions\\q1\\q1_bfs.txt', 'w')
if solved:
    action_seq = bfs.return_action_seq()

    for act in action_seq:
        text = '(' + str(act[0])
        if act[1] is not None:
            text += ' , ' + str(act[1])
        direction = '->' if act[2] else '<-'
        text += ') ' + direction
        f1.write(text + '\n')

    f1.write('----------' + '\n')
    f1.write('expanded nodes: ' + str(bfs.stat_expanded_nodes) + '\n')
    f1.write('visited nodes: ' + str(bfs.stat_visited_nodes) + '\n')
    f1.write('sol. depth: ' + str(bfs.stat_solution_depth) + '\n')
    f1.write('max mem.: ' + str(bfs.stat_max_memory) + '\n')
else:
    f1.write('could not solve...')
f1.close()


dfs = DFS()
solved = dfs.solve(problem)
f2 = open('.\\solutions\\q1\\q1_dfs.txt', 'w')
if solved:
    action_seq = dfs.return_action_seq()

    for act in action_seq:
        text = '(' + str(act[0])
        if act[1] is not None:
            text += ' , ' + str(act[1])
        direction = '->' if act[2] else '<-'
        text += ') ' + direction
        f2.write(text + '\n')

    f2.write('----------' + '\n')
    f2.write('expanded nodes: ' + str(dfs.stat_expanded_nodes) + '\n')
    f2.write('visited nodes: ' + str(dfs.stat_visited_nodes) + '\n')
    f2.write('sol. depth: ' + str(dfs.stat_solution_depth) + '\n')
    f2.write('max mem.: ' + str(dfs.stat_max_memory) + '\n')
else:
    f2.write('could not solve...')
f2.close()

# plotting results
import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 4
stat_bfs = (bfs.stat_expanded_nodes, bfs.stat_visited_nodes, bfs.stat_solution_depth, bfs.stat_max_memory)
stat_dfs = (dfs.stat_expanded_nodes, dfs.stat_visited_nodes, dfs.stat_solution_depth, dfs.stat_max_memory)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, stat_bfs, bar_width,
                 alpha=opacity,
                 color='b',
                 label='BFS')

rects2 = plt.bar(index + bar_width, stat_dfs, bar_width,
                 alpha=opacity,
                 color='g',
                 label='DFS')

plt.xlabel('Algorithm')
plt.ylabel('Stat')
plt.title('Statistics by Algorithm')
plt.xticks(index + bar_width, ('expanded nodes', 'visited nodes', 'sol. depth', 'max mem.'))
plt.legend()

plt.tight_layout()
plt.show()
