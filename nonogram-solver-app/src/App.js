import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [solvedGrid, setSolvedGrid] = useState([]);
  const [gridSize, setGridSize] = useState({ R: 9, C: 5 }); // Initial grid size

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

  // Function to dynamically calculate grid columns based on grid size
  const calculateGridColumns = () => {
    return `repeat(${gridSize.C}, 40px)`;
  };

  return (
    <div>
      <h1>Nonogram Solver App</h1>
      <button onClick={handleSolveClick}>Solve</button>
      <div className="grid-container" style={{ gridTemplateColumns: calculateGridColumns() }}>
        {solvedGrid.map((row, rowIndex) => (
          <div key={rowIndex} className="grid-row">
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
