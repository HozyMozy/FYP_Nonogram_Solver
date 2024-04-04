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
    axios.post("http://localhost:5000/solve", gridDetails)
      .then((response) => {
        const solvedGrid = response.data.solved_grid;
        setSolvedGrid(solvedGrid);
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    setSolved({solved:true})
  };
/*
  const handleSubmit = (event) => {
      event.preventDefault();
      const updatedColConstraints = col_constraints.col.map((con, colIndex) => {
        const inputElement = document.getElementById("colcon" + colIndex);
        console.log(inputElement)
        const inputValue = inputElement ? inputElement.value : "";
        return stringToArray(inputValue);
      });
      const updatedRowConstraints = row_constraints.row.map((row, rowIndex) => {
          const inputElement = document.getElementById("rowcon"+rowIndex);
          const inputValue = inputElement ? inputElement.value : "";
          return stringToArray(inputValue);
      })
      setColConstraints({ col: updatedColConstraints });
      setRowConstraints({row: updatedRowConstraints});
      console.log(col_constraints)
  };
*/
  function handleSubmit(e){
      e.preventDefault();
      const form = e.target;
      const formData = new FormData(form);
      const formJson = Object.fromEntries(formData.entries());
      console.log(form)
      console.log(formData)
      console.log(formJson)
  }

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
                                  {col_constraints.col.map((con, colIndex) => (
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
                              {row_constraints.row.map((row, rowIndex) => (
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
              <button type="submit">Change Constraints</button>
              <button type="button" onClick={handleSolveClick}>Solve</button>
              <button type="button" onClick={handleResetClick}>Reset</button>
          </form>
      )
  }



    const displaySolvedTable = () => {
      return (
          <form method="post" onSubmit={handleSubmit}>
              <table className="table-container">
                  <tbody>
                  <tr className="constraints-row">
                      <td className="constraint-cell"></td>
                      <td>
                          <table>
                              <tbody>
                              <tr>
                                  {col_constraints.col.map((con, colIndex) => (
                                      <td><input
                                          className="constraint-cell"
                                          name={"colcon"+colIndex}
                                          type="text"
                                          defaultValue={con.toString()}>
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
                              {row_constraints.row.map((row, rowIndex) => (
                                  <tr>
                                      <td><input
                                          className="constraint-cell"
                                          name={"rowcon"+rowIndex}
                                          type="text"
                                          defaultValue={row.toString()}
                                      >
                                      </input></td>
                                  </tr>
                              ))}
                              </tbody>
                          </table>
                      </td>
                      <td>
                          <table className="nonogram-cells">
                              <tbody>
                              {solvedGrid.map((row, rowIndex) =>(
                                  <tr>
                                      {row.map((col, colindex) => (
                                          <td
                                              className={col === 1 ? "grid-cell black-cell" : "grid-cell white-cell"}
                                              onMouseOver={highlightConstraints(colindex, rowIndex)}
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
              <button type="submit">Change Constraints</button>
              <button type="button" onClick={handleSolveClick}>Solve</button>
              <button type="button" onClick={handleResetClick}>Reset</button>
          </form>
      )
  };

  let defaultOrSolved;
  if (solved.solved) {
      defaultOrSolved = displaySolvedTable()
  } else {
      defaultOrSolved = displayDefaultTable()
  }

  return (
    <div>
      <h1>Nonogram Solver</h1>
        <div>{defaultOrSolved}</div>
    </div>
  );
}

export default App;
