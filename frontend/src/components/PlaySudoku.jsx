import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { API_BASE } from '../config'
import SudokuBoard from './SudokuBoard'
import Timer from './Timer'
import './PlaySudoku.css'

function PlaySudoku() {
  const [difficulty, setDifficulty] = useState('medium')
  const [puzzle, setPuzzle] = useState(null)
  const [solution, setSolution] = useState(null)
  const [grid, setGrid] = useState(null)
  const [loading, setLoading] = useState(false)
  const [timerStarted, setTimerStarted] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [error, setError] = useState(null)
  const [gameStarted, setGameStarted] = useState(false)

  const generatePuzzle = async () => {
    setLoading(true)
    setError(null)
    setCompleted(false)
    setTimerStarted(false)
    setGameStarted(false)

    try {
      const response = await axios.post(`${API_BASE} /api/generate / `, {
        difficulty: difficulty
      })
      setPuzzle(response.data.puzzle)
      setSolution(response.data.solution)
      setGrid(response.data.puzzle.map(row => [...row]))
    } catch (err) {
      setError('Failed to generate puzzle. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const startGame = () => {
    if (grid) {
      setGameStarted(true)
      setTimerStarted(true)
    }
  }

  const handleCellChange = (row, col, value) => {
    if (completed || !grid) return

    const newGrid = grid.map(r => [...r])
    newGrid[row][col] = value
    setGrid(newGrid)

    if (JSON.stringify(newGrid) === JSON.stringify(solution)) {
      setCompleted(true)
      setTimerStarted(false)
    }
  }

  const resetPuzzle = () => {
    if (puzzle) {
      setGrid(puzzle.map(row => [...row]))
      setCompleted(false)
      setTimerStarted(true)
      setGameStarted(true)
    }
  }

  const handleNewPuzzle = () => {
    setGameStarted(false)
    setTimerStarted(false)
    setGrid(null)
    setPuzzle(null)
    setSolution(null)
    generatePuzzle()
  }

  return (
    <div className="play-sudoku">
      <div className="play-container">
        <Link to="/" className="back-link">← Back to Home</Link>

        <h1>Play Sudoku</h1>

        {!gameStarted ? (
          <div className="start-screen">
            <div className="difficulty-selector-large">
              <label>Choose Difficulty:</label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                disabled={loading}
                className="difficulty-select"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
                <option value="expert">Expert</option>
              </select>
            </div>

            <button
              onClick={handleNewPuzzle}
              disabled={loading}
              className="btn btn-primary btn-large"
            >
              {loading ? 'Generating Puzzle...' : 'Generate Puzzle'}
            </button>

            {error && <div className="error-message">{error}</div>}

            {grid && !gameStarted && (
              <div className="ready-to-play">
                <p>Puzzle ready! Click Play to start the timer.</p>
                <button
                  onClick={startGame}
                  className="btn btn-primary btn-large"
                >
                  Play
                </button>
              </div>
            )}
          </div>
        ) : (
          <>
            <div className="controls">
              <div className="difficulty-selector">
                <label>Difficulty:</label>
                <span className="difficulty-badge">{difficulty}</span>
              </div>

              <button
                onClick={handleNewPuzzle}
                disabled={loading}
                className="btn btn-secondary"
              >
                New Puzzle
              </button>

              <button
                onClick={resetPuzzle}
                className="btn btn-secondary"
              >
                Reset
              </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <Timer
              started={timerStarted}
              completed={completed}
            />

            {completed && (
              <div className="completion-message">
                🎉 Congratulations! Puzzle solved!
              </div>
            )}

            <SudokuBoard
              grid={grid}
              puzzle={puzzle}
              solution={solution}
              onCellChange={handleCellChange}
              disabled={completed}
            />
          </>
        )}
      </div>
    </div>
  )
}

export default PlaySudoku
