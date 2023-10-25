
function counterfactual(inSet, exSet, measures) {
    const inLen = inSet.length;
    const exLen = exSet.length;
    const cfLen = exLen > inLen ? inLen : Math.ceil(exLen / 2);
  
    const results = Array.from({ length: exLen }, () => 0);
    const resultsId = exSet.map((_, index) => index);
  
    measures.forEach(([multiplier, measureFunc]) => {
      for (let j = 0; j < exLen; j++) {
        results[j] += multiplier * measureFunc(exSet[j], inSet);
      }
    });
  
    // Sort indices by their corresponding results
    const sortedId = results
      .map((value, index) => [value, index])
      .sort(([a], [b]) => a - b)
      .map(([, index]) => index);
  
    // Get counterfactual set (cfSet) and remaining set (remSet)
    const cfId = sortedId.slice(0, cfLen);
    const cfSet = cfId.map(id => exSet[id]);
    const remSet = resultsId.filter(id => !cfId.includes(id)).map(id => exSet[id]);
  
    return [cfSet, remSet];
  }
  
function resize(cfSet, inSet, remSet, size, measures) {
    const cfLen = cfSet.length;
    let remSetNew = [];
    let cfSetNew = [];
  
    const calcResults = (set) => {
      const results = Array.from({ length: set.length }, () => 0);
      for (const [multiplier, measureFunc] of measures) {
        for (let j = 0; j < set.length; j++) {
          results[j] += multiplier * measureFunc(set[j], inSet);
        }
      }
      return results;
    };
  
    if (size < cfLen) {
      const results = calcResults(cfSet);
      const sortedId = results
        .map((val, idx) => [val, idx])
        .sort((a, b) => b[0] - a[0])
        .map(([, idx]) => idx);
  
      const minusId = sortedId.slice(0, cfLen - size);
      remSetNew = remSet.concat(minusId.map(id => cfSet[id]));
      cfSetNew = cfSet.filter((_, idx) => !minusId.includes(idx));
  
    } else if (size > cfLen) {
      const results = calcResults(remSet);
      const sortedId = results
        .map((val, idx) => [val, idx])
        .sort((a, b) => a[0] - b[0])
        .map(([, idx]) => idx);
  
      const addId = sortedId.slice(0, size - cfLen);
      cfSetNew = cfSet.concat(addId.map(id => remSet[id]));
      remSetNew = remSet.filter((_, idx) => !addId.includes(idx));
  
    } else if (size === cfLen) {
      [cfSetNew, remSetNew] = counterfactual(inSet, remSet.concat(cfSet), measures);
    }
  
    return [cfSetNew, remSetNew];
  }