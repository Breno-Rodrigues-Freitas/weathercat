import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da API
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(cidade):
    """
    Busca dados climáticos da API OpenWeather.
    Retorna um dicionário com temperatura, condição, umidade e ícone,
    ou None em caso de erro.
    """
    if not API_KEY:
        print("ERRO: OPENWEATHER_API_KEY não encontrada no arquivo .env")
        return None

    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",        # Celsius
        "lang": "pt_br"           # Descrição em português
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "temperatura": data["main"]["temp"],
                "condicao": data["weather"][0]["description"],
                "umidade": data["main"]["humidity"],
                "icone": data["weather"][0]["icon"]  # código do ícone (pode ser usado futuramente)
            }
        else:
            # Log detalhado do erro (aparecerá no terminal)
            print(f"Erro na API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None

def choose_cat(weather_data):
    """
    Define o humor do gato com base nos dados do clima.
    Retorna uma tupla: (nome_da_imagem, descrição_do_humor)
    Os nomes das imagens correspondem aos arquivos na pasta images/.
    """
    temp = weather_data["temperatura"]
    cond = weather_data["condicao"].lower()
    umid = weather_data["umidade"]

    # Lógica de humor (você pode ajustar os limiares como preferir)
    if any(palavra in cond for palavra in ["chuva", "rain", "pancadas"]):
        return "rain_cat", "🌧️ Gato observando a chuva"
    elif temp < 10:
        return "cold_cat", "❄️ Gato com frio"
    elif temp > 30:
        return "hot_cat", "☀️ Gato derretendo de calor"
    elif umid > 80:
        return "sleep_cat", "😴 Gato preguiçoso (umidade alta)"
    else:
        return "normal_cat", "😺 Gato tranquilo"

def get_weather_and_mood(cidade):
    """
    Função principal que combina a busca do clima e a escolha do humor.
    Retorna uma tupla: (dados_completos, mensagem_de_erro)
    Se dados_completos for None, a mensagem de erro explica o motivo.
    """
    dados = get_weather_data(cidade)
    if dados is None:
        return None, "Não foi possível obter os dados do clima. Verifique o nome da cidade e sua chave da API."

    humor_nome, humor_desc = choose_cat(dados)
    dados["humor_nome"] = humor_nome   # nome do arquivo (sem extensão)
    dados["humor_desc"] = humor_desc   # texto descritivo
    return dados, None