import React, { useState, useEffect, useRef } from 'react'
import './SudokuBoard.css'

function SudokuBoard({ grid, puzzle, solution, onCellChange, disabled = false }) {
  const [selectedCell, setSelectedCell] = useState(null)
  const boardRef = useRef(null)

  const handleCellClick = (row, col) => {
    if (disabled) return
    setSelectedCell({ row, col })
  }

  const moveSelection = (direction) => {
    if (!selectedCell) return

    const { row, col } = selectedCell
    let newRow = row
    let newCol = col

    if (direction === 'next') {
      if (col < 8) {
        newCol = col + 1
      } else if (row < 8) {
        newRow = row + 1
        newCol = 0
      }
    }

    setSelectedCell({ row: newRow, col: newCol })
  }

  const handleKeyDown = (e) => {
    if (!selectedCell || disabled) return

    const { row, col } = selectedCell
    const isLocked = puzzle && puzzle[row][col] !== 0

    if (isLocked) return

    if (e.key >= '1' && e.key <= '9') {
      onCellChange(row, col, parseInt(e.key))
    } else if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') {
      onCellChange(row, col, 0)
    } else if (e.key === 'ArrowUp' && row > 0) {
      setSelectedCell({ row: row - 1, col })
    } else if (e.key === 'ArrowDown' && row < 8) {
      setSelectedCell({ row: row + 1, col })
    } else if (e.key === 'ArrowLeft' && col > 0) {
      setSelectedCell({ row, col: col - 1 })
    } else if (e.key === 'ArrowRight' && col < 8) {
      setSelectedCell({ row, col: col + 1 })
    }
  }

  useEffect(() => {
    if (boardRef.current) {
      boardRef.current.focus()
    }
  }, [])

  const isLocked = (row, col) => {
    return puzzle && puzzle[row][col] !== 0
  }

  const getBoxClass = (row, col) => {
    const boxRow = Math.floor(row / 3)
    const boxCol = Math.floor(col / 3)
    return `box-${boxRow}-${boxCol}`
  }

  const isError = (row, col, val) => {
    if (val === 0 || !solution) return false
    return solution[row][col] !== val
  }

  const isRelated = (row, col) => {
    if (!selectedCell) return false
    const { row: sRow, col: sCol } = selectedCell
    if (row === sRow && col === sCol) return false
    if (row === sRow) return true
    if (col === sCol) return true

    const sBoxRow = Math.floor(sRow / 3)
    const sBoxCol = Math.floor(sCol / 3)
    const boxRow = Math.floor(row / 3)
    const boxCol = Math.floor(col / 3)

    return sBoxRow === boxRow && sBoxCol === boxCol
  }

  const isSameValue = (val) => {
    if (!selectedCell || val === 0) return false
    const { row, col } = selectedCell
    const selectedValue = grid[row][col]
    return selectedValue !== 0 && val === selectedValue
  }

  return (
    <div
      className="sudoku-board-container"
      ref={boardRef}
      tabIndex={0}
      onKeyDown={handleKeyDown}
    >
      <div className="sudoku-board">
        {grid.map((row, rowIdx) => (
          <div key={rowIdx} className="sudoku-row">
            {row.map((cell, colIdx) => {
              const locked = isLocked(rowIdx, colIdx)
              const selected = selectedCell && selectedCell.row === rowIdx && selectedCell.col === colIdx
              const boxClass = getBoxClass(rowIdx, colIdx)
              const error = !locked && isError(rowIdx, colIdx, cell)
              const related = isRelated(rowIdx, colIdx)
              const sameValue = isSameValue(cell)

              let cellClass = `sudoku-cell ${boxClass}`
              if (locked) cellClass += ' locked'
              if (selected) cellClass += ' selected'
              if (error) cellClass += ' error'
              if (related) cellClass += ' related'
              if (sameValue && !selected && !error) cellClass += ' same-value'

              return (
                <input
                  key={`${rowIdx}-${colIdx}`}
                  type="text"
                  inputMode="numeric"
                  className={cellClass}
                  value={cell === 0 ? '' : cell}
                  readOnly={locked || disabled}
                  onClick={() => handleCellClick(rowIdx, colIdx)}
                  onChange={(e) => {
                    const value = e.target.value
                    if (value === '' || (value >= '1' && value <= '9')) {
                      onCellChange(rowIdx, colIdx, value === '' ? 0 : parseInt(value))
                    }
                  }}
                  maxLength={1}
                />
              )
            })}
          </div>
        ))}
      </div>
    </div>
  )
}

export default SudokuBoard
