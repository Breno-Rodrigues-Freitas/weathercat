"""
WeatherCat API
--------------
API FastAPI que expõe a lógica existente de cat_engine.py para
o app mobile (Flutter) consumir via HTTP.

Rodar localmente:
    pip install -r requirements.txt
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Endpoint principal:
    GET /weather-mood?cidade=London
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from cat_engine import get_weather_and_mood

app = FastAPI(title="WeatherCat API", version="1.0.0")

# Libera acesso do app Flutter (mobile) à API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WeatherMoodResponse(BaseModel):
    temperatura: float
    sensacao: float
    umidade: int
    condicao: str
    condicao_main: str
    icone: str
    vento_velocidade: float
    nascer_sol: Optional[int] = None
    por_sol: Optional[int] = None
    timezone: int
    humor_nome: str
    humor_desc: str


@app.get("/")
def root():
    return {"status": "ok", "service": "WeatherCat API"}


@app.get("/weather-mood", response_model=WeatherMoodResponse)
def weather_mood(cidade: str = Query(..., min_length=1, description="Nome da cidade, ex: London")):
    dados, erro = get_weather_and_mood(cidade.strip())

    if erro:
        raise HTTPException(status_code=404, detail=erro)

    return dados
