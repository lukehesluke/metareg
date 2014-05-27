import itertools
import operator
import random
import time


def one_of(probs):
    '''
    Returns the index of one of a list of weighted probabilities
    Example usage:
        one_of([0.5, 0.4, 0.1])
        will return:
            0 with 50% chance
            1 with 40% chance
            2 with 10% chance
    '''
    total = sum(probs)
    rand = random.random() * total
    for i, prob in enumerate(probs):
        rand -= prob
        if rand <= 0:
            break
    return i


def generate_until(time_limit, generator):
    '''
    Iterate through generator until time limit, in seconds, is reached
    At each iteration, feeds the generator the ratio of time remaining
    '''
    time_begin = time.time()
    time_elapsed = 0
    yield next(generator)
    while time_elapsed < time_limit:
        time_elapsed = time.time() - time_begin
        yield generator.send(time_elapsed / time_limit)


def half_normal_distribution(mu, sigma):
    '''
    A normal distribution with only a positive side
    Example usage:
        dist = half_normal_distribution(3, 5)
        dist()  # Returms, say, 5.5
        dist()  # Returns, say, 4.1
    '''
    return lambda: abs(random.gauss(0, sigma)) + mu
