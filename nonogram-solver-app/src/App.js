import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const default_row = [
      [3],
      [1, 1],
      [1, 1],
      [1],
      [5],
      [2, 2],
      [5],
      [5],
      [3]
  ];
  const default_col = [
      [2, 4],
      [1, 5],
      [1, 1, 3],
      [1, 5],
      [7]
  ];
  const [solvedGrid, setSolvedGrid] = useState([]);
  const [gridSize] = useState({ R: 9, C: 5, row: default_row, col: default_col }); // Initial grid size
  const [row_constraints, setRowConstraints] = useState({row: default_row});
  const [col_constraints, setColConstraints] = useState({col: default_col});
  const handleSolveClick = () => {
    axios.post("http://localhost:5000/solve", gridSize)
      .then((response) => {
        const solvedGrid = response.data.solved_grid;
        setSolvedGrid(solvedGrid);
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const calculateGridColumns = () => {
    return `repeat(${gridSize.C}, 40px)`;
  };
  const calculateGridRows = () => {
      return `repeat(${gridSize.R}, 40px)`;
  };

  return (
    <div>
      <h1>Nonogram Solver App</h1>
      <button onClick={handleSolveClick}>Solve</button>
      <div className="grid-container" style={{ gridTemplateColumns: calculateGridColumns()}}>
        {solvedGrid.map((row, rowIndex) => (
          <div key={rowIndex} className="grid-row" style={{gridTemplateRows: calculateGridRows()}}>
            {row.map((cell, colIndex) => (
              <span key={colIndex} className={cell === 1 ? "grid-cell black-cell" : "grid-cell white-cell"}></span>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
