import numpy as np
import scipy
from scipy.integrate import quad, dblquad, nquad


def get_integrand(*pdfs):
    def p_product(*xs):
        result = 1
        if len(xs) != len(pdfs):
            print("not the same amount of variables as pdfs")
        for pdf, xi in zip(pdfs, xs):
            result *= pdf(xi)
        return result

    return p_product

#construct uniform distribution between given lower and upper bound
def construct_uniform_pdf(lower, upper):
    def p(x):
        if lower <= x <= upper:
            return 1 / (upper - lower)
        return 0

    return p

#construct normal distribution given mean and std
def construct_normal_pdf(mean, std):
    def p(x):
        value = scipy.stats.norm.pdf(x, loc=mean, scale=std)
        return value

    return p

#If we have a function f(x0, x1, x2), then nquad assumes that x0 is the integration variable of the innermost integral,
# and x2 is the integration variable of the outermost integral.
#The bounds argument takes the bounds in the same order: first the bounds for x0 (innermost integral), and so on,
# until the outermost integral bounds for x2.
#The earlier entries in the bounds list can depend on the values of all the following integration variables. Put differently,
# this means that the integration bounds for the innermost integral can depend on all values of the other integration values.
def bound_func(i, tmins, tmaxs):
    # this function determines the integral bounds of the i-th pdf, given the lists of minimal and maximal timestmaps of all events
    def bound_func_inner(*xs):
        upper_bound = min(tmaxs[i:])

        if len(xs) > 0:
            lower_bound = max(tmins[i], xs[0])
        else:
            lower_bound = tmins[i]

        return lower_bound, upper_bound
    return bound_func_inner


def bounds_proper(tmins, tmaxs):
    # return sequence of functions that return integration bounds
    # First element gives bounds for the innermost integral, and can depend on all other integration variables.
    # Last element gives bounds for the outermost integral, which is the first element we add to the list.

    # The tmins and tmaxs are in the order outermost integral to innermost integral.

    num_integrals = len(tmins)

    # count the integrals from outermost (0) to innermost (num_integrals - 1)
    bounds = []
    for i in range(num_integrals):
        bounds.insert(0, bound_func(i, tmins, tmaxs))

    return bounds

def probability(pdfs, tmins, tmaxs):
    """
    pdfs: list of functions where the i-th function gives the pdf of the i-th interval
    tmins, tmaxs: list of floats where the i-th float is the lower / upper bound of the i-th interval
    """
    integrand = get_integrand(*pdfs)
    bounds = bounds_proper(tmins, tmaxs) # bounds_for_scipy(tmins, tmaxs)
    area = nquad(integrand, bounds)
    return area

#whenever we define a new event, we use either the event_uniform or the event_normal function
def event_uniform(lower, upper):
    return {
        "p": construct_uniform_pdf(lower, upper),
        "lower": lower,
        "upper": upper
    }


def event_normal(mean, std):
    #we set lower and upper bound to +- 4*std
    lower = mean + 4 * std
    upper = mean - 4 * std

    return {
        "p": construct_uniform_pdf(mean, std),
        "lower": lower,
        "upper": upper
    }


#given a list of events generated with event_uniform or event_normal, compute probability of the given ordering in the list
def prob_nice(*events):
    # events is list of arguments

    probs = [events[i]["p"] for i in range(len(events))]
    tmins = [events[i]["lower"] for i in range(len(events))]
    tmaxs = [events[i]["upper"] for i in range(len(events))]

    probs.reverse()  # because of how nquad works

    return probability(probs, tmins, tmaxs)


#EXAMPLE
e2 = event_uniform(3,5)
e3 = event_uniform(6,8)
e4 = event_uniform(4,7)

integral = prob_nice(e2,e4,e3)