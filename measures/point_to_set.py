import point_to_point as p2p
import pandas as pd

#- Function to calculate the average pairwise distance for a point p and a set of points S
def pd_avg(p, S, measure=None, function=None):
    res = 0
    for index, row in S.iterrows():
        res += p2p.pd(p, row.tolist(), measure, function)
    return res/len(S)

#- Function to calculate the weighted average pairwise distance for a point p and a set of points S
def pd_avg_w(p, S, weights, measure=None, function=None):
    res = 0
    for index, row in S.iterrows():
        res += p2p.pd_w(p, row.tolist(), weights, measure, function)
    return res/len(S)

