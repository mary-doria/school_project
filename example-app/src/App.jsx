import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Routes, Route, Link } from 'react-router-dom'
import School from './pages/School'
import Student from './pages/Student'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/" element={<School />} />
        <Route path="/student" element={<Student />} />
        <Route path="/student/:id" element={<Student />} />
        {/* catch-all for unmatched URLs */}
        <Route path="*" element={<School />} />
      </Routes>
    </>
  )
}

export default App
