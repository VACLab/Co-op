import point_to_set as p2s
import numpy as np
import pandas as pd
import scipy.stats
from sklearn.preprocessing import MinMaxScaler

# Calculates the Gower distance matrix between two datasets
def gower_distance_matrix(data1, data2, numerical_cols, categorical_cols):
    n1 = data1.shape[0]
    n2 = data2.shape[0]
    dm = np.zeros((n1, n2))

    # Scale numerical data to a [0, 1] range for distance calculation
    df_combined = pd.concat([data1[numerical_cols], data2[numerical_cols]])
    scaler = MinMaxScaler()
    df_combined_scaled = scaler.fit_transform(df_combined)
    data1_num_scaled = scaler.transform(data1[numerical_cols])
    data2_num_scaled = scaler.transform(data2[numerical_cols])

    for i in range(n1):
        for j in range(n2):
            num_dist_sum = np.sum(np.abs(data1_num_scaled[i, :] - data2_num_scaled[j, :]))
            cat_dist_sum = np.sum(data1[categorical_cols].iloc[i] != data2[categorical_cols].iloc[j])
            dm[i, j] = (num_dist_sum + cat_dist_sum) / (len(numerical_cols) + len(categorical_cols))
    return dm

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
