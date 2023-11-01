import React, { useState } from "react";
import axios from "axios";

function App() {
  const [solvedGrid, setSolvedGrid] = useState([]);

  const R = 9;
  const C = 5;

  const handleSolveClick = () => {
    axios.post("http://localhost:5000/solve", {
        R,
        C,
      })
      .then((response) => {
        const solvedGrid = response.data.solved_grid;
        setSolvedGrid(solvedGrid);
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div>
      <h1>Nonogram Solver App</h1>
      <button onClick={handleSolveClick}>Solve</button>
      <div>
        {solvedGrid.map((row, rowIndex) => (
          <div key={rowIndex}>
            {row.map((cell, colIndex) => (
              <span key={colIndex}>{cell === 1 ? "X" : "O"}</span>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;