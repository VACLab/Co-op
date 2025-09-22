import numpy as np
from scipy.spatial.distance import pdist


#- Function to calculate point to point to point expotional similarity
def point_similarity(p, q, measure=None, function=None):
    if measure == 'euclidean' or measure == None:
        return np.exp(-pdist(np.vstack([p, q]))[0])
    elif measure == 'customize' and function != None:
        return np.exp(-function(p, q))
    elif measure == 'customize' and function == None:
        return np.exp(-pdist(np.vstack([p, q]))[0])
    else:
        return np.exp(-pdist(np.vstack([p, q]), measure)[0])

#- Function to calculate point to set dissimilarity
def point_set_dissimilarity(p, S, measure=None, function=None):
    res = 0
    for index, row in S.iterrows():
        res += (1 - point_similarity(p, row.tolist(), measure, function))
    return res

#- Function to calculate set to set dissimilarity
def set_dissimilarity(S1, S2, measure=None, function=None):
    res = 0
    for index, row in S1.iterrows():
        res += point_set_dissimilarity(row.tolist(), S2, measure, function)
    return res

#- Function to calculate the overall d score between two subsets
def get_d_score(S1, S2, measure=None, function=None):
    res = set_dissimilarity(S1, S2, measure, function) / (len(S1) + len(S2))
    return res

#- Function to calculate the counterfactual guidance of three subsets under user-selected variables
def get_cf_guidance_score(in_set, cf_set, rem_set, included_variables, measure=None, function=None):
    S1 = in_set[included_variables]
    S2 = cf_set[included_variables]
    S3 = rem_set[included_variables]
    d_in_cf = get_d_score(S1, S2, measure, function)
    d_in_rem = get_d_score(S1, S3, measure, function)
    res = 0.5 * (d_in_cf + np.sqrt(d_in_cf * d_in_rem))
    return res

#- Get subset distribution score for any two subsets
def get_distribution_score(S1, S2):
    size_difference = len(S1) / (len(S1) + len(S2))
    res = 1 - 2 * abs(size_difference - 0.5)
    return res
