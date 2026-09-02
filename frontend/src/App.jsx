import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ApplyPage from './pages/ApplyPage'
import AdminLogin from './pages/AdminLogin'
import AdminDashboard from './pages/AdminDashboard'
import JobsPage from './pages/admin/JobsPage'
import CandidatesPage from './pages/admin/CandidatesPage'
import { RequireAuth } from './components/RequireAuth'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ApplyPage />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route element={<RequireAuth />}>
          <Route path="/admin" element={<AdminDashboard />}>
            <Route index element={<Navigate to="jobs" replace />} />
            <Route path="jobs" element={<JobsPage />} />
            <Route path="candidates" element={<CandidatesPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
