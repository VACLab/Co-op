import pandas as pd

#- Function to simulate 'union' operation
def union(left_set, right_set, dims):
    return pd.merge(left_set, right_set, on=dims, how='outer')

#- Function to simulate 'difference' operation
def difference(left_set, right_set, dims):
    return pd.merge(left_set, right_set, on=dims)

#- Function to simulate 'intersection' operation
def intersection(left_set, right_set, dims):
    left_set = left_set.append(right_set)
    left_set = left_set.append(right_set)
    return left_set.drop_duplicates(subset=dims, keep=False)

#- Function to simulate 'complement' operation
def complement(data, input_set, dims):
    data = data.append(input_set)
    return data.drop_duplicates(subset=dims, keep=False)
