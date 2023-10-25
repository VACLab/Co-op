import point_to_set as p2s
import numpy as np
import scipy.stats
import pandas as pd

#- Function to calculate the set-to-set distance
def sd(S1, S2, measure=None, function=None):
    res = 0
    for index, row in S1.iterrows():
        res += p2s.pd_avg(row.tolist(), S2, measure, function)
    return res

#- Function to calculate the weighted set-to-set distance
def sd_w(S1, S2, weights, measure=None, function=None):
    res = 0
    for index, row in S1.iterrows():
        res += p2s.pd_avg_w(row.tolist(), S2, weights, measure, function)
    return res

#- Function to calculate the entropy-based set-to-set distance
def sd_entropy(S1, S2):
    return scipy.stats.entropy(S1, S2).sum()

#- Function to calculate the weighted entropy-based set-to-set distance
def sd_entropy_w(S1, S2, weights):
    return np.multiply(scipy.stats.entropy(S1, S2), weights).sum()