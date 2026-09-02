import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { Home, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { clearToken } from '@/lib/auth'

const navLinkClass = ({ isActive }) =>
  `rounded-md px-3 py-2 text-sm font-medium transition-colors ${
    isActive ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted hover:text-foreground'
  }`

export default function AdminDashboard() {
  const navigate = useNavigate()

  function handleLogout() {
    clearToken()
    navigate('/admin/login', { replace: true })
  }

  return (
    <div className="min-h-dvh bg-background">
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-2 px-4 py-3 sm:px-6">
          <div className="flex flex-wrap items-center gap-1 sm:gap-4">
            <span className="px-2 text-base font-semibold text-foreground">enter</span>
            <nav className="flex items-center gap-1">
              <NavLink to="jobs" className={navLinkClass}>
                Jobs
              </NavLink>
              <NavLink to="candidates" className={navLinkClass}>
                Candidates
              </NavLink>
            </nav>
          </div>
          <div className="flex items-center gap-1">
            <Button type="button" variant="ghost" className="h-10 gap-1.5 px-3" asChild>
              <Link to="/">
                <Home className="h-4 w-4" />
                Home
              </Link>
            </Button>
            <Button type="button" variant="ghost" className="h-10 gap-1.5 px-3" onClick={handleLogout}>
              <LogOut className="h-4 w-4" />
              Log out
            </Button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
        <Outlet />
      </main>
    </div>
  )
}
