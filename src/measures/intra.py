import numpy as np
import scipy.stats

#- Function to calculate the variance of an array S
def variance(S):
    return np.var(S).sum()

#- Function to calculate the weighted variance of an array S with weights
def variance_w(S, weights):
    return np.multiply(np.var(S), weights).sum()

#- Function to calculate the entropy of a n array S
def entropy(S):
    return scipy.stats.entropy(S).sum()

#- Function to calculate the weighted entropy of an array S with weights
def entropy_w(S, weights):
    return np.multiply(scipy.stats.entropy(S), weights).sum()
