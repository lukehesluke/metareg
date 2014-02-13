from .util import half_normal_distribution

# Probability of turning a character in a regex component into a dot
prob_dotify = 0.2
# Distribution used to determine length of regex components
substring_length_dist = half_normal_distribution(1, 2)
# Determines number of regexes to remove from solution when looking for
# neighbour solutions
neighbour_remove_regex_dist = half_normal_distribution(1, 1)
# In greedy algorithm, the locally optimal solution is always chosen at each
# iteration. This distribution adds some randomness to this when generating
# neighbour solutions
neighbour_greediness_dist = half_normal_distribution(0, 1.5)
# Time limit imposed on construction of random regex components
time_limit_regex_components = 30
# Time limit imposed on improving greedy solution with simulated annealing
time_limit_simulated_annealing = 30
