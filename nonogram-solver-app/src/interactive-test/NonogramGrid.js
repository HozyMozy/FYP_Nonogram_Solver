import React, { useState } from 'react';
import './NonogramGrid.css'

const NonogramGrid = ({ rows, columns, rowConstraints, colConstraints }) => {

  const [gridData, setGridData] = useState(createInitialGrid(rows, columns));

  function createInitialGrid(rows, columns) {
    const initialGrid = [];
    for (let i = 0; i < rows; i++) {
      const row = Array(columns).fill(0);
      initialGrid.push(row);
    }
    return initialGrid;
  }

  function handleCellClick(row, col) {
    const updatedGrid = [...gridData];
    updatedGrid[row][col] = updatedGrid[row][col] === 1 ? 0 : 1; // Toggle cell state
    setGridData(updatedGrid);
  }

  return (
    <div className="nonogram-grid">
      {gridData.map((row, rowIndex) => (
        <div key={rowIndex} className="row">
          {row.map((cell, colIndex) => (
            <div
              key={colIndex}
              className={`cell ${cell === 1 ? 'filled' : ''}`}
              onClick={() => handleCellClick(rowIndex, colIndex)}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default NonogramGrid;