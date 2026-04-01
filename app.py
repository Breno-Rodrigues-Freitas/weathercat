import streamlit as st
import os
import time
from datetime import datetime
from cat_engine import get_weather_and_mood

# Configuração da página
st.set_page_config(
    page_title="WeatherCat",
    page_icon="🐱",
    layout="centered"
)

st.markdown("""
<style>
    /* Fonte e cores base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo escuro suave */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Títulos */
    h1, h2, h3 {
        color: #ffd966;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Botões bonitos */
    .stButton > button {
        background: linear-gradient(90deg, #ff9966, #ff5e62);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Sidebar (opcional) */
    .css-1d391kg, .css-163ttbj {
        background: rgba(20, 20, 40, 0.95);
        border-right: 1px solid #ffd96620;
    }

    /* ===== REMOVER QUADROS ===== */
    /* Remove fundo e padding dos elementos que envolvem dados */
    .element-container, .stMarkdown, .stDataFrame, .stAlert {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 8px !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }

    /* Deixa os textos claros e sem caixas */
    .stMarkdown p, .stMarkdown div, .stMarkdown ul, .stMarkdown li {
        color: #f0f0f0 !important;
        font-size: 1rem;
        line-height: 1.5;
        background: transparent !important;
    }

    /* Inputs continuam funcionais e bonitos */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: #2a2a3a !important;
        border: 1px solid #ffd966 !important;
        border-radius: 30px !important;
        color: white !important;
        padding: 8px 16px !important;
    }
    .stTextInput label, .stSelectbox label {
        color: #ffd966 !important;
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.image("images/cat_animation.gif", use_container_width=True)
st.title(" WeatherCat")
st.markdown("Descubra o clima e o humor do gato na sua cidade!")

# Entrada do usuário (a variável cidade é definida aqui)
cidade = st.text_input("Digite o nome da cidade", placeholder="Ex: London, São Paulo")

def formatar_hora(timestamp_utc, timezone_segundos):
    """Converte timestamp UTC para hora local e retorna string HH:MM."""
    if timestamp_utc is None:
        return "Não disponível"
    # Converte para hora local
    hora_local = datetime.fromtimestamp(timestamp_utc + timezone_segundos)
    return hora_local.strftime("%H:%M")

def imagem_existe(caminho):
    """Verifica se o arquivo de imagem existe."""
    return os.path.isfile(caminho)

if st.button("Ver clima e humor do gato"):
    if not cidade.strip():
        st.warning("Por favor, digite o nome de uma cidade.")
    else:
        with st.spinner("Consultando o tempo..."):
            dados, erro = get_weather_and_mood(cidade.strip())

        if erro:
            st.error(f"😿 {erro}")
            st.image("images/sleep_cat.webp", caption="Gato dormindo de tédio...")
        else:
            # Define o caminho da imagem baseado no humor
            imagem_nome = dados['humor_nome'] + ".webp"
            imagem_path = f"images/{imagem_nome}"

            # Se a imagem não existir, usa normal_cat.webp como fallback
            if not imagem_existe(imagem_path):
                st.warning(f"Imagem {imagem_nome} não encontrada. Usando imagem padrão.")
                imagem_path = "images/normal_cat.webp"
                humor_desc = dados['humor_desc'] + " (imagem padrão)"
            else:
                humor_desc = dados['humor_desc']

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Clima em {cidade}")
                st.metric("Temperatura", f"{dados['temperatura']} °C")
                st.write(f"**Condição:** {dados['condicao'].capitalize()}")
                st.write(f"**Umidade:** {dados['umidade']}%")
                st.write(f"**Vento:** {dados['vento_velocidade']} m/s")
                
                # Novos campos: nascer e pôr do sol
                nascer = formatar_hora(dados.get('nascer_sol'), dados.get('timezone', 0))
                por_sol = formatar_hora(dados.get('por_sol'), dados.get('timezone', 0))
                st.write(f" Nascer do sol: {nascer}")
                st.write(f" Pôr do sol: {por_sol}")
                
                st.write(f"**Humor:** {humor_desc}")

                # Hora local atual da cidade
                agora_utc = time.time()
                hora_local = datetime.fromtimestamp(agora_utc + dados['timezone']).strftime("%d/%m/%Y %H:%M:%S")
                st.write(f" Hora local: {hora_local}")

                st.write(f" Sensação térmica: {dados['sensacao']} °C")

            with col2:
                st.image(imagem_path, caption=humor_desc, use_container_width=True)

            st.divider()
            st.caption("WeatherCat – Trazendo o humor felino para o seu dia a dia☁️😺")

# Barra lateral (opcional)
st.sidebar.header("Sobre")
st.sidebar.info(
    "Este app usa a API do OpenWeather para obter dados climáticos "
    "e um gatinho que muda de humor de acordo com o tempo.\n\n"
    "Imagens personalizadas tornam a experiência mais divertida!" \
    "Todos Diretos Reservados - Breno Rodrigues Freitas"
)