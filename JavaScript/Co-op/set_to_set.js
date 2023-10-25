//- Function to calculate entropy between two arrays p and q
function s2sEntropy(p, q) {
    let res = 0;
    for(let i = 0; i < p.length; i++) {
        res += p[i] * Math.log(p[i] / q[i]);
    }
    return res;
}

//- Function to calculate the set-to-set distance
function sd(S1, S2, measure = null, func = null) {
    let res = 0;
    S1.forEach(row => {
        res += pd_avg(Object.values(row), S2, measure, func);
    });
    return res;
}

//- Function to calculate the weighted set-to-set distance
function sd_w(S1, S2, weights, measure = null, func = null) {
    let res = 0;
    S1.forEach(row => {
        res += pd_avg_w(Object.values(row), S2, weights, measure, func);
    });
    return res;
}

//- Function to calculate the entropy-based set-to-set distance
function sd_entropy(S1, S2) {
    let res = 0;
    for(let i = 0; i < S1.length; i++) {
        res += s2sEntropy(Object.values(S1[i]), Object.values(S2[i]));
    }
    return res;
}

//- Function to calculate the weighted entropy-based set-to-set distance
function sd_entropy_w(S1, S2, weights) {
    let res = 0;
    for(let i = 0; i < S1.length; i++) {
        const ent = s2sEntropy(Object.values(S1[i]), Object.values(S2[i]));
        res += ent * weights[i];
    }
    return res;
}
