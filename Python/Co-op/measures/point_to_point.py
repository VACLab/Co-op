import numpy as np
from scipy.spatial.distance import pdist

#- Function to calculate pairwise distance
def pd(p, q, measure=None, function=None):
    if measure == 'euclidean' or measure == None:
        return pdist(np.vstack([p, q]))[0]
    elif measure == 'customize' and function != None:
        return function(p, q)
    elif measure == 'customize' and function == None:
        return pdist(np.vstack([p, q]))[0]
    else:
        return pdist(np.vstack([p, q]), measure)[0]

#- Function to calculate weighted pairwise distance
def pd_w(p, q, weights, measure=None, function=None):
    return pd(np.multiply(p, weights), np.multiply(q, weights), measure, function)