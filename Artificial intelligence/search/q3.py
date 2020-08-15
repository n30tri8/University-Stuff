from SearchStrategies.UCS import UCS
from SearchStrategies.IDS import IDS
from Problems.homing_horse import HomingHorse

#              1  2  3  4  5  6  7  8
arrangement = [0, 0, 0, 0, 0, 1, 0, 0,   # 1
               0, 0, 0, 0, 0, 0, 0, 0,   # 2
               0, -1, 0, 0, 0, 0, 0, 0,  # 3
               0, 0, 0, 0, 0, -1, 0, 0,  # 4
               0, 0, 0, -1, 0, 0, 0, 0,  # 5
               0, 0, 0, 0, -1, 0, 0, 0,  # 6
               2, 0, 0, 0, 0, 0, 0, 0,   # 7
               0, 0, 0, 0, 2, 0, 0, 0,   # 8
               ]

try:
    input_file = open('.\\input\\q3.txt', 'r')
    arrangement = []
    for line in input_file:
        arrangement += [int(s) for s in line.rstrip().split(', ')]
    input_file.close()
except FileNotFoundError:
    print('No input file. Continuing with default arrangement')

problem = HomingHorse(arrangement)

ucs = UCS()
solved = ucs.solve(problem)
output = open('.\\solutions\\q3\\ucs.txt', 'w', encoding='utf-8')
if solved:
    action_seq = ucs.return_action_seq()

    for act in action_seq:
        text = None
        if act == 0:
            text = '\u2190\u2190\u2193'
        elif act == 1:
            text = '\u2190\u2190\u2191'
        elif act == 2:
            text = '\u2191\u2191\u2190'
        elif act == 3:
            text = '\u2191\u2191\u2192'
        elif act == 4:
            text = '\u2192\u2192\u2191'
        elif act == 5:
            text = '\u2192\u2192\u2193'
        elif act == 6:
            text = '\u2193\u2193\u2192'
        elif act == 7:
            text = '\u2193\u2193\u2190'

        output.write(text + '\n')

    output.write('----------' + '\n')
    output.write('expanded nodes: ' + str(ucs.stat_expanded_nodes) + '\n')
    output.write('visited nodes: ' + str(ucs.stat_visited_nodes) + '\n')
    output.write('sol. depth: ' + str(ucs.stat_solution_depth) + '\n')
    output.write('max mem.: ' + str(ucs.stat_max_memory) + '\n')
else:
    output.write('could not solve...')
output.close()


ids = IDS()
solved = ids.solve(problem)
output = open('.\\solutions\\q3\\ids.txt', 'w', encoding='utf-8')
if solved:
    action_seq = ids.dls.return_action_seq()

    for act in action_seq:
        text = None
        if act == 0:
            text = '\u2190\u2190\u2193'
        elif act == 1:
            text = '\u2190\u2190\u2191'
        elif act == 2:
            text = '\u2191\u2191\u2190'
        elif act == 3:
            text = '\u2191\u2191\u2192'
        elif act == 4:
            text = '\u2192\u2192\u2191'
        elif act == 5:
            text = '\u2192\u2192\u2193'
        elif act == 6:
            text = '\u2193\u2193\u2192'
        elif act == 7:
            text = '\u2193\u2193\u2190'

        output.write(text + '\n')

    output.write('----------' + '\n')
    output.write('expanded nodes: ' + str(ids.stat_expanded_nodes) + '\n')
    output.write('visited nodes: ' + str(ids.dls.stat_visited_nodes) + '\n')
    output.write('sol. depth: ' + str(ids.dls.stat_solution_depth) + '\n')
    output.write('max mem.: ' + str(ids.stat_max_memory) + '\n')
else:
    output.write('could not solve...')
    if ids.dls.cut_off_error:
        output.write('cut off error occurred')
output.close()

# plotting results
import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 4
stat_ucs = (ucs.stat_expanded_nodes, ucs.stat_visited_nodes, ucs.stat_solution_depth, ucs.stat_max_memory)
stat_ids = (ids.stat_expanded_nodes, ids.dls.stat_visited_nodes, ids.dls.stat_solution_depth, ids.stat_max_memory)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, stat_ucs, bar_width,
                 alpha=opacity,
                 color='b',
                 label='UCS')

rects2 = plt.bar(index + bar_width, stat_ids, bar_width,
                 alpha=opacity,
                 color='g',
                 label='IDS')

plt.xlabel('Algorithm')
plt.ylabel('Stat')
plt.title('Statistics by Algorithm')
plt.xticks(index + bar_width, ('expanded nodes', 'visited nodes', 'sol. depth', 'max mem.'))
plt.legend()

plt.tight_layout()
plt.show()
