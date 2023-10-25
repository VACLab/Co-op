//- Function to calculate the variance of an array S
function variance(S) {
  const n = S.length;
  const mean = S.reduce((acc, val) => acc + val, 0) / n;
  return S.map(x => Math.pow(x - mean, 2)).reduce((acc, val) => acc + val, 0) / n;
}

//- Function to calculate the weighted variance of an array S with weights
function variance_w(S, weights) {
  const n = S.length;
  const mean = S.reduce((acc, val) => acc + val, 0) / n;
  const variance = S.map(x => Math.pow(x - mean, 2)).reduce((acc, val) => acc + val, 0) / n;
  return variance * weights.reduce((acc, val) => acc + val, 0);
}

//- Function to calculate the entropy of an array S
function entropy(S) {
  const sum = S.reduce((acc, val) => acc + val, 0);
  const probabilities = S.map(x => x / sum);
  return -probabilities.map(p => p * Math.log(p)).reduce((acc, val) => acc + val, 0);
}

//- Function to calculate the weighted entropy of an array S with weights
function entropy_w(S, weights) {
  const sum = S.reduce((acc, val) => acc + val, 0);
  const probabilities = S.map(x => x / sum);
  const entropy = -probabilities.map(p => p * Math.log(p)).reduce((acc, val) => acc + val, 0);
  return entropy * weights.reduce((acc, val) => acc + val, 0);
}
