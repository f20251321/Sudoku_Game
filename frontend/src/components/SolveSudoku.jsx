import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import SudokuBoard from './SudokuBoard'
import axios from 'axios'
import { API_BASE } from '../config'
import './SolveSudoku.css'

function SolveSudoku() {
  const [mode, setMode] = useState('manual') // 'manual' or 'image'
  const [grid, setGrid] = useState(Array(9).fill(null).map(() => Array(9).fill(0)))
  const [solution, setSolution] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [solved, setSolved] = useState(false)

  const handleCellChange = (row, col, value) => {
    if (solved) return

    const newGrid = grid.map(r => [...r])
    newGrid[row][col] = value
    setGrid(newGrid)
    setSolution(null)
    setError(null)
  }

  const handleImageUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setLoading(true)
    setError(null)
    setSolution(null)
    setSolved(false)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(`${API_BASE}/api/ocr/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setGrid(response.data.grid)
    } catch (err) {
      setError('Failed to process image. Please try again or use manual input.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const solvePuzzle = async () => {
    setLoading(true)
    setError(null)
    setSolution(null)
    setSolved(false)

    try {
      const response = await axios.post(`${API_BASE}/api/solve/`, {
        grid: grid
      })

      if (response.data.solved) {
        setSolution(response.data.solution)
        setSolved(true)
      } else {
        setError(response.data.error || 'Puzzle is unsolvable')
      }
    } catch (err) {
      setError('Failed to solve puzzle. Please check your input.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const clearGrid = () => {
    setGrid(Array(9).fill(null).map(() => Array(9).fill(0)))
    setSolution(null)
    setError(null)
    setSolved(false)
  }

  return (
    <div className="solve-sudoku">
      <div className="solve-container">
        <Link to="/" className="back-link">← Back to Home</Link>

        <h1>Solve Sudoku</h1>

        <div className="mode-selector">
          <button
            className={`mode-btn ${mode === 'manual' ? 'active' : ''}`}
            onClick={() => setMode('manual')}
          >
            Manual Input
          </button>
          <button
            className={`mode-btn ${mode === 'image' ? 'active' : ''}`}
            onClick={() => setMode('image')}
          >
            Upload Image
          </button>
        </div>

        {mode === 'image' && (
          <div className="image-upload">
            <label className="upload-label">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                disabled={loading}
                style={{ display: 'none' }}
              />
              <span className="upload-button">
                {loading ? 'Processing...' : 'Choose Image'}
              </span>
            </label>
            <p className="upload-hint">Upload a clear image of a Sudoku puzzle</p>
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        <div className="board-container">
          <SudokuBoard
            grid={solution || grid}
            puzzle={mode === 'manual' ? null : grid}
            onCellChange={handleCellChange}
            disabled={solved || mode === 'image'}
          />
        </div>

        <div className="solve-controls">
          <button
            onClick={solvePuzzle}
            disabled={loading}
            className="btn btn-primary"
          >
            {loading ? 'Solving...' : 'Solve Puzzle'}
          </button>
          <button
            onClick={clearGrid}
            className="btn btn-secondary"
          >
            Clear
          </button>
        </div>

        {solved && (
          <div className="solution-message">
            ✓ Puzzle solved successfully!
          </div>
        )}
      </div>
    </div>
  )
}

export default SolveSudoku
