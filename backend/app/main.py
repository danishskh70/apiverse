from fastapi import FastAPI
from app.api.integrations import router as integrations_router
from app.integrations.plugins.weather.routes import router as weather_router
from app.integrations.plugins.countries.routes import router as countries_router
from app.integrations.plugins.news.routes import router as news_router
from app.integrations.plugins.space.routes import router as space_router
from app.integrations.plugins.jokes.routes import router as jokes_router
from app.integrations.plugins.quotes.routes import router as quotes_router
from app.integrations.plugins.word.routes import router as word_router
from app.integrations.plugins.history.routes import router as history_router

app = FastAPI(
    title="APIverse",
    description="Explore more. Understand better.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

@app.get("/")
def root():
    return {"root"}

@app.get("/health",tags=["Health"])
def health():
    return {
       "status":"ok",
       "service":"apiverse",
    }

app.include_router(countries_router)
app.include_router(weather_router)
app.include_router(news_router)
app.include_router(space_router)
app.include_router(jokes_router)
app.include_router(quotes_router)
app.include_router(word_router)
app.include_router(history_router)
app.include_router(integrations_router)