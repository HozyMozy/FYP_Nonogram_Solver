import React, {useState} from "react";
import axios from "axios";
import "./App.css";


function App() {
    const default_row = [[3], [1, 1], [1, 1], [1], [5], [2, 2], [5], [5], [3]];
    const default_col = [[2, 4], [1, 5], [1, 1, 3], [1, 5], [7]];

    const trophy_row = [[10], [1,2,2,1], [1,2,2,1], [1,2,2,1], [3,3], [4], [2], [2], [4], [6]];
    const trophy_col = [[4], [1,1], [5,1], [6,2], [1,5], [1,5], [6,2], [5,1], [1,1], [4]];

    const iron_row = [[4], [1], [5], [1,1], [7]];
    const iron_col = [[1], [2], [1,1], [1,1,1], [1,1,1], [1,1,1], [5]];

    const insect_row = [[2,2], [3,1,4], [1,1,4], [6], [7], [6], [5,1], [4,1,1,1], [1,1,1], [1,1,1]]
    const insect_col = [[1,1,1], [1,1,1], [2,1,4], [1,5], [7], [7], [6], [4,1,3], [4,1], [2,2]]

    const [solvedGrid, setSolvedGrid] = useState([[]]);
    const [gridDetails, setGridDetails] = useState({R: 9, C: 5, row: default_row, col: default_col}); // Initial grid, and constraints
    const [solved, setSolved] = useState({solved: false});
    const initial_grid = Array.from({length: gridDetails.R}, () =>
        Array.from({length: gridDetails.C}, () => 0));
    const [default_grid, setDefaultGrid] = useState({grid: initial_grid});

    // Handles solve by sending axios request to back-end, sets solved to true and grid to solved grid.
  const handleSolveClick = () => {
        if (!(solved.solved))
            console.log(gridDetails);
            axios.post("http://localhost:5000/solve", gridDetails).then((response) => {
                const solvedGrid = response.data.solved_grid;
                if (!(solvedGrid === null)) {
                    setSolvedGrid(solvedGrid);
                    setDefaultGrid({grid: solvedGrid});
                    console.log(response.data);
                    setSolved({solved:true});
                }
            })
                .catch((error) => {
                    console.error("Error:", error);
                });

    };


  // Submits the constraints and grid size and makes respective changes to variables
  function handleSubmit(e) {
  e.preventDefault();  // Prevents default submission

  const form = e.target;  // Gets event target
  const formData = new FormData(form);
  const formJson = Object.fromEntries(formData.entries());  // Gets data from form


  const { rows, cols, ...constraints } = formJson;

  // Sets row and column constraints, and also grid size.
  const rowConstraints = Object.keys(constraints)
    .filter(key => key.startsWith("rowcon"))
    .map(key => stringToArray(formJson[key]));

  const colConstraints = Object.keys(constraints)
    .filter(key => key.startsWith("colcon"))
    .map(key => stringToArray(formJson[key]));

  const newRows = parseInt(rows);
  const newCols = parseInt(cols);


  // Adjusts the length of rowConstraints
  while (rowConstraints.length < newRows) {
    rowConstraints.push([]);
  }
  while (rowConstraints.length > newRows) {
    rowConstraints.pop();
  }

  // Adjusts the length of colConstraints
  while (colConstraints.length < newCols) {
    colConstraints.push([]);
  }
  while (colConstraints.length > newCols) {
    colConstraints.pop();
  }

  const initial_grid = Array.from({length: newRows}, () =>
        Array.from({length: newCols}, () => 0));

  // Sets grid details with new values, resets default grid, and sets solved to false
  setGridDetails({
    R: newRows,
    C: newCols,
    row: rowConstraints,
    col: colConstraints
  });
  setDefaultGrid({grid: initial_grid});
  setSolved({solved: false})
  }

  // Removes squares present in default grid but not in solved grid, also sends solve request if not yet solved.

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

  // Toggles cell using indices passed to function
  const handleCellChange = (rowIndex, colIndex) => {
      console.log("cell clicked")
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

  // Resets the grid to an empty grid
  const handleResetClick = () => {
      setDefaultGrid({grid: initial_grid})
      setSolved({solved: false})
  }
  // Wrapper for the display
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

    function loadPuzzle(e) {
        e.preventDefault();  // Prevents default behavior of select element
        const selectedValue = e.target.value.toString();  // Gets the selected value
        console.log(selectedValue);
        if (selectedValue === "lock") {
            const newRows = default_row.length
            const newCols = default_col.length
            setGridDetails({
                R: newRows,
                C: newCols,
                row: default_row,
                col: default_col
            });
            const initial_grid = Array.from({length: newRows}, () =>
                Array.from({length: newCols}, () => 0));
            setDefaultGrid({grid: initial_grid});
            setSolved({solved: false})
        } else if (selectedValue === "iron") {
            const newRows = iron_row.length
            const newCols = iron_col.length
            setGridDetails({
                R: newRows,
                C: newCols,
                row: iron_row,
                col: iron_col
            });
            const initial_grid = Array.from({length: newRows}, () =>
                Array.from({length: newCols}, () => 0));
            setDefaultGrid({grid: initial_grid});
            setSolved({solved: false})
        } else if (selectedValue === "trophy") {
            const newRows = trophy_row.length
            const newCols = trophy_col.length
            setGridDetails({
                R: newRows,
                C: newCols,
                row: trophy_row,
                col: trophy_col
            });
            const initial_grid = Array.from({length: newRows}, () =>
                Array.from({length: newCols}, () => 0));
            setDefaultGrid({grid: initial_grid});
            setSolved({solved: false})
        } else if (selectedValue === "insect") {
            const newRows = insect_row.length
            const newCols = insect_col.length
            setGridDetails({
                R: newRows,
                C: newCols,
                row: insect_row,
                col: insect_col
            });
            const initial_grid = Array.from({length: newRows}, () =>
                Array.from({length: newCols}, () => 0));
            setDefaultGrid({grid: initial_grid});
            setSolved({solved: false})
        }
    }

    // Returns output
  return (
    <div>
      <h1>Nonogram Solver</h1>
        <div>{displayDefaultTable()}</div>
        <div>
            <label>Load Puzzle:
                <select defaultValue="lock" onChange={loadPuzzle}>
                    <option value="lock"> Lock </option>
                    <option value="iron"> Iron </option>
                    <option value="trophy"> Trophy </option>
                    <option value="insect"> Insect </option>
                </select>
            </label>
        </div>
        <div>Note: Press set grid size once after changing size, then again after setting constraints.</div>
        <div>Currently the solver takes over 10 minutes for puzzles over 15x10, depending on how many blank spaces there are.</div>
    </div>
  );
}

export default App;
