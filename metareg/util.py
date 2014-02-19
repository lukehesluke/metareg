import itertools
import operator
import random
import time


def first(iterable, default=None):
    ''' First element from iterable or some default value '''
    try:
        return next(iter(iterable))
    except StopIteration:
        return default


def tuple_accumulator(n, func=operator.add):
    '''
    Creates an accumulator function which can be used, along with
    itertools.accumulate to accumulate the value at the n-th position
    in tuples
    '''
    def accumulator(tuple1, tuple2):
        indexed_tuple = zip(itertools.count(), tuple2)
        return tuple(
            item if pos != n else func(tuple1[n], tuple2[n])
            for pos, item in indexed_tuple
        )
    return accumulator


def one_of(probs_dict, default=None):
    '''
    Randomly returns an object with each object mapping onto its chance
    of being returned
    Example usage:
        one_of("half_chance": 0.5, "two_fifths": 0.4, "one_tenth": 0.1)
    If the probabilities add up to less than 1, the default value may be
    returned
    '''
    rand = random.random()
    # Accumulate probabilities so, e.g. (0.5, 0.4, 0.1) becomes (0.5, 0.9, 1.0)
    accumulated = itertools.accumulate(probs_dict.items(), tuple_accumulator(1))
    # The first object whose accumulated probability is greater than a random
    # number is returned
    return first((obj for obj, prob in accumulated if rand < prob), default)


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
