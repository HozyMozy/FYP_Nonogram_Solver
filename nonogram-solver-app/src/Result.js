import React from "react";

function Result() {
  const R = 9;
  const C = 5;

  function solvePic(grid, x, y) {
    // Your existing nonogram solver function
    // ...

    // For simplicity, let's assume it returns the solved grid
    return grid;
  }

  const grid = solvePic([...], 0, 0);

  return (
    <div>
      <h1>Nonogram Solver Result</h1>
      <div>
        {grid.map((row, rowIndex) => (
          <div key={rowIndex}>
            {row.map((cell, colIndex) => (
              <span key={colIndex}>{cell === 1 ? "X" : " "}</span>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Result;