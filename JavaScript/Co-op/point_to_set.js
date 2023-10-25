//- Function to calculate the average pairwise distance for a point p and a set of points S
function pd_avg(p, S, measure = null, func = null) {
    let res = 0;
    S.forEach(row => {
      res += pd(p, Object.values(row), measure, func);
    });
    return res / S.length;
  }
  
  //- Function to calculate the weighted average pairwise distance for a point p and a set of points S
function pd_avg_w(p, S, weights, measure = null, func = null) {
    let res = 0;
    S.forEach(row => {
      res += pd_w(p, Object.values(row), weights, measure, func);
    });
    return res / S.length;
  }
  
console.log("point_to_set.js loaded");