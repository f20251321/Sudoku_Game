import React from 'react'
import { Link } from 'react-router-dom'
import './LandingPage.css'

function LandingPage() {
  return (
    <div className="landing-page">
      <div className="landing-container">
        <h1 className="title">Sudoku Arena</h1>
        <p className="subtitle">Challenge yourself with Sudoku puzzles</p>
        
        <div className="options">
          <Link to="/play" className="option-card">
            <h2>Play Sudoku</h2>
            <p>Generate and solve puzzles with different difficulty levels</p>
          </Link>
          
          <Link to="/solve" className="option-card">
            <h2>Solve Sudoku</h2>
            <p>Upload an image or enter a puzzle manually to get the solution</p>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
