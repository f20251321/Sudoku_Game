import React, { useState, useEffect } from 'react'
import './Timer.css'

function Timer({ started, completed }) {
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    if (!started || completed) return

    const interval = setInterval(() => {
      setSeconds(prev => prev + 1)
    }, 1000)

    return () => clearInterval(interval)
  }, [started, completed])

  useEffect(() => {
    if (started && !completed) {
      setSeconds(0)
    }
  }, [started])

  const formatTime = (totalSeconds) => {
    const hours = Math.floor(totalSeconds / 3600)
    const minutes = Math.floor((totalSeconds % 3600) / 60)
    const secs = totalSeconds % 60

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="timer">
      <div className="timer-label">Time:</div>
      <div className="timer-value">{formatTime(seconds)}</div>
    </div>
  )
}

export default Timer
