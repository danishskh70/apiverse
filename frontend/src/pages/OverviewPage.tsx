import { Link } from 'react-router'
import {
  BookOpen,
  CloudSun,
  Compass,
  History,
  Laugh,
  Newspaper,
  Orbit,
  Quote,
} from 'lucide-react'

const modules = [
  {
    title: 'Weather',
    description: 'Explore current conditions and forecasts.',
    category: 'ENVIRONMENT',
    path: '/weather',
    icon: CloudSun,
  },
  {
    title: 'World Explorer',
    description: 'Discover countries, flags, and places.',
    category: 'OUR PLANET',
    path: '/world',
    icon: Compass,
  },
  {
    title: 'Newsroom',
    description: 'Catch up on the latest headlines.',
    category: 'CURRENT EVENTS',
    path: '/news',
    icon: Newspaper,
  },
  {
    title: 'Space',
    description: 'Explore astronomy and the universe.',
    category: 'BEYOND EARTH',
    path: '/space',
    icon: Orbit,
  },
  {
    title: 'JokeBox',
    description: 'Take a break with something funny.',
    category: 'A LITTLE FUN',
    path: '/jokes',
    icon: Laugh,
  },
  {
    title: 'Daily Inspiration',
    description: 'Find a thought worth carrying with you.',
    category: 'INSPIRATION',
    path: '/inspiration',
    icon: Quote,
  },
  {
    title: 'Word of the Day',
    description: 'Build your vocabulary one word at a time.',
    category: 'LEARNING',
    path: '/word',
    icon: BookOpen,
  },
  {
    title: 'This Day in History',
    description: 'Discover events that happened on this date.',
    category: 'HISTORY',
    path: '/history',
    icon: History,
  },
]

export default function OverviewPage() {
  return (
    <div className="overview-page">
      <section className="overview-hero">
        <p className="eyebrow">YOUR PERSONAL EXPLORATION SPACE</p>
        <h1>
          Explore more.
          <br />
          <span>Understand better.</span>
        </h1>
        <p className="overview-intro">
          A quieter place to discover the world, learn something new,
          and follow your curiosity.
        </p>
      </section>

      <section className="overview-section">
        <div className="overview-section-heading">
          <div>
            <p className="eyebrow">YOUR COLLECTION</p>
            <h2>Explore APIverse</h2>
          </div>
          <span className="module-count">08 MODULES</span>
        </div>

        <div className="overview-grid">
          {modules.map(({ title, description, category, path, icon: Icon }) => (
            <Link className="overview-card" to={path} key={path}>
              <div className="overview-card-top">
                <span className="overview-card-icon">
                  <Icon size={20} />
                </span>
                <span className="overview-card-arrow" aria-hidden="true">
                  ↗
                </span>
              </div>
              <p className="overview-card-category">{category}</p>
              <h3>{title}</h3>
              <p className="overview-card-description">{description}</p>
              <span className="overview-card-link">Open module</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
