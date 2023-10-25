//- Function to simulate 'union' operation
function union(leftSet, rightSet, dims) {
    const mergedSet = [...leftSet, ...rightSet];
    return [...new Set(mergedSet.map(JSON.stringify))].map(JSON.parse);
  }
  
//- Function to simulate 'difference' operation
function difference(leftSet, rightSet, dims) {
    const rightSetStr = new Set(rightSet.map(JSON.stringify));
    return leftSet.filter(item => rightSetStr.has(JSON.stringify(item)));
  }
  
//- Function to simulate 'intersection' operation
function intersection(leftSet, rightSet, dims) {
    const allItems = [...leftSet, ...rightSet, ...rightSet];
    const itemCounts = {};
    
    allItems.forEach(item => {
      const itemStr = JSON.stringify(item);
      itemCounts[itemStr] = (itemCounts[itemStr] || 0) + 1;
    });
  
    return Object.keys(itemCounts).filter(itemStr => itemCounts[itemStr] === 1).map(JSON.parse);
  }
  
  
  
//- Function to simulate 'complement' operation
function complement(data, inputSet, dims) {
    const allItems = [...data, ...inputSet];
    const itemCounts = {};
    
    allItems.forEach(item => {
      const itemStr = JSON.stringify(item);
      itemCounts[itemStr] = (itemCounts[itemStr] || 0) + 1;
    });
  
    return Object.keys(itemCounts).filter(itemStr => itemCounts[itemStr] === 1).map(JSON.parse);
  }
  
//* OPTIONAL FUNCTION TO PRINT DATAFRAME
function printDataFrame(data, label) {
    console.log(label);
    const keys = Object.keys(data[0]);
    console.log(keys.join(" | "));
    console.log("-".repeat(keys.join(" | ").length));
    for (const row of data) {
        console.log(Object.values(row).join(" | "));
    }
    console.log('\n');
  }