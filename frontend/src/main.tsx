import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router'
import './index.css'
import './App.css'
import AppLayout from './components/layout/AppLayout'
import OverviewPage from './pages/OverviewPage'
import {
  HistoryPage,
  InspirationPage,
  JokesPage,
  NewsPage,
  SpacePage,
  WeatherPage,
  WordPage,
  WorldPage,
} from './pages/IntegrationPages'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<OverviewPage />} />
          <Route path="weather" element={<WeatherPage />} />
          <Route path="world" element={<WorldPage />} />
          <Route path="news" element={<NewsPage />} />
          <Route path="space" element={<SpacePage />} />
          <Route path="jokes" element={<JokesPage />} />
          <Route path="inspiration" element={<InspirationPage />} />
          <Route path="word" element={<WordPage />} />
          <Route path="history" element={<HistoryPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
