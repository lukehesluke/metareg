from .util import half_normal_distribution

escape_characters = {"$", "^", "\\", ".", "*", "+", "(", ")", "[", "]", "?"}
# Probability of turning a character in a regex component into a dot
prob_dotify = 0.25
# Probabilities of repeating characters in a regex component using +, * or ?
repeat_character_probs = {"+": 0.15, "*": 0.2, "?": 0.1}
# Distribution used to determine length of regex components
substring_length_dist = half_normal_distribution(1, 1.75)
# Determines number of regexes to remove from solution when looking for
# neighbour solutions
neighbour_remove_regex_dist = half_normal_distribution(1, 1.75)
# In greedy algorithm, the locally optimal solution is always chosen at each
# iteration. This distribution adds some randomness to this when generating
# neighbour solutions
neighbour_greediness_dist = half_normal_distribution(0, 0.5)
# When moving to neighbour solutions in simulated annealing, the cost added
# to moving to an invalid solution for each string that it's missing
# With this cost, when the annealing is at a high temperature, there is still
# a reasonable chance of moving to an invalid solution. This is in the hopes
# of travelling from here to other neighbourhoods that contain valid solutions
strings_missed_cost = 13
# Time limit imposed on construction of random regex components
time_limit_regex_components = 30
# Time limit imposed on improving greedy solution with simulated annealing
time_limit_simulated_annealing = 30
