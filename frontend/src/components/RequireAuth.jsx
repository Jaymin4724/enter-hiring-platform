import { Navigate, Outlet } from 'react-router-dom'
import { isAuthenticated } from '@/lib/auth'

export function RequireAuth() {
  if (!isAuthenticated()) {
    return <Navigate to="/admin/login" replace />
  }
  return <Outlet />
}
