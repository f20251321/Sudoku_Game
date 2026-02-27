import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import LandingPage from './components/LandingPage'
import PlaySudoku from './components/PlaySudoku'
import SolveSudoku from './components/SolveSudoku'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/play" element={<PlaySudoku />} />
          <Route path="/solve" element={<SolveSudoku />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
