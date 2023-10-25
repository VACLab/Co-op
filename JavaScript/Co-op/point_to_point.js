//- Function to calculate the Euclidean distance between two vectors p and q
function euclideanDistance(p, q) {
    return Math.sqrt(p.reduce((sum, pi, i) => sum + Math.pow(pi - q[i], 2), 0));
  }
  
//- Function to calculate pairwise distance
function pd(p, q, measure = null, func = null) {
    if (measure === 'euclidean' || measure === null) {
      return euclideanDistance(p, q);
    } else if (measure === 'customize' && func !== null) {
      return func(p, q);
    } else if (measure === 'customize' && func === null) {
      return euclideanDistance(p, q);
    } else {
      // Add your custom distance measures here
      // For example, for a "manhattan" measure:
      // return p.reduce((sum, pi, i) => sum + Math.abs(pi - q[i]), 0);
      return null;
    }
  }
  
//- Function to calculate weighted pairwise distance
function pd_w(p, q, weights, measure = null, func = null) {
    const weightedP = p.map((pi, i) => pi * weights[i]);
    const weightedQ = q.map((qi, i) => qi * weights[i]);
    return pd(weightedP, weightedQ, measure, func);
  }
  