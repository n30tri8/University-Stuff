from random import randint
from SearchStrategies.HillClimbing.hill_climbing import HillClimbing
from SearchStrategies.HillClimbing.first_choice_HC import FirstChoiceHillClimbing
from SearchStrategies.HillClimbing.stochastic_HC import StochasticHillClimbing
from SearchStrategies.HillClimbing.random_restart_HC import RandomRestartHillClimbing

from Problems.balance_queue import BalanceQueue

group_size = 3
no_groups = 50
number_range = 1000

arrangement = []
output = open('.\\solutions\\q4\\input_queue.txt', 'w', encoding='utf-8')
for i in range(no_groups):
    t = [randint(-number_range, number_range) for j in range(group_size)]
    arrangement.append(t)

    text = str(t)
    output.write(text + '\n')

problem = BalanceQueue(arrangement)
output.write('----------' + '\n')
output.write('initial state fitness: ' + str(HillClimbing.evaluate_state(problem.initial_state)) + '\n')
output.close()

hc = HillClimbing()
solution_state = hc.solve(problem)
output = open('.\\solutions\\q4\\hc.txt', 'w', encoding='utf-8')
for t in solution_state.arrangement:
    text = str(t)
    output.write(text + '\n')

output.write('----------' + '\n')
output.write('solution state fitness: ' + str(hc.local_maximum.heuristic_value) + '\n')
output.write('no. visited states: ' + str(hc.stat_visited_nodes) + '\n')
output.close()

hc_fc = FirstChoiceHillClimbing()
solution_state = hc_fc.solve(problem)
output = open('.\\solutions\\q4\\hc_first_choice.txt', 'w', encoding='utf-8')
for t in solution_state.arrangement:
    text = str(t)
    output.write(text + '\n')

output.write('----------' + '\n')
output.write('solution state fitness: ' + str(hc_fc.local_maximum.heuristic_value) + '\n')
output.write('no. visited states: ' + str(hc_fc.stat_visited_nodes) + '\n')
output.close()

hc_stoc = StochasticHillClimbing()
solution_state = hc_stoc.solve(problem)
output = open('.\\solutions\\q4\\hc_stochastic.txt', 'w', encoding='utf-8')
for t in solution_state.arrangement:
    text = str(t)
    output.write(text + '\n')

output.write('----------' + '\n')
output.write('solution state fitness: ' + str(hc_stoc.local_maximum.heuristic_value) + '\n')
output.write('no. visited states: ' + str(hc_stoc.stat_visited_nodes) + '\n')
output.close()

hc_rr = RandomRestartHillClimbing()
solution_state = hc_rr.solve(problem)
output = open('.\\solutions\\q4\\hc_random_restart.txt', 'w', encoding='utf-8')
for t in solution_state.arrangement:
    text = str(t)
    output.write(text + '\n')

output.write('----------' + '\n')
output.write('solution state fitness: ' + str(hc_rr.local_maximum.heuristic_value) + '\n')
output.write('no. visited states: ' + str(hc_rr.stat_visited_nodes) + '\n')
output.close()

# plotting results
import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 2
stat_hc = (hc.local_maximum.heuristic_value, hc.stat_visited_nodes)
stat_hc_fc = (hc_fc.local_maximum.heuristic_value, hc_fc.stat_visited_nodes)
stat_hc_stoc = (hc_stoc.local_maximum.heuristic_value, hc_stoc.stat_visited_nodes)
stat_hc_rr = (hc_rr.local_maximum.heuristic_value, hc_rr.stat_visited_nodes)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.25
opacity = 0.8

rects1 = plt.bar(index, stat_hc, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Hill Climbing')
rects2 = plt.bar(index + bar_width, stat_hc_fc, bar_width,
                 alpha=opacity,
                 color='r',
                 label='First Choice')
rects3 = plt.bar(index + 2*bar_width, stat_hc_stoc, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Stochastic')
rects4 = plt.bar(index + 3*bar_width, stat_hc_rr, bar_width,
                 alpha=opacity,
                 color='y',
                 label='Random Restart')

plt.xlabel('Algorithm')
plt.ylabel('Stat')
plt.title('Statistics by Algorithm')
plt.xticks(index + bar_width, ('solution fitness', 'visited nodes'))
plt.legend()

plt.tight_layout()
plt.show()
