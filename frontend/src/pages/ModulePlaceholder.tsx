import { Link, useLocation } from 'react-router'
import { ArrowLeft } from 'lucide-react'

const titles: Record<string, string> = {
  '/weather': 'Weather',
  '/world': 'World Explorer',
  '/news': 'Newsroom',
  '/space': 'Space',
  '/jokes': 'JokeBox',
  '/inspiration': 'Daily Inspiration',
  '/word': 'Word of the Day',
  '/history': 'This Day in History',
}

export default function ModulePlaceholder() {
  const location = useLocation()
  const title = titles[location.pathname] ?? 'APIverse'

  return (
    <section className="placeholder-page">
      <p className="module-eyebrow">APIverse MODULE</p>
      <h1>{title}</h1>
      <p>This page is not connected yet.</p>
      <Link className="action-button" to="/">
        <ArrowLeft size={16} /> Back to Overview
      </Link>
    </section>
  )
}
