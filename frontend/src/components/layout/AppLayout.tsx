import { Bell, Search } from 'lucide-react'
import { Link, useLocation, Outlet } from 'react-router'
import Sidebar from './Sidebar'

const pageTitles: Record<string, string> = {
  '/': 'Overview',
  '/weather': 'Weather',
  '/world': 'World Explorer',
  '/news': 'Newsroom',
  '/space': 'Space',
  '/jokes': 'JokeBox',
  '/inspiration': 'Daily Inspiration',
  '/word': 'Word of the Day',
  '/history': 'This Day in History',
}

export default function AppLayout() {
  const location = useLocation()
  const pageTitle = pageTitles[location.pathname] ?? 'APIverse'

  return (
    <div className="app-shell">
      <Sidebar />

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            <Link to="/">APIverse</Link>
            <span>/</span>
            {pageTitle}
          </div>

          <div className="topbar-actions">
            <span className="workspace-label">PERSONAL WORKSPACE</span>
            <button
              className="icon-button"
              type="button"
              aria-label="Search (coming soon)"
              title="Search coming soon"
            >
              <Search size={18} />
            </button>
            <button
              className="icon-button"
              type="button"
              aria-label="Notifications (coming soon)"
              title="Notifications coming soon"
            >
              <Bell size={18} />
            </button>
          </div>
        </header>

        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
