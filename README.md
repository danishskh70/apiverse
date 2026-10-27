# Apiverse 🌐

**Explore APIs. Discover data. Experience the web through one platform.**

Apiverse is a full-stack API exploration platform that brings multiple external APIs together in one minimalistic web application. It provides a unified interface for exploring weather information, countries, news, space-related content, random jokes, and developer information.

Built with **FastAPI, React, TypeScript, and Vite**, Apiverse demonstrates modular backend architecture, third-party API integration, RESTful API development, and modern frontend engineering.

## ✨ Features

- **Weather** — Explore weather information using external weather data APIs.
- **World Explorer** — Discover information about countries around the world.
- **Newsroom** — Access news content through an external news API.
- **Space** — Explore space-related information and content.
- **JokeBox** — Discover random jokes and enjoy interactive content.
- **Developer Hub** — Explore developer-related information and GitHub integrations.
- **Modular architecture** — Integrations are organized into independent backend modules.
- **REST API** — Exposes versioned API endpoints through FastAPI.
- **Minimalistic UI** — A clean, responsive interface focused on usability.
- **API health check** — Provides an endpoint for checking backend availability.

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI, Pydantic |
| API communication | REST, JSON, HTTPX |
| Integration architecture | Modular, plugin-based integrations |
| Frontend styling | CSS |
| Testing | Pytest |
| Development tools | Git, GitHub, uv, npm |
| Deployment | Netlify, Render |

## 🏗️ Architecture

Apiverse separates the user interface, API backend, and external data providers.

```text
                   User
                    |
                    v
          React + TypeScript
             (Frontend)
                    |
             HTTP / JSON
                    |
                    v
            FastAPI Backend
                    |
             /api/v1/...
                    |
                    v
          Integration Registry
                    |
       +------------+------------+
       |            |            |
    Weather       Newsroom    World Explorer
       |            |            |
       +------------+------------+
                    |
          +---------+---------+
          |         |         |
        Space    JokeBox   Developer Hub
          |         |         |
          +---------+---------+
                    |
                    v
             External APIs
```

Each integration has its own backend module, allowing features to be developed, tested, and maintained independently.

## 📁 Project Structure

```text
apiverse/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── integrations/
│   │   │   └── plugins/
│   │   │       ├── weather/
│   │   │       ├── world-explorer/
│   │   │       ├── news/
│   │   │       ├── space/
│   │   │       ├── jokebox/
│   │   │       └── github/
│   │   └── main.py
│   ├── .env.example
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   ├── components/
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

*Note: The tree illustrates the main architectural components; individual files may differ in the current repository.*

## 🚀 Getting Started

### Prerequisites

Install the following tools:

- Python 3.14 or a compatible version specified by the backend project
- `uv`
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/danishskh70/apiverse.git
cd apiverse
```

### 2. Configure the backend

```bash
cd backend
cp .env.example .env
```

Add the required environment variables to `backend/.env`. Configure any API keys required by your enabled integrations.

For example, the Newsroom integration uses a NewsAPI key:

```env
NEWS_API_KEY=your_newsapi_key
```

Keep your actual API keys private. Never commit `.env` files or expose secret keys in frontend code.

Install dependencies and start the backend:

```bash
uv sync
uv run uvicorn main:app --reload
```

The backend will typically be available at:

`http://127.0.0.1:8000`

### 3. Configure and start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, typically:

`http://localhost:5173`

Ensure the frontend's API configuration points to your running backend. During development, the Vite proxy can route `/api` requests to FastAPI.

## 🔌 API Endpoints

The backend exposes versioned endpoints under `/api/v1`.

| Endpoint | Purpose |
|---|---|
| `/api/health` | Check backend health |
| `/api/v1/integrations/weather` | Weather integration |
| `/api/v1/integrations/news` | News integration |
| `/api/v1/integrations/jokebox/random` | Retrieve a random joke |
| `/api/v1/integrations/word/definition?word=serendipity` | Look up a word definition |

Other integration routes provide functionality for World Explorer, Space, and Developer Hub.

Consult the backend's registered routes for the exact parameters and available operations.

### Interactive API documentation

When enabled in the current environment, FastAPI provides interactive documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Documentation availability depends on the backend configuration.

## 🌍 Live Deployment

- **Frontend:** https://apiverseexplore.netlify.app/
- **Backend API:** https://apiverse-20l2.onrender.com
- **Health check:** https://apiverse-20l2.onrender.com/api/health

The frontend communicates with the deployed backend over HTTP APIs. Production configuration must use the correct backend URL, valid environment variables, and an appropriate CORS allowlist.

## 🧪 Testing

Run backend tests from the backend directory:

```bash
cd backend
uv run pytest
```

To verify the backend health endpoint locally:

```bash
curl http://127.0.0.1:8000/api/health
```

To test the deployed service:

```bash
curl https://apiverse-20l2.onrender.com/api/health
```

## 🔐 Security and Configuration

- Store API credentials in environment variables.
- Keep secrets out of source control.
- Configure CORS for trusted frontend origins only.
- Validate incoming request parameters.
- Handle external API errors and timeouts gracefully.
- Avoid exposing provider credentials through frontend requests.
- Use HTTPS for production deployments.

## 🎯 Project Goals

Apiverse is designed to demonstrate practical full-stack engineering skills, including:

- Building REST APIs with FastAPI.
- Integrating external services into a unified application.
- Designing modular and maintainable backend systems.
- Connecting React interfaces to backend endpoints.
- Managing environment-based configuration.
- Testing backend functionality.
- Deploying frontend and backend services independently.

## 🗺️ Future Improvements

Potential improvements include:

- More public API integrations.
- Improved loading, empty, and error states.
- API request caching and rate-limit handling.
- Integration-level automated tests.
- Better API discovery and documentation.
- Saved results and personalized preferences.
- Performance and accessibility improvements.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests where appropriate.
4. Submit a pull request describing your changes.

## 📄 License

Choose and add an appropriate open-source license before distributing the project under an open-source license.

---

**Apiverse — One platform. Multiple APIs. Endless possibilities.**