//- Function to simulate 'filtering' operation
function filtering(constraints, S) {
    let inSet = [...S];
    let exSet = [...S];
  
    constraints.forEach(([col, filterFunc]) => {
      const inVals = S.map(row => row[col]).filter(filterFunc);
  
      inSet = inSet.filter(row => inVals.includes(row[col]));
      exSet = exSet.filter(row => !inVals.includes(row[col]));
    });
  
    return [inSet, exSet];
  }
  
//- Function to simulate 'groupby' operation
function groupby(constraints, S) {
    const groups = [];
  
    constraints.forEach(([col, filterFunc]) => {
      const fVals = S.map(row => row[col]).filter(filterFunc);
      const newGroup = S.filter(row => fVals.includes(row[col]));
  
      groups.push(newGroup);
    });
  
    return groups;
  }

//* OPTIONAL FUNCTION TO PRINT DATAFRAME
function printFilteredDataFrame(data, label) {
    console.log(label);
    if (Array.isArray(data) && Array.isArray(data[0])) {
      // Handle nested arrays (for 'groupby' function)
      data.forEach((group, index) => {
        console.log(`Group ${index + 1}:`);
        if (group.length === 0) {
          console.log("Empty DataFrame");
        } else {
          const keys = Object.keys(group[0]);
          console.log(keys.join(" | "));
          console.log("-".repeat(keys.join(" | ").length));
          group.forEach(row => {
            console.log(Object.values(row).join(" | "));
          });
        }
        console.log();
      });
    } else {
      // Handle single array (for 'filtering' function)
      if (data.length === 0) {
        console.log("Empty DataFrame");
      } else {
        const keys = Object.keys(data[0]);
        console.log(keys.join(" | "));
        console.log("-".repeat(keys.join(" | ").length));
        data.forEach(row => {
          console.log(Object.values(row).join(" | "));
        });
      }
    }
    console.log('\n');
  }