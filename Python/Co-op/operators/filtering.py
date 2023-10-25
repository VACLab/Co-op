import pandas as pd

#- Function to simulate 'filtering' operation
def filtering(constraints, S):
    in_set = S
    ex_set = S
    for i, val in enumerate(constraints):
        in_vals = list(filter(val[1], S[val[0]].tolist()))
        in_set = in_set.loc[S[val[0]].isin(in_vals)]
        ex_set = ex_set.loc[~S[val[0]].isin(in_vals)]
    return in_set, ex_set

#- Function to simulate 'groupby' operation
def groupby(constraints, S):
    groups = []
    for i, val in enumerate(constraints):
        print(val[0])
        print(val[1])
        print(S[val[0]])
        fvals = list(filter(val[1], S[val[0]].tolist()))
        new_group = S.loc[S[val[0]].isin(fvals)]
        groups.append(new_group)
    return groups

