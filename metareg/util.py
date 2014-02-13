import random
import time


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
