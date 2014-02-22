"""
Useful functions/classes for recipes that might also be used in another 
app/project
"""
from math import sqrt


def wilson_score_interval(ups, downs):
    """
    An implementation of the Wilson score interval 
    (http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval) for
    the purpose of figuring out rankings based on user up-votes or down-votes.
    
    Thank you, possiblywrong, for this implementation:
    http://possiblywrong.wordpress.com/2011/06/05/reddits-comment-ranking-algorithm/
    
    :param ups: number of up-votes for an object (integer)
    :param downs: number of down-votes for the same object (integer)
    :return: float
    """
    z = 1.64485 # 1.0 = 85%, 1.6 = 95%
    
    if ups == 0:
        return -downs
    n = ups + downs
    phat = float(ups) / n
    
    return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)