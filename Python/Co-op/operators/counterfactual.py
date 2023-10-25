import math
import pandas as pd

def counterfactual(in_set, ex_set, measures):
    in_len = in_set.shape[0]
    ex_len = ex_set.shape[0]
    cf_len = in_len if ex_len > in_len else math.ceil(ex_len / 2)

    results = [0] * ex_len
    results_id = ex_set.index
    for id, measure in enumerate(measures):
        j = 0
        for index, row in ex_set.iterrows():
            results[j] += measure[0]*measure[1](row, in_set)
            j += 1

    sorted_id = sorted(range(len(results)),
                       key=lambda k: results[k], reverse=False)
    cf_id = list(results_id[sorted_id[:cf_len]])
    cf_set = ex_set.loc[cf_id]

    results_id = list(results_id)
    for i in cf_id:
        results_id.remove(i)
    rem_set = ex_set.loc[results_id]

    return cf_set, rem_set


def resize(cf_set, in_set, rem_set, size, measures):
    cf_len = cf_set.shape[0]

    if size < cf_len:
        results = [0] * cf_len
        for id, measure in enumerate(measures):
            j = 0
            for index, row in cf_set.iterrows():
                results[j] += measure[0]*measure[1](row, in_set)
                j += 1

        sorted_id = sorted(range(len(results)),
                           key=lambda k: results[k], reverse=True)
        cf_id = list(cf_set.index)
        minus_id = list(cf_id[sorted_id[:(cf_len - size)]])
        rem_set_new = rem_set.append(cf_set.loc[minus_id])

        for i in minus_id:
            cf_id.remove(i)
        cf_set_new = cf_set.loc[cf_id]

    elif size > cf_len:
        results = [0] * cf_len
        for id, measure in enumerate(measures):
            j = 0
            for index, row in rem_set.iterrows():
                results[j] += measure[0]*measure[1](row, in_set)
                j += 1

        sorted_id = sorted(range(len(results)),
                           key=lambda k: results[k], reverse=False)
        ex_id = list(rem_set.index)
        add_id = list(ex_id[sorted_id[:(size - cf_len)]])
        cf_set_new = cf_set.append(rem_set.loc[add_id])

        for i in add_id:
            ex_id.remove(i)
        rem_set_new = rem_set.loc[ex_id]

    elif size == cf_len:
        cf_set_new, rem_set_new = counterfactual(
            in_set, rem_set.append(cf_set), measures)

    return cf_set_new, rem_set_new
