# Co-op

Co-op is a python library consists of a set of measures and operators that can compute counterfactual subsets of input dataset for designing and implementing visualization systems.

See the paper for more details about the subset computation theory, operator-based model, measures, and operators.

Still NOT uploaded to PYPI currently to meet the anonymity requirements, will upload it after the review cycle.

Import packages directly if you want to use it. Import operators package only if you've implemented your own measures.

A JavaScript implementation of Co-op is attached in the folder ./JavaScript as well.

## Usage

Usage demo for filtering operators is as follows:

```
def filtering_usage_demo():
    data = pandas.DataFrame([
        [800,    1000],
        [1200,    12000],
        [3600,    36000],
        [500,    15000],
        [100,    12000]
    ], columns=['profit', 'sales'])

    cstr1 = ['sales', geq_constraint]
    cstr2 = ['sales', geq_constraint_10000]
    cstr = [cstr1, cstr2]

    in_set, ex_set = filtering.filtering([cstr1], data)
    in_groups = filtering.groupby(cstr, data)

    return in_set, ex_set, in_groups
```

Some examples for the filtering constriants are described as follows:

```
def less_constraint(point, number=1):
    return point < number


def leq_constraint(point, number=1):
    return point <= number


def greater_constraint(point, number=1):
    return point > number


def geq_constraint(point, number=1):
    return point >= number


def geq_constraint_10000(point, number=10000):
    return point >= number


def geq_constraint_30000(point, number=30000):
    return point >= number
```

Usage demo for counterfactual operators is as follows:

```
def cf_usage_demo():
    data = pandas.DataFrame([
        [800,    1000],
        [1200,    12000],
        [3600,    36000],
        [500,    15000],
        [100,    12000]
    ], columns=['profit', 'sales'])

    cstr = ['sales', geq_constraint_30000]

    in_set, ex_set = filtering.filtering([cstr], data)

    Measure = [[1, customized_measure]]
    cf_set, ex_set = counterfactual.counterfactual(in_set, ex_set, Measure)

    return in_set, cf_set, ex_set
```

An example of customized measure computation is as follows:

```
def customized_measure(p, S, weights=[1, 0.5, 3, 8, 21], measure='mahalanobis', dims=['a', 'b', 'c']):
    res = 0
    target_data = S.loc[:, dims]
    for index, row in target_data.iterrows():
        res += p2p.pd_w(p, row.tolist(), weights)
    return res
```
