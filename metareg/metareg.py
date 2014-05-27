import functools
import math
import random
import re

from . import settings, util


def does_match(regex, strings):
    ''' Does regex match any from a collection of strings? '''
    compiled = re.compile(regex)
    return any(re.search(compiled, s) for s in strings)


def matched_strings(regex, strings):
    ''' Set of strings matched by regex '''
    compiled = re.compile(regex)
    return {s for s in strings if re.search(compiled, s)}


def escape(char):
    '''
    Escape special regex character
    re.escape escapes all characters that are neither ASCII letters,
    numbers or '_'. This results in too many backslashes, unnecessarily
    increasing the size of the resulting regex
    '''
    return "\\" + char if char in settings.escape_characters else char


def dotify(char):
    ''' Randomly return character or a dot '''
    return "." if random.random() < settings.prob_dotify else char


def repeat(char):
    '''
    Possibly repeat a regex character
    Appends a +, * or a ? to the character with a low probability
    '''
    index = util.one_of(settings.repeat_character_probs)
    return char + settings.repeat_characters[index]


def random_substring(string):
    ''' Random substring from a string '''
    # Length of string plus ^ and $ anchor tags
    total_length = len(string) + 2
    start_index = random.randrange(total_length)
    end_index = start_index + round(settings.substring_length_dist())
    raw_substring = string[max(start_index - 1, 0):end_index - 1]
    substring = "".join(repeat(dotify(escape(c))) for c in raw_substring)
    if start_index == 0:
        substring = "^" + substring
    if end_index >= total_length - 1:
        substring += "$"
    return substring


def random_regex_component_generator(strings):
    '''
    Generator returning random regex components that match one of a collection
    of strings
    '''
    # Cheaper to get random item from list than set
    string_list = list(strings)
    while True:
        string = random.choice(string_list)
        yield random_substring(string)


def regex_components(match_these, dont_match_these):
    '''
    Generate a set of regex components which each match one or more of the
    'good' strings, while matching none of the 'bad'
    '''
    # Whole matches for each string
    wholes = {"^{0}$".format(s) for s in match_these}
    parts = {
        p for p in util.generate_until(
            settings.time_limit_regex_components,
            random_regex_component_generator(match_these)
        ) if not does_match(p, dont_match_these)
    }
    return wholes.union(parts)


def greedy_weighted_set_cover(strings, regex_components, greediness_dist=None):
    '''
    Use greedy weighted set cover algorithm to find a reasonably short regex
    that matches all from a collection of strings
    '''
    # If argument not given, the distribution always returns 0
    greediness_dist = greediness_dist or (lambda: 0)
    solution = set()
    # Store the string matches for each regex
    matches_by_regex = {r: matched_strings(r, strings) for r in regex_components}

    def score(regex):
        # Add 1 to weight of all but the first regex in the solution due
        # to the | in regex disjunction
        weight = len(regex) + (1 if solution else 0)
        num_matches = len(matches_by_regex[regex])
        return (weight / num_matches) if num_matches > 0 else float("+inf")
    while strings:
        regex_components = [
            r for w, r in sorted((
                (score(r), r) for r in regex_components
            ), reverse=True) if w != float("+inf")
        ]
        if not regex_components:
            break  # No set cover could be found
        # If greediness distribution sample returns 0, the last (i.e. best)
        # element will be added to the solution. This would be truly greedy
        greediness = min(len(regex_components) - 1, round(greediness_dist()))
        best_regex = regex_components.pop(-1 - greediness)
        solution.add(best_regex)
        strings_to_remove = matches_by_regex.pop(best_regex)
        strings = strings.difference(strings_to_remove)
        matches_by_regex = {c: m - strings_to_remove for c, m in matches_by_regex.items()}
    return solution


def neighbour_solution(solution, strings, regex_components):
    '''
    Generate a neighbour solution to a currently acceptable solution
    A neighbour is generated by removing a random number of regexes from the
    current solution and then running a randomized weighted set cover algorithm
    on this partial solution
    '''
    num_patterns_to_remove = min(
        round(settings.neighbour_remove_regex_dist()),
        # Don't remove more solutions than in the solution
        len(solution) - 1
    )
    num_patterns_to_keep = len(solution) - num_patterns_to_remove
    partial_solution = set(random.sample(solution, num_patterns_to_keep))
    unmatched_strings = strings - set.union(*(
        matched_strings(r, strings) for r in partial_solution
    ))
    partial_solution.update(greedy_weighted_set_cover(
        unmatched_strings,
        regex_components - partial_solution,
        settings.neighbour_greediness_dist
    ))
    return partial_solution


def move_to_neighbour_solution(current, neighbour, inverse_temperature, strings_missed):
    ''' Whether or not to move to a neighbour solution in simulated annealing '''
    energy_delta = (
        (len("|".join(neighbour)) - len("|".join(current))) +
        # At a high temperature, there should be a chance to enter invalid solutions
        # in order to escape a non-optimal neighbourhood
        (strings_missed * settings.strings_missed_cost)
    )
    # Always move if neighbour is in a lower energy state
    if energy_delta <= 0:
        return True
    inertia = -energy_delta * inverse_temperature   # Resistance to change
    return random.random() < math.exp(inertia)


def simulated_annealing_generator(solution, match_these, dont_match_these, regex_components):
    '''
    Use simulated annealing to generate improved solutions after greedy
    search
    '''
    inverse_temperature = (yield solution)
    while True:
        neighbour = neighbour_solution(solution, match_these, regex_components)
        strings_missed = len(match_these) - len(matched_strings("|".join(neighbour), match_these))
        if move_to_neighbour_solution(solution, neighbour, inverse_temperature, strings_missed):
            solution = neighbour
        inverse_temperature = (yield solution)


def verify(regex, match_these, dont_match_these):
    ''' Verify that regex matches all good strings but no bad '''
    compiled = re.compile(regex)
    return (
        all(re.search(compiled, s) for s in match_these) and
        not does_match(regex, dont_match_these)
    )


def improve_solution(solution, match_these, dont_match_these, components):
    ''' Find the best solution from a simulated annealing run '''
    simulated_annealer = util.generate_until(
        settings.time_limit_simulated_annealing,
        simulated_annealing_generator(solution, match_these, dont_match_these, components)
    )

    def is_improved_solution(best_so_far, new):
        new_regex = "|".join(new)
        if len(new_regex) < len("|".join(best_so_far)) and verify(new_regex, match_these, dont_match_these):
            return new
        else:
            return best_so_far
    return functools.reduce(is_improved_solution, simulated_annealer)


def find_regex(match_these, dont_match_these):
    ''' Find short regex to match all of one set of strings but none of the other '''
    components = regex_components(match_these, dont_match_these)
    cover = greedy_weighted_set_cover(match_these, components)
    improved = improve_solution(cover, match_these, dont_match_these, components)
    return "|".join(improved)
