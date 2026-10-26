import { useEffect, useState } from 'react'
import { getCurrentWeather, type WeatherData } from './services/weather'
import { getCountries, type Country } from './services/countries'
import {
  getTopHeadlines,
  type NewsArticle,
  type NewsCategory,
} from './services/news'
import { getApod, type ApodResponse } from './services/space'
import { getRandomJoke, type JokeResponse } from './services/jokes'
import { getDailyQuote, type DailyQuote } from './services/quotes'
import { getWordDefinition, type WordDefinition } from './services/word'
import {
  getHistoricalEvents,
  type HistoryResponse,
} from './services/history'
import {
  CloudSun,
  Compass,
  Newspaper,
  Orbit,
  Globe,
  BookOpen,
  Laugh,
  Code2,
  History,
  LayoutDashboard,
  Search,
  Bell,
  ArrowUpRight,
  Sparkles,
} from 'lucide-react'
import './App.css'

const navigation = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'Weather', icon: CloudSun },
  { label: 'World Explorer', icon: Compass },
  { label: 'Newsroom', icon: Newspaper },
  { label: 'Space', icon: Orbit },
  { label: 'JokeBox', icon: Laugh },
  { label: 'GitHub', icon: Code2 },
]

function App() {
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [weatherError, setWeatherError] = useState('')
  const [weatherLoading, setWeatherLoading] = useState(true)
  const [countries, setCountries] = useState<Country[]>([])
  const [countriesLoading, setCountriesLoading] = useState(true)
  const [countriesError, setCountriesError] = useState('')
  const [countrySearch, setCountrySearch] = useState('')
  const [news, setNews] = useState<NewsArticle[]>([])
  const [newsLoading, setNewsLoading] = useState(true)
  const [newsError, setNewsError] = useState('')
  const [newsCategory, setNewsCategory] = useState<NewsCategory>('general')
  const [apod, setApod] = useState<ApodResponse | null>(null)
  const [apodLoading, setApodLoading] = useState(true)
  const [apodError, setApodError] = useState('')
  const [apodDate, setApodDate] = useState('')
  const [joke, setJoke] = useState<JokeResponse | null>(null)
  const [jokeLoading, setJokeLoading] = useState(false)
  const [jokeError, setJokeError] = useState('')
  const [jokeRequest, setJokeRequest] = useState(0)
  const [dailyQuote, setDailyQuote] = useState<DailyQuote | null>(null)
  const [quoteLoading, setQuoteLoading] = useState(true)
  const [quoteError, setQuoteError] = useState('')
  const [wordData, setWordData] = useState<WordDefinition | null>(null)
  const [wordLoading, setWordLoading] = useState(true)
  const [wordError, setWordError] = useState('')
  const [historyData, setHistoryData] = useState<HistoryResponse | null>(null)
  const [historyLoading, setHistoryLoading] = useState(true)
  const [historyError, setHistoryError] = useState('')


  useEffect(() => {
    getCurrentWeather()
      .then(setWeather)
      .catch(() => setWeatherError('Weather data is temporarily unavailable.'))
      .finally(() => setWeatherLoading(false))
  }, [])

  useEffect(() => {
    let cancelled = false

    getCountries()
      .then((data) => {
        if (!cancelled) {
          setCountries(data)
          setCountriesError('')
        }
      })
      .catch(() => {
        if (!cancelled) {
          setCountriesError('Unable to load countries right now.')
        }
      })
      .finally(() => {
        if (!cancelled) {
          setCountriesLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    let cancelled = false

    setNewsLoading(true)
    setNewsError('')

    getTopHeadlines(newsCategory)
      .then((data) => {
        if (!cancelled) {
          setNews(data.articles)
        }
      })
      .catch(() => {
        if (!cancelled) {
          setNewsError('Unable to load news right now.')
        }
      })
      .finally(() => {
        if (!cancelled) {
          setNewsLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [newsCategory])
  useEffect(() => {
    let cancelled = false

    setApodLoading(true)
    setApodError('')

    getApod(apodDate || undefined)
      .then((data) => {
        if (!cancelled) {
          setApod(data)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setApodError(
            error instanceof Error
              ? error.message
              : 'Unable to load NASA astronomy data right now.',
          )
        }
      })
      .finally(() => {
        if (!cancelled) {
          setApodLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [apodDate])
  useEffect(() => {
    let cancelled = false

    setJokeLoading(true)
    setJokeError('')

    getRandomJoke()
      .then((data) => {
        if (!cancelled) {
          setJoke(data)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setJokeError(
            error instanceof Error
              ? error.message
              : 'Unable to load a joke right now.',
          )
        }
      })
      .finally(() => {
        if (!cancelled) {
          setJokeLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [jokeRequest])

  useEffect(() => {
    let cancelled = false

    setQuoteLoading(true)
    setQuoteError('')

    getDailyQuote()
      .then((data) => {
        if (!cancelled) {
          setDailyQuote(data)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setQuoteError(
            error instanceof Error
              ? error.message
              : "Unable to load today's quote.",
          )
        }
      })
      .finally(() => {
        if (!cancelled) {
          setQuoteLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    let cancelled = false

    getWordDefinition('serendipity')
      .then((data) => {
        if (!cancelled) {
          setWordData(data)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setWordError(
            error instanceof Error
              ? error.message
              : 'Unable to load the word of the day.',
          )
        }
      })
      .finally(() => {
        if (!cancelled) {
          setWordLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [])
  useEffect(() => {
    let cancelled = false

    getHistoricalEvents()
      .then((data) => {
        if (!cancelled) {
          setHistoryData(data)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setHistoryError(
            error instanceof Error
              ? error.message
              : 'Unable to load historical events.',
          )
        }
      })
      .finally(() => {
        if (!cancelled) {
          setHistoryLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#">
          <span className="brand-mark"><Sparkles size={21} /></span>
          <span>APIverse<small>EXPLORE MORE</small></span>
        </a>

        <p className="nav-heading">WORKSPACE</p>

        <nav className="navigation">
          {navigation.map(({ label, icon: Icon }, index) => (
            <button
              className={`nav-item ${index === 0 ? 'active' : ''}`}
              key={label}
            >
              <Icon size={18} />
              <span>{label}</span>
              {index === 0 && <span className="active-dot" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot" />
          <span>All systems operational</span>
          <small>v1.0</small>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">APIverse <span>/</span> Overview</div>
          <div className="topbar-actions">
            <span className="workspace-label">PERSONAL WORKSPACE</span>
            <button className="icon-button" aria-label="Search"><Search size={18} /></button>
            <button className="icon-button" aria-label="Notifications"><Bell size={18} /></button>
            <div className="avatar">A</div>
          </div>
        </header>


        <section className="welcome-section">
          <div className="eyebrow"><span /> YOUR PERSONAL COMMAND CENTER</div>
          <h1>Explore more.<br /><span>Understand better.</span></h1>
          <p>
            Six windows into a bigger world. Discover live weather, explore
            our planet, catch up on news, and look beyond the stars.
          </p>
          <div className="welcome-meta">
            <span><Sparkles size={15} /> Stay curious.</span>
            <span>APIverse workspace</span>
            <span className="version-pill">v1.0</span>
          </div>
        </section>
        <section className="inspiration-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">A THOUGHT FOR TODAY</p>
              <h2>
                <Sparkles size={21} /> Daily Inspiration
              </h2>
            </div>
          </div>

          {quoteLoading ? (
            <p className="countries-message">Finding today's inspiration...</p>
          ) : quoteError ? (
            <p className="countries-message">{quoteError}</p>
          ) : dailyQuote ? (
            <article className="inspiration-card">
              <span className="inspiration-mark">“</span>
              <blockquote>{dailyQuote.quote}</blockquote>
              <p className="inspiration-author">— {dailyQuote.author}</p>
              <div className="card-footer">
                <span>A little inspiration for your day.</span>
                <span>
                  Quotes by{' '}
                  <a
                    href="https://zenquotes.io/"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    ZenQuotes
                  </a>
                </span>
              </div>
            </article>
          ) : null}
        </section>
        <section className="word-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">GROW YOUR VOCABULARY</p>
              <h2>
                <BookOpen size={21} /> Word of the Day
              </h2>
            </div>
          </div>

          {wordLoading ? (
            <p className="countries-message">Discovering today's word...</p>
          ) : wordError ? (
            <p className="countries-message">{wordError}</p>
          ) : wordData ? (
            <article className="word-card">
              <div className="word-title-row">
                <h3>{wordData.word}</h3>
                {wordData.phonetic && (
                  <span className="word-phonetic">{wordData.phonetic}</span>
                )}
              </div>

              {wordData.meanings.map((meaning, index) => (
                <div className="word-meaning" key={`${meaning.partOfSpeech}-${index}`}>
                  <span className="word-part-of-speech">
                    {meaning.partOfSpeech || 'Definition'}
                  </span>

                  {meaning.definitions.slice(0, 2).map((definition, definitionIndex) => (
                    <div
                      className="word-definition"
                      key={`${definition.definition}-${definitionIndex}`}
                    >
                      <p>{definition.definition}</p>
                      {definition.example && (
                        <p className="word-example">“{definition.example}”</p>
                      )}
                    </div>
                  ))}
                </div>
              ))}

              <div className="card-footer">
                <span>Learn a little every day.</span>
                <span>Powered by Free Dictionary API</span>
              </div>
            </article>
          ) : null}
        </section>
                <section className="history-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">EXPLORE THE PAST</p>
              <h2>
                <History size={21} />
                This Day in History
              </h2>
            </div>
          </div>

          {historyLoading ? (
            <p className="countries-message">Discovering events from this day...</p>
          ) : historyError ? (
            <p className="countries-message">{historyError}</p>
          ) : historyData ? (
            <div className="history-list">
              {historyData.events.map((event, index) => (
                <article
                  className="history-card"
                  key={`${event.year}-${index}`}
                >
                  <span className="history-year">{event.year}</span>
                  <p>{event.title}</p>

                  {event.pages[0]?.url && (
                    <a
                      href={event.pages[0].url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Read more on Wikipedia ↗
                    </a>
                  )}
                </article>
              ))}

              <p className="history-attribution">
                Historical events from Wikipedia
              </p>
            </div>
          ) : null}
        </section>
        <section className="section-heading">
          <div>
            <p className="eyebrow">YOUR UNIVERSE, AT A GLANCE</p>
            <h2>Explore your workspace</h2>
          </div>
          <span className="module-count">06 MODULES</span>
        </section>

        <section className="module-grid">

          <article className="module-card weather-card">
            <div className="card-top">
              <span className="module-icon"><CloudSun size={22} /></span>
              <ArrowUpRight size={18} />
            </div>

            <p className="card-category">ENVIRONMENT · PUNE</p>
            <h3>Weather</h3>

            {weatherLoading ? (
              <p className="card-description">Loading current weather...</p>
            ) : weatherError ? (
              <p className="card-description">{weatherError}</p>
            ) : weather ? (
              <>
                <div className="weather-reading">
                  <span className="weather-temperature">
                    {Math.round(weather.current.temperature_2m)}°
                  </span>
                  <div>
                    <p className="weather-condition">{weather.condition}</p>
                    <p className="weather-feels">
                      Feels like {Math.round(weather.current.apparent_temperature)}°
                    </p>
                  </div>
                </div>

                <p className="card-description">
                  Humidity {weather.current.relative_humidity_2m}% · Wind{' '}
                  {weather.current.wind_speed_10m} km/h
                </p>
              </>
            ) : null}

            <div className="card-footer">
              <span className="mini-dot" />
              Live weather data
            </div>
          </article>


          <article className="module-card world-card">
            <div className="card-top">
              <span className="module-icon"><Compass size={22} /></span>
              <ArrowUpRight size={18} />
            </div>
            <p className="card-category">OUR PLANET</p>
            <h3>World Explorer</h3>
            <p className="card-description">Discover countries, cultures, flags, and fascinating places around the globe.</p>
            <div className="card-footer">Explore the world <span>↗</span></div>
          </article>

          <article className="module-card news-card">
            <div className="card-top">
              <span className="module-icon"><Newspaper size={22} /></span>
              <ArrowUpRight size={18} />
            </div>
            <p className="card-category">THE LATEST</p>
            <h3>Newsroom</h3>
            <p className="card-description">Stay informed with headlines and stories shaping the world around you.</p>
            <div className="card-footer">Your world, updated <span>↗</span></div>
          </article>

          <article className="module-card space-card">
            <div className="card-top">
              <span className="module-icon"><Orbit size={22} /></span>
              <ArrowUpRight size={18} />
            </div>
            <p className="card-category">BEYOND EARTH</p>
            <h3>Space</h3>
            <p className="card-description">Explore astronomy pictures, celestial discoveries, and the mysteries of space.</p>
            <div className="card-footer">Look up and wonder <span>↗</span></div>
          </article>

          <article className="module-card joke-card">
            <div className="card-top">
              <span className="module-icon"><Laugh size={22} /></span>
              <ArrowUpRight size={18} />
            </div>
            <p className="card-category">A MOMENT OF FUN</p>
            <h3>JokeBox</h3>
            <p className="card-description">Take a break, find a laugh, and add a little fun to your day.</p>
            <div className="card-footer">A little joy goes far <span>↗</span></div>
          </article>

          <article className="module-card github-card">
            <div className="card-top">
              <span className="module-icon"><Code2 size={22} /></span>
              <ArrowUpRight size={18} />
            </div>
            <p className="card-category">FOR BUILDERS</p>
            <h3>Developer Hub</h3>
            <p className="card-description">Discover GitHub projects, developer tools, and ideas worth building.</p>
            <div className="card-footer">Build something great <span>↗</span></div>
          </article>
        </section>

        <section className="newsroom-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">THE LATEST</p>
              <h2>
                <Newspaper size={21} /> Newsroom
              </h2>
            </div>

            <select
              className="news-category-select"
              value={newsCategory}
              onChange={(event) =>
                setNewsCategory(event.target.value as NewsCategory)
              }
              aria-label="Filter news by category"
            >
              <option value="general">Top headlines</option>
              <option value="business">Business</option>
              <option value="entertainment">Entertainment</option>
              <option value="health">Health</option>
              <option value="science">Science</option>
              <option value="sports">Sports</option>
              <option value="technology">Technology</option>
            </select>
          </div>

          {newsLoading ? (
            <p className="countries-message">Loading headlines...</p>
          ) : newsError ? (
            <p className="countries-message">{newsError}</p>
          ) : news.length === 0 ? (
            <p className="countries-message">No headlines available right now.</p>
          ) : (
            <div className="news-article-grid">
              {news.map((article) => (
                <article className="news-article-card" key={article.url}>
                  {article.urlToImage && (
                    <img
                      className="news-article-image"
                      src={article.urlToImage}
                      alt=""
                      loading="lazy"
                    />
                  )}

                  <div className="news-article-content">
                    <p className="card-category">
                      {article.source.name || 'News source'}
                    </p>

                    <h3>{article.title}</h3>

                    {article.description && (
                      <p className="card-description">
                        {article.description}
                      </p>
                    )}

                    <p className="news-article-date">
                      {new Date(article.publishedAt).toLocaleDateString()}
                    </p>

                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Read article ↗
                    </a>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="space-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">NASA · ASTRONOMY</p>
              <h2><Orbit size={21} /> Space</h2>
            </div>

            <input
              className="space-date-input"
              type="date"
              value={apodDate}
              max={new Date().toLocaleDateString('en-CA')}
              onChange={(event) => setApodDate(event.target.value)}
              aria-label="Choose astronomy picture date"
            />
          </div>

          {apodLoading ? (
            <p className="countries-message">Loading astronomy picture...</p>
          ) : apodError ? (
            <p className="countries-message">{apodError}</p>
          ) : apod ? (
            <article className="space-apod-card">
              {apod.media_type === 'image' ? (
                <a
                  className="space-apod-media-link"
                  href={apod.hdurl || apod.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Open NASA astronomy image"
                >
                  <img
                    className="space-apod-image"
                    src={apod.url}
                    alt={apod.title}
                    loading="lazy"
                  />
                </a>
              ) : apod.media_type === 'video' ? (
                <div className="space-apod-video">
                  <iframe
                    src={apod.url}
                    title={apod.title}
                    loading="lazy"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                </div>
              ) : (
                <p className="countries-message">
                  NASA returned an unsupported media type.
                  <a href={apod.url} target="_blank" rel="noopener noreferrer">
                    {' '}Open original media ↗
                  </a>
                </p>
              )}

              <div className="space-apod-content">
                <p className="card-category">
                  ASTRONOMY PICTURE OF THE DAY · {apod.date}
                </p>
                <h3>{apod.title}</h3>

                {apod.copyright && (
                  <p className="space-apod-credit">
                    Image credit: {apod.copyright}
                  </p>
                )}

                <p className="space-apod-explanation">{apod.explanation}</p>

                <a
                  href={apod.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View original on NASA ↗
                </a>
              </div>
            </article>
          ) : (
            <p className="countries-message">No astronomy picture available.</p>
          )}
        </section>

        <section className="jokebox-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">A MOMENT OF FUN</p>
              <h2><Laugh size={21} /> JokeBox</h2>
            </div>

            <button
              className="joke-refresh-button"
              type="button"
              onClick={() => setJokeRequest((current) => current + 1)}
              disabled={jokeLoading}
            >
              {jokeLoading ? 'Loading...' : 'Another joke ↻'}
            </button>
          </div>

          {jokeLoading ? (
            <p className="countries-message">Finding a joke...</p>
          ) : jokeError ? (
            <p className="countries-message">{jokeError}</p>
          ) : joke ? (
            <article className="joke-content-card">
              <p className="card-category">
                {joke.category.toUpperCase()} · {joke.type === 'single' ? 'QUICK JOKE' : 'SETUP & PUNCHLINE'}
              </p>

              {joke.type === 'single' ? (
                <p className="joke-text">{joke.joke}</p>
              ) : (
                <>
                  <p className="joke-text">{joke.setup}</p>
                  <p className="joke-punchline">{joke.delivery}</p>
                </>
              )}

              <div className="card-footer">
                <span>A little joy goes far.</span>
                <Laugh size={16} />
              </div>
            </article>
          ) : (
            <p className="countries-message">No joke available right now.</p>
          )}
        </section>


        <section className="countries-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">DISCOVER OUR PLANET</p>
              <h2><Globe size={21} /> World Explorer</h2>
            </div>
            <span className="module-count">
              {countries.length} COUNTRIES
            </span>
          </div>

          <input
            className="country-search"
            type="search"
            placeholder="Search countries..."
            value={countrySearch}
            onChange={(event) => setCountrySearch(event.target.value)}
          />

          {countriesLoading ? (
            <p className="countries-message">Loading countries...</p>
          ) : countriesError ? (
            <p className="countries-message">{countriesError}</p>
          ) : (
            <div className="country-grid">
              {countries
                .filter((country) =>
                  country.name.common
                    .toLowerCase()
                    .includes(countrySearch.toLowerCase()),
                )
                .sort((a, b) =>
                  a.name.common.localeCompare(b.name.common),
                )
                .slice(0, 12)
                .map((country) => (
                  <article className="country-card" key={country.cca3}>
                    <img
                      src={country.flags.png}
                      alt={country.flags.alt || `Flag of ${country.name.common}`}
                      loading="lazy"
                    />
                    <div>
                      <h3>{country.name.common}</h3>
                      <p>{country.capital?.[0] || 'Capital not listed'}</p>
                      <p>{country.region} · Population {country.population.toLocaleString()}</p>
                    </div>
                  </article>
                ))}
            </div>
          )}
        </section>
        <footer className="page-footer">
          <span>APIverse © 2026</span>
          <span>Built for the curious <Sparkles size={13} /></span>
        </footer>
      </main>
    </div>
  )
}

export default App
