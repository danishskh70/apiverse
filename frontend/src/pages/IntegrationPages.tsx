import { useEffect, useState } from 'react'
import {
  CalendarDays,
  ExternalLink,
  LoaderCircle,
  MapPin,
  RefreshCw,
  Search,
  Sparkles,
  Wind,
  Droplets,
  Thermometer,
} from 'lucide-react'
import {
  getCurrentWeather,
  type WeatherData,
} from '../services/weather'
import {
  getCountries,
  type Country,
} from '../services/countries'
import {
  getTopHeadlines,
  type NewsArticle,
  type NewsCategory,
} from '../services/news'
import {
  getApod,
  type ApodResponse,
} from '../services/space'
import {
  getRandomJoke,
  type JokeResponse,
} from '../services/jokes'
import {
  getDailyQuote,
  type DailyQuote,
} from '../services/quotes'
import {
  getWordDefinition,
  type WordDefinition,
} from '../services/word'
import {
  getHistoricalEvents,
  type HistoryResponse,
} from '../services/history'
import DOMPurify from 'dompurify'

function PageHeading({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string
  title: string
  description: string
}) {
  return (
    <div className="module-heading">
      <p className="module-eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p>{description}</p>
    </div>
  )
}

function LoadingState({ label = 'Loading data…' }: { label?: string }) {
  return (
    <div className="module-state" role="status">
      <LoaderCircle className="spin" size={22} />
      <span>{label}</span>
    </div>
  )
}

function ErrorState({
  message,
  onRetry,
}: {
  message: string
  onRetry: () => void
}) {
  return (
    <div className="module-error" role="alert">
      <p>{message}</p>
      <button className="action-button" type="button" onClick={onRetry}>
        <RefreshCw size={15} />
        Try again
      </button>
    </div>
  )
}

function EmptyState({ message }: { message: string }) {
  return <div className="module-empty">{message}</div>
}

function formatNumber(value: number) {
  return new Intl.NumberFormat('en-IN').format(value)
}

function formatDate(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString(undefined, {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

function formatTime(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function WeatherPage() {
  const [data, setData] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadWeather() {
    setLoading(true)
    setError('')
    try {
      setData(await getCurrentWeather())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load weather.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchWeather() {
    try {
      const result = await getCurrentWeather()
      if (!cancelled) setData(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error ? err.message : 'Could not load weather.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchWeather()

  return () => {
    cancelled = true
  }
}, [])

  return (
    <section className="module-page">
      <PageHeading
        eyebrow="DISCOVER / WEATHER"
        title="Weather"
        description="Current conditions for Pune, Maharashtra."
      />
      {loading ? <LoadingState label="Fetching current conditions…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadWeather()} /> : null}
      {!loading && !error && data ? (
        <div className="weather-layout">
          <article className="module-card weather-main-card">
            <div className="weather-location">
              <MapPin size={16} />
              <span>Pune, India</span>
            </div>
            <p className="weather-condition">{data.condition}</p>
            <div className="weather-temperature">
              {Math.round(data.current.temperature_2m)}°
              <span>C</span>
            </div>
            <p className="weather-feels">
              Feels like {Math.round(data.current.apparent_temperature)}°C
            </p>
            <div className="weather-meta">
              <span>{data.current.is_day ? 'Daytime' : 'Nighttime'}</span>
              <span>Updated {formatTime(data.current.time)}</span>
            </div>
          </article>
          <div className="weather-metrics">
            <article className="module-card metric-card">
              <Thermometer size={19} />
              <span>Temperature</span>
              <strong>{data.current.temperature_2m}°C</strong>
              <small>Current air temperature</small>
            </article>
            <article className="module-card metric-card">
              <Droplets size={19} />
              <span>Humidity</span>
              <strong>{data.current.relative_humidity_2m}%</strong>
              <small>Relative humidity</small>
            </article>
            <article className="module-card metric-card">
              <Wind size={19} />
              <span>Wind speed</span>
              <strong>{data.current.wind_speed_10m} km/h</strong>
              <small>At the measurement point</small>
            </article>
            <article className="module-card metric-card">
              <Droplets size={19} />
              <span>Precipitation</span>
              <strong>{data.current.precipitation} mm</strong>
              <small>Current precipitation</small>
            </article>
          </div>
          <p className="module-footnote">Timezone: {data.timezone}</p>
        </div>
      ) : null}
    </section>
  )
}

export function WorldPage() {
  const [countries, setCountries] = useState<Country[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  async function loadCountries() {
    setLoading(true)
    setError('')
    try {
      setCountries(await getCountries())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load countries.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchCountries() {
    try {
      const result = await getCountries()
      if (!cancelled) setCountries(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error ? err.message : 'Could not load countries.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchCountries()

  return () => {
    cancelled = true
  }
}, [])

  const query = search.trim().toLowerCase()
  const filtered = countries.filter((country) => {
    const text = [
      country.name.common,
      country.name.official,
      country.capital?.join(' '),
      country.region,
      country.cca3,
    ].join(' ').toLowerCase()
    return text.includes(query)
  })

  return (
    <section className="module-page">
      <PageHeading
        eyebrow="DISCOVER / WORLD"
        title="World Explorer"
        description="Explore countries, capitals, regions and population."
      />
      <div className="module-toolbar">
        <label className="search-field">
          <Search size={17} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search countries or capitals…"
            aria-label="Search countries"
          />
        </label>
        {!loading && !error ? (
          <span className="result-count">{filtered.length} countries</span>
        ) : null}
      </div>
      {loading ? <LoadingState label="Loading country data…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadCountries()} /> : null}
      {!loading && !error && filtered.length === 0 ? (
        <EmptyState message="No countries match your search." />
      ) : null}
      {!loading && !error && filtered.length > 0 ? (
        <div className="country-grid">
          {filtered.map((country) => (
            <article className="module-card country-card" key={country.cca3}>
              <div className="country-card-top">
                {country.flags?.png ? (
                  <img
                    src={country.flags.png}
                    alt=""
                    loading="lazy"
                  />
                ) : null}
                <span className="country-code">{country.cca3}</span>
              </div>
              <h2>{country.name.common}</h2>
              <p className="country-official">{country.name.official}</p>
              <dl className="country-details">
                <div>
                  <dt>Capital</dt>
                  <dd>{country.capital?.join(', ') || 'Not listed'}</dd>
                </div>
                <div>
                  <dt>Region</dt>
                  <dd>{country.region || 'Not listed'}</dd>
                </div>
                <div>
                  <dt>Population</dt>
                  <dd>{formatNumber(country.population)}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  )
}

const newsCategories: { label: string; value: NewsCategory }[] = [
  { label: 'General', value: 'general' },
  { label: 'Business', value: 'business' },
  { label: 'Technology', value: 'technology' },
  { label: 'Science', value: 'science' },
  { label: 'Health', value: 'health' },
  { label: 'Sports', value: 'sports' },
  { label: 'Entertainment', value: 'entertainment' },
]

export function NewsPage() {
  const [articles, setArticles] = useState<NewsArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [category, setCategory] = useState<NewsCategory>('general')
  const [search, setSearch] = useState('')
  const [submittedSearch, setSubmittedSearch] = useState('')

  async function loadNews(nextCategory = category, query = submittedSearch) {
    setLoading(true)
    setError('')
    try {
      const result = await getTopHeadlines(nextCategory, query || undefined)
      setArticles(result.articles)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load news.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchNews() {
    try {
      const result = await getTopHeadlines('general')
      if (!cancelled) setArticles(result.articles)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error ? err.message : 'Could not load news.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchNews()

  return () => {
    cancelled = true
  }
}, [])

  function chooseCategory(nextCategory: NewsCategory) {
    setCategory(nextCategory)
    void loadNews(nextCategory, submittedSearch)
  }

  function submitSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmittedSearch(search.trim())
    void loadNews(category, search.trim())
  }

  return (
    <section className="module-page">
      <PageHeading
        eyebrow="DISCOVER / NEWS"
        title="Newsroom"
        description="Headlines from India, with categories and search."
      />
      <form className="module-toolbar news-search-form" onSubmit={submitSearch}>
        <label className="search-field">
          <Search size={17} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search news…"
            aria-label="Search news"
          />
        </label>
        <button className="action-button" type="submit">Search</button>
        <button
          className="icon-button"
          type="button"
          aria-label="Refresh news"
          onClick={() => void loadNews()}
          title="Refresh news"
        >
          <RefreshCw size={17} />
        </button>
      </form>
      <div className="category-tabs" aria-label="News categories">
        {newsCategories.map((item) => (
          <button
            type="button"
            key={item.value}
            className={`category-tab${category === item.value ? ' selected' : ''}`}
            onClick={() => chooseCategory(item.value)}
            aria-pressed={category === item.value}
          >
            {item.label}
          </button>
        ))}
      </div>
      {loading ? <LoadingState label="Loading headlines…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadNews()} /> : null}
      {!loading && !error && articles.length === 0 ? (
        <EmptyState message="No articles were returned. Try another category or search." />
      ) : null}
      {!loading && !error && articles.length > 0 ? (
        <div className="news-grid">
          {articles.map((article, index) => (
            <article className="module-card news-card" key={`${article.url}-${index}`}>
              {article.urlToImage ? (
                <img
                  className="news-image"
                  src={article.urlToImage}
                  alt=""
                  loading="lazy"
                  onError={(event) => {
                    event.currentTarget.style.display = 'none'
                  }}
                />
              ) : null}
              <div className="news-card-content">
                <p className="news-source">{article.source.name || 'News source'}</p>
                <h2>{article.title}</h2>
                {article.description ? <p className="news-description">{article.description}</p> : null}
                <div className="news-card-footer">
                  <span>{article.publishedAt ? formatDate(article.publishedAt) : 'Date unavailable'}</span>
                  {article.url ? (
                    <a href={article.url} target="_blank" rel="noreferrer">
                      Read article <ExternalLink size={14} />
                    </a>
                  ) : null}
                </div>
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  )
}

export function SpacePage() {
  const [data, setData] = useState<ApodResponse | null>(null)
  const [date, setDate] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadApod(nextDate = date) {
    setLoading(true)
    setError('')
    try {
      setData(await getApod(nextDate || undefined))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load astronomy data.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchApod() {
    try {
      const result = await getApod()
      if (!cancelled) setData(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error
            ? err.message
            : 'Could not load astronomy data.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchApod()

  return () => {
    cancelled = true
  }
}, [])

  return (
    <section className="module-page">
      <PageHeading
        eyebrow="DISCOVER / SPACE"
        title="Space"
        description="A daily view of the universe, powered by NASA's Astronomy Picture of the Day."
      />
      <form
        className="module-toolbar date-toolbar"
        onSubmit={(event) => {
          event.preventDefault()
          void loadApod()
        }}
      >
        <label className="date-field">
          <CalendarDays size={17} />
          <span>Choose a date</span>
          <input
            type="date"
            value={date}
            max={new Date().toISOString().slice(0, 10)}
            onChange={(event) => setDate(event.target.value)}
            aria-label="Astronomy picture date"
          />
        </label>
        <button className="action-button" type="submit">View date</button>
        <button
          className="icon-button"
          type="button"
          onClick={() => {
            setDate('')
            void loadApod('')
          }}
          aria-label="Load today's picture"
          title="Load today's picture"
        >
          <RefreshCw size={17} />
        </button>
      </form>
      {loading ? <LoadingState label="Exploring today's universe…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadApod()} /> : null}
      {!loading && !error && data ? (
        <article className="module-card apod-card">
          <div className="apod-copy">
            <p className="module-eyebrow">{formatDate(data.date)}</p>
            <h2>{data.title}</h2>
            {data.copyright ? (
              <p className="apod-copyright">
                Image credit:{' '}
                <span
                  dangerouslySetInnerHTML={{
                    __html: DOMPurify.sanitize(data.copyright),
                  }}
                />
              </p>
            ) : null}

            <div
              className="apod-explanation"
              dangerouslySetInnerHTML={{
                __html: DOMPurify.sanitize(data.explanation),
              }}
            />
            {data.url ? (
              <a className="text-link" href={data.hdurl || data.url} target="_blank" rel="noreferrer">
                Open full resolution <ExternalLink size={15} />
              </a>
            ) : null}
          </div>
          <div className="apod-media">
            {data.media_type === 'video' ? (
              <iframe
                src={data.url}
                title={data.title}
                loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            ) : (
              <a
                href={data.hdurl || data.url}
                target="_blank"
                rel="noreferrer"
              >
                <img
                  src={data.hdurl || data.url}
                  alt={data.title}
                  loading="lazy"
                  onError={(event) => {
                    event.currentTarget.style.display = 'none'
                  }}
                />
              </a>
            )}
          </div>
        </article>
      ) : null}
    </section>
  )
}

export function JokesPage() {
  const [joke, setJoke] = useState<JokeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadJoke() {
    setLoading(true)
    setError('')
    try {
      setJoke(await getRandomJoke())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load a joke.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchJoke() {
    try {
      const result = await getRandomJoke()
      if (!cancelled) setJoke(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error ? err.message : 'Could not load a joke.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchJoke()

  return () => {
    cancelled = true
  }
}, [])
  return (
    <section className="module-page">
      <PageHeading
        eyebrow="DISCOVER / ENTERTAINMENT"
        title="JokeBox"
        description="Take a quick break with a random joke."
      />
      {loading ? <LoadingState label="Finding a joke…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadJoke()} /> : null}
      {!loading && !error && joke ? (
        <article className="module-card joke-card">
          <div className="joke-symbol"><Sparkles size={24} /></div>
          <p className="module-eyebrow">{joke.category || 'RANDOM JOKE'}</p>
          {joke.type === 'twopart' ? (
            <>
              <h2 className="joke-setup">{joke.setup}</h2>
              <p className="joke-delivery">{joke.delivery}</p>
            </>
          ) : (
            <h2 className="joke-setup">{joke.joke}</h2>
          )}
          <button className="action-button" type="button" onClick={() => void loadJoke()}>
            <RefreshCw size={16} />
            Another joke
          </button>
        </article>
      ) : null}
      {!loading && !error && !joke ? (
        <EmptyState message="No joke loaded yet." />
      ) : null}
    </section>
  )
}

export function InspirationPage() {
  const [quote, setQuote] = useState<DailyQuote | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadQuote() {
    setLoading(true)
    setError('')
    try {
      setQuote(await getDailyQuote())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load the quote.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchQuote() {
    try {
      const result = await getDailyQuote()
      if (!cancelled) setQuote(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error ? err.message : 'Could not load the quote.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchQuote()

  return () => {
    cancelled = true
  }
}, [])
  return (
    <section className="module-page">
      <PageHeading
        eyebrow="KNOWLEDGE / INSPIRATION"
        title="Daily Inspiration"
        description="A thoughtful quote to carry into your day."
      />
      {loading ? <LoadingState label="Finding today's quote…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadQuote()} /> : null}
      {!loading && !error && quote ? (
        <article className="module-card quote-card">
          <span className="quote-mark" aria-hidden="true">“</span>
          <blockquote>{quote.quote}</blockquote>
          <p className="quote-author">{quote.author}</p>
          {quote.source ? <p className="quote-source">{quote.source}</p> : null}
          <button className="action-button" type="button" onClick={() => void loadQuote()}>
            <RefreshCw size={15} />
            Refresh quote
          </button>
        </article>
      ) : null}
    </section>
  )
}

export function WordPage() {
  const [wordInput, setWordInput] = useState('serendipity')
  const [word, setWord] = useState<WordDefinition | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadWord(value = wordInput) {
    const cleaned = value.trim()
    if (!cleaned) {
      setError('Enter a word to look up.')
      return
    }

    setLoading(true)
    setError('')
    try {
      setWord(await getWordDefinition(cleaned))
    } catch (err) {
      setWord(null)
      setError(err instanceof Error ? err.message : 'Could not load the definition.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchWord() {
    try {
      const result = await getWordDefinition('serendipity')
      if (!cancelled) setWord(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error
            ? err.message
            : 'Could not load the definition.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchWord()

  return () => {
    cancelled = true
  }
}, [])
  return (
    <section className="module-page">
      <PageHeading
        eyebrow="KNOWLEDGE / VOCABULARY"
        title="Word of the Day"
        description="Look up a word, learn its meaning and discover how it is used."
      />
      <form
        className="module-toolbar word-search-form"
        onSubmit={(event) => {
          event.preventDefault()
          void loadWord()
        }}
      >
        <label className="search-field">
          <Search size={17} />
          <input
            value={wordInput}
            onChange={(event) => setWordInput(event.target.value)}
            placeholder="Enter a word…"
            aria-label="Word to define"
          />
        </label>
        <button className="action-button" type="submit" disabled={loading}>
          Look up
        </button>
      </form>
      {loading ? <LoadingState label="Looking up the word…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadWord()} /> : null}
      {!loading && !error && word ? (
        <article className="module-card word-card">
          <p className="module-eyebrow">WORD DEFINITION</p>
          <h2>{word.word}</h2>
          {word.phonetic ? <p className="word-phonetic">{word.phonetic}</p> : null}
          {word.meanings.map((meaning, index) => (
            <section className="word-meaning" key={`${meaning.partOfSpeech}-${index}`}>
              <span className="part-of-speech">{meaning.partOfSpeech}</span>
              <ol>
                {meaning.definitions.map((definition, definitionIndex) => (
                  <li key={`${definition.definition}-${definitionIndex}`}>
                    <p>{definition.definition}</p>
                    {definition.example ? (
                      <p className="word-example">“{definition.example}”</p>
                    ) : null}
                  </li>
                ))}
              </ol>
            </section>
          ))}
          {word.source ? (
            <p className="module-footnote">
              Source: <a href={word.source} target="_blank" rel="noreferrer">{word.source}</a>
            </p>
          ) : null}
        </article>
      ) : null}
    </section>
  )
}

export function HistoryPage() {
  const [data, setData] = useState<HistoryResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadHistory() {
    setLoading(true)
    setError('')
    try {
      setData(await getHistoricalEvents())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load historical events.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
  let cancelled = false

  async function fetchHistory() {
    try {
      const result = await getHistoricalEvents()
      if (!cancelled) setData(result)
    } catch (err) {
      if (!cancelled) {
        setError(
          err instanceof Error
            ? err.message
            : 'Could not load historical events.',
        )
      }
    } finally {
      if (!cancelled) setLoading(false)
    }
  }

  void fetchHistory()

  return () => {
    cancelled = true
  }
}, [])

  return (
    <section className="module-page">
      <PageHeading
        eyebrow="KNOWLEDGE / HISTORY"
        title="This Day in History"
        description="Explore notable events that happened on this date."
      />
      {loading ? <LoadingState label="Looking through history…" /> : null}
      {!loading && error ? <ErrorState message={error} onRetry={() => void loadHistory()} /> : null}
      {!loading && !error && data ? (
        <>
          <div className="history-date-card module-card">
            <CalendarDays size={19} />
            <div>
              <strong>{data.date ? formatDate(data.date) : 'Today in history'}</strong>
              <p>{data.events.length} events found</p>
            </div>
          </div>
          {data.events.length === 0 ? (
            <EmptyState message="No historical events were returned for this date." />
          ) : (
            <div className="history-timeline">
              {data.events.map((event, index) => (
                <article className="module-card history-event" key={`${event.year}-${event.title}-${index}`}>
                  <div className="history-year">{event.year}</div>
                  <div className="history-event-content">
                    <h2>{event.title}</h2>
                    {event.pages.length > 0 ? (
                      <div className="history-links">
                        {event.pages.slice(0, 3).map((page, pageIndex) => (
                          page.url ? (
                            <a href={page.url} key={`${page.url}-${pageIndex}`} target="_blank" rel="noreferrer">
                              {page.title || 'Read more'} <ExternalLink size={13} />
                            </a>
                          ) : (
                            <span key={`${page.title}-${pageIndex}`}>{page.title}</span>
                          )
                        ))}
                      </div>
                    ) : null}
                  </div>
                </article>
              ))}
            </div>
          )}
          {data.source ? <p className="module-footnote">Source: {data.source}</p> : null}
        </>
      ) : null}
    </section>
  )
}
