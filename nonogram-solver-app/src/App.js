import React, {useState} from "react";
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


    const [solvedGrid, setSolvedGrid] = useState([[]]);
    const [gridDetails, setGridDetails] = useState({R: 9, C: 5, row: default_row, col: default_col}); // Initial grid size
    const [row_constraints, setRowConstraints] = useState({row: default_row});
    const [col_constraints, setColConstraints] = useState({col: default_col});
    const [solved, setSolved] = useState({solved: false});
    const initial_grid = Array.from({length: gridDetails.R}, () =>
        Array.from({length: gridDetails.C}, () => 0));
    const [default_grid, setDefaultGrid] = useState({grid: initial_grid})

  const handleSolveClick = () => {
        if (!(solved.solved))
            console.log(gridDetails)
            axios.post("http://localhost:5000/solve", gridDetails).then((response) => {
                const solvedGrid = response.data.solved_grid;
                setSolvedGrid(solvedGrid);
                setDefaultGrid({grid: solvedGrid})
                console.log(response.data);
            })
                .catch((error) => {
                    console.error("Error:", error);
                });
            setSolved({solved:true})
    };

  function handleSubmit(e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  const formJson = Object.fromEntries(formData.entries());


  const { rows, cols, ...constraints } = formJson;


  const rowConstraints = Object.keys(constraints)
    .filter(key => key.startsWith("rowcon"))
    .map(key => stringToArray(formJson[key]));

  const colConstraints = Object.keys(constraints)
    .filter(key => key.startsWith("colcon"))
    .map(key => stringToArray(formJson[key]));

  const newRows = parseInt(rows);
  const newCols = parseInt(cols);

  while (rowConstraints.length < newRows) {
    rowConstraints.push([]);
  }
  while (rowConstraints.length > newRows) {
    rowConstraints.pop();
  }

  // Adjust the length of colConstraints
  while (colConstraints.length < newCols) {
    colConstraints.push([]);
  }
  while (colConstraints.length > newCols) {
    colConstraints.pop();
  }

  const initial_grid = Array.from({length: newRows}, () =>
        Array.from({length: newCols}, () => 0));


  setGridDetails({
    R: newRows,
    C: newCols,
    row: rowConstraints,
    col: colConstraints
  });
  setDefaultGrid({grid: initial_grid});
  setSolved({solved: false})
  }

  const removeMistakes = () => {
      if (!(solved.solved)){
          axios.post("http://localhost:5000/solve", gridDetails).then((response) => {
              const solvedGrid = response.data.solved_grid;
              setSolvedGrid(solvedGrid);
              console.log(response.data);
          })
            .catch((error) => {
                console.error("Error:", error);
            });
          setSolved({solved:true})
      }

      const newGrid = default_grid.grid.map((row, rowIndex) => {
            return row.map((cell, colIndex) => {
                if (cell === 1 && solvedGrid[rowIndex][colIndex] !== 1) {
                    return 0; // Replace 1 with 0 if it's a mistake
                } else {
                    return cell; // Keep the cell unchanged
                }
                });
        });

      setDefaultGrid({grid: newGrid});



    };

  function stringToArray(data) {
      return data.split(",").map(item => parseInt(item.trim(), 10));
  }

  function highlightConstraints(colindex, rowIndex) {
        return undefined;
    }

    const handleCellChange = (rowIndex, colIndex) => {
      const updatedGrid = default_grid.grid.map((row, i) => {
        if (i === rowIndex) {
          return row.map((col, j) => {
            if (j === colIndex) {
              // Toggle the value of the cell (0 to 1 or 1 to 0)
              return col === 1 ? 0 : 1;
            }
            return col;
          });
        }
        return row;
      });
      setDefaultGrid({grid: updatedGrid});
};

  const handleResetClick = () => {
      setDefaultGrid({grid: initial_grid})
      setSolved({solved: false})
  }

    const displayDefaultTable = () => {
      return (
          <form className="table-container" method="post" onSubmit={handleSubmit}>
              <table className="table-container">
                  <tbody>
                  <tr className="constraints-row">
                      <td></td>
                      <td className="constraints-row">
                          <table>
                              <tbody>
                              <tr>
                                  {gridDetails.col.map((con, colIndex) => (
                                      <td><input
                                          className="constraint-cell"
                                          name={"colcon"+colIndex}
                                          type="text" defaultValue={con.toString()}>
                                      </input></td>
                                  ))}
                              </tr>
                              </tbody>
                          </table>
                      </td>
                  </tr>
                  <tr>
                      <td>
                          <table className="constraints-row">
                              <tbody>
                              {gridDetails.row.map((row, rowIndex) => (
                                  <tr>
                                      <td><input
                                          className="constraint-cell"
                                          name={"rowcon"+rowIndex}
                                          type="text"
                                          defaultValue={row.toString()}>
                                      </input></td>
                                  </tr>
                              ))}
                              </tbody>
                          </table>
                      </td>
                      <td>
                          <table className="nonogram-cells">
                              <tbody>
                              {default_grid.grid.map((row, rowIndex) =>(
                                  <tr>
                                      {row.map((col, colIndex) => (
                                          <td
                                              className={col === 1 ? "grid-cell black-cell" : "grid-cell white-cell"}
                                              onMouseDown={() => handleCellChange(rowIndex, colIndex)}
                                          >
                                          </td>
                                      ))}
                                  </tr>
                              ))}
                              </tbody>
                          </table>
                      </td>
                  </tr>
                  </tbody>
              </table>
              <button type="submit">Set Grid Size/Constraints</button>
              <button type="button" onClick={handleSolveClick}>Solve</button>
              <button type="button" onClick={handleResetClick}>Reset</button>
              <button type="button" onClick={removeMistakes}>Remove Mistakes</button>
              <div>
                  <b>
                  <label>
                      Rows:
                      <input type="text" name="rows" defaultValue={gridDetails.R.toString()}></input>
                  </label>
                  <label>
                      Columns:
                      <input type="text" name="cols" defaultValue={gridDetails.C.toString()}></input>
                  </label>
                  </b>
              </div>
          </form>
      )
  }

  return (
    <div>
      <h1>Nonogram Solver</h1>
        <div>{displayDefaultTable()}</div>
        <div>Note: Press set grid size once after changing size, then again after setting constraints.</div>
        <div>Currently the solver takes over 10 minutes for puzzles over 15x15, depending on how many blank spaces there are.</div>
    </div>
  );
}

export default App;
