import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(cidade):
    """Busca dados climáticos da API OpenWeather."""
    if not API_KEY:
        print("ERRO: OPENWEATHER_API_KEY não encontrada")
        return None

    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extrai todos os campos necessários
            weather_data = {
                "temperatura": data["main"]["temp"],
                "umidade": data["main"]["humidity"],
                "condicao": data["weather"][0]["description"],
                "condicao_main": data["weather"][0]["main"],  # "Rain", "Clouds", etc.
                "icone": data["weather"][0]["icon"],
                "vento_velocidade": data.get("wind", {}).get("speed", 0),
                "nascer_sol": data.get("sys", {}).get("sunrise"),
                "por_sol": data.get("sys", {}).get("sunset"),
                "timezone": data.get("timezone", 0)  # offset em segundos
            }
            return weather_data
        else:
            print(f"Erro na API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None

def is_noite(nascer, por_sol, timezone):
    """Verifica se é noite na cidade baseado nos horários de nascer/pôr do sol."""
    if not (nascer and por_sol):
        return False
    # Hora atual em UTC
    agora_utc = time.time()
    # Hora local na cidade
    agora_local = agora_utc + timezone
    # Verifica se está fora do intervalo [nascer, por_sol]
    return agora_local < nascer or agora_local > por_sol

def choose_cat(weather_data):
    """
    Define o humor do gato com base nos dados do clima.
    Retorna (nome_da_imagem, descricao_do_humor).
    """
    temp = weather_data["temperatura"]
    umid = weather_data["umidade"]
    cond_main = weather_data["condicao_main"]
    vento = weather_data["vento_velocidade"]
    descricao = weather_data["condicao"].lower()

    # Verifica se é noite
    noite = is_noite(weather_data["nascer_sol"], weather_data["por_sol"], weather_data["timezone"])

    # Prioridade das condições (do mais específico ao mais genérico)
    if cond_main == "Thunderstorm":
        return "storm_cat", "⛈️ Gato assustado com trovões"
    elif cond_main == "Snow":
        return "snow_cat", "❄️ Gato brincando na neve"
    elif cond_main in ["Mist", "Fog", "Haze"]:
        return "foggy_cat", "🌫️ Gato confuso no nevoeiro"
    elif vento > 10:  # vento forte (m/s)
        return "windy_cat", "💨 Gato voando com o vento"
    elif cond_main in ["Rain", "Drizzle"]:
        return "rain_cat", "🌧️ Gato observando a chuva"
    elif noite:
        return "night_cat", "🌙 Gato noturno caçando estrelas"
    elif cond_main == "Clouds" and "nublado" in descricao:
        return "cloudy_cat", "☁️ Gato preguiçoso nas nuvens"
    elif temp < 10:
        return "cold_cat", "❄️ Gato com frio"
    elif temp > 30:
        return "hot_cat", "☀️ Gato derretendo de calor"
    elif umid > 80:
        return "sleep_cat", "😴 Gato preguiçoso (umidade alta)"
    else:
        return "normal_cat", "😺 Gato tranquilo"

def get_weather_and_mood(cidade):
    """Função principal que retorna dados do clima e humor."""
    dados = get_weather_data(cidade)
    if dados is None:
        return None, "Não foi possível obter os dados do clima. Verifique o nome da cidade e sua chave da API."

    humor_nome, humor_desc = choose_cat(dados)
    dados["humor_nome"] = humor_nome
    dados["humor_desc"] = humor_desc
    return dados, None