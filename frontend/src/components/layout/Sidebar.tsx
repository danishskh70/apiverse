import { NavLink } from 'react-router'
import {
  BookOpen,
  CloudSun,
  Compass,
  LayoutDashboard,
  Laugh,
  Newspaper,
  Orbit,
  Quote,
  Sparkles,
  History,
} from 'lucide-react'

const groups = [
  {
    title: 'WORKSPACE',
    items: [
      { label: 'Overview', path: '/', icon: LayoutDashboard },
    ],
  },
  {
    title: 'DISCOVER',
    items: [
      { label: 'Weather', path: '/weather', icon: CloudSun },
      { label: 'World Explorer', path: '/world', icon: Compass },
      { label: 'Newsroom', path: '/news', icon: Newspaper },
      { label: 'Space', path: '/space', icon: Orbit },
      { label: 'JokeBox', path: '/jokes', icon: Laugh },
    ],
  },
  {
    title: 'KNOWLEDGE',
    items: [
      { label: 'Daily Inspiration', path: '/inspiration', icon: Quote },
      { label: 'Word of the Day', path: '/word', icon: BookOpen },
      { label: 'This Day in History', path: '/history', icon: History },
    ],
  },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <NavLink className="brand" to="/" end>
        <span className="brand-mark">
          <Sparkles size={21} />
        </span>
        <span>
          APIverse
          <small>EXPLORE MORE</small>
        </span>
      </NavLink>

      {groups.map((group) => (
        <div className="nav-group" key={group.title}>
          <p className="nav-heading">{group.title}</p>
          <nav className="navigation" aria-label={group.title}>
            {group.items.map(({ label, path, icon: Icon }) => (
              <NavLink
                className={({ isActive }) =>
                  `nav-item${isActive ? ' active' : ''}`
                }
                key={path}
                to={path}
                end={path === '/'}
              >
                <Icon size={18} />
                <span>{label}</span>
                <span className="active-dot" aria-hidden="true" />
              </NavLink>
            ))}
          </nav>
        </div>
      ))}

      <div className="sidebar-bottom">
        <div className="status-dot" />
        <span>APIverse workspace</span>
        <small>v1.0</small>
      </div>
    </aside>
  )
}
