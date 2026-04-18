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
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Fundo */
    .stApp {
        background: #0d0d14;
        background-image:
            radial-gradient(ellipse 70% 40% at 15% 0%, #1c0a35 0%, transparent 55%),
            radial-gradient(ellipse 50% 35% at 85% 100%, #0a1830 0%, transparent 55%);
    }

    /* Títulos */
    h1 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.4rem !important;
        color: #f5e642 !important;
        letter-spacing: -1px;
    }
    h2, h3 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        color: #f5e642 !important;
    }

    /* Botão */
    .stButton > button {
        background: linear-gradient(135deg, #f5e642 0%, #ff9f43 100%);
        color: #0d0d14;
        border: none;
        border-radius: 14px;
        padding: 0.65rem 1.8rem;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245, 230, 66, 0.3);
        filter: brightness(1.06);
    }

    /* Input */
    .stTextInput > div > div > input {
        background: #16161f !important;
        border: 1.5px solid #2a2a40 !important;
        border-radius: 12px !important;
        color: #e8e8f0 !important;
        padding: 10px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #f5e642 !important;
        box-shadow: 0 0 0 3px rgba(245, 230, 66, 0.1) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #555568 !important;
    }
    .stTextInput label {
        color: #888899 !important;
        font-size: 0.85rem !important;
    }

    /* Textos gerais */
    .stMarkdown p, .stMarkdown div, .stMarkdown li {
        color: #d8d8e8 !important;
        background: transparent !important;
    }

    /* Metric */
    [data-testid="metric-container"] {
        background: #16161f !important;
        border: 1px solid #22223a !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
    }
    [data-testid="metric-container"] label {
        color: #6666aa !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f5e642 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* Textos soltos */
    .element-container .stMarkdown {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* Subheader com linha */
    h3 {
        border-bottom: 1px solid #22223a;
        padding-bottom: 8px;
        margin-bottom: 14px !important;
    }

    /* Divider */
    hr {
        border-color: #1e1e30 !important;
        margin: 20px 0 !important;
    }

    /* Caption */
    .stCaption {
        color: #444455 !important;
        text-align: center;
    }

    /* Alerts */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f0f1a !important;
        border-right: 1px solid #1e1e30 !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] div {
        color: #7777aa !important;
    }
    [data-testid="stSidebar"] h2 {
        color: #f5e642 !important;
    }

    /* Imagem arredondada */
    [data-testid="stImage"] img {
        border-radius: 16px;
    }

    /* Spinner padrão oculto */
    .stSpinner > div {
        border-top-color: #f5e642 !important;
        display: none !important;
    }
    .stSpinner {
        display: none !important;
    }

    /* Loading personalizado */
    @keyframes pawBounce {
        0%, 100% { transform: translateY(0px); opacity: 1; }
        50% { transform: translateY(-10px); opacity: 0.4; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .custom-loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        animation: fadeInUp 0.4s ease;
    }
    .paw-row {
        display: flex;
        gap: 14px;
        margin-bottom: 20px;
    }
    .paw {
        font-size: 1.8rem;
        animation: pawBounce 1s ease-in-out infinite;
    }
    .paw:nth-child(1) { animation-delay: 0s; }
    .paw:nth-child(2) { animation-delay: 0.2s; }
    .paw:nth-child(3) { animation-delay: 0.4s; }
    .loader-text {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: #f5e642;
        letter-spacing: 1px;
    }
    .loader-sub {
        color: #555568;
        font-size: 0.78rem;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.image("images/cat_animation.gif", use_container_width=True)
st.title("🐱 WeatherCat")
st.markdown("Descubra o clima e o humor do gato na sua cidade!")

# Entrada do usuário (a variável cidade é definida aqui)
cidade = st.text_input("Digite o nome da cidade", placeholder="Ex: London, São Paulo")

def formatar_hora(timestamp_utc, timezone_segundos):
    """Converte timestamp UTC para hora local e retorna string HH:MM."""
    if timestamp_utc is None:
        return "Não disponível"
    hora_local = datetime.fromtimestamp(timestamp_utc + timezone_segundos)
    return hora_local.strftime("%H:%M")

def imagem_existe(caminho):
    """Verifica se o arquivo de imagem existe."""
    return os.path.isfile(caminho)

if st.button("Ver clima e humor do gato"):
    if not cidade.strip():
        st.warning("Por favor, digite o nome de uma cidade.")
    else:
        loader = st.empty()
        loader.markdown("""
<div class="custom-loader">
    <div class="paw-row">
        <span class="paw">🐾</span>
        <span class="paw">🐾</span>
        <span class="paw">🐾</span>
        <span class="paw">🐾</span>
    </div>
    <div class="loader-text">Consultando o tempo...</div>
    <div class="loader-sub">O gato está farejando as nuvens ☁️</div>
</div>
""", unsafe_allow_html=True)
        dados, erro = get_weather_and_mood(cidade.strip())
        loader.empty()

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
                st.write(f"🌅 Nascer do sol: {nascer}")
                st.write(f"🌇 Pôr do sol: {por_sol}")

                st.write(f"**Humor:** {humor_desc}")

                # Hora local atual da cidade
                agora_utc = time.time()
                hora_local = datetime.fromtimestamp(agora_utc + dados['timezone']).strftime("%d/%m/%Y %H:%M:%S")
                st.write(f"🕐 Hora local: {hora_local}")

                st.write(f"🌡️ Sensação térmica: {dados['sensacao']} °C")

            with col2:
                st.image(imagem_path, caption=humor_desc, use_container_width=True)

            st.divider()
            st.markdown("""
<div style="text-align:center; padding: 18px 0 8px;">
    <div style="font-size:1.3rem; margin-bottom:6px;">🐱 ☁️ 😺</div>
    <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; color:#f5e642; letter-spacing:1px; margin-bottom:4px;">WeatherCat</div>
    <div style="color:#444466; font-size:0.78rem; margin-bottom:10px;">Trazendo o humor felino para o seu dia a dia</div>
    <div style="display:inline-block; height:1px; width:40px; background:linear-gradient(90deg,transparent,#f5e64260,transparent); margin-bottom:10px;"></div><br>
    <div style="color:#333350; font-size:0.72rem; letter-spacing:0.5px;">© 2025 Breno Rodrigues Freitas · Todos os direitos reservados</div>
</div>
""", unsafe_allow_html=True)

# Barra lateral estilizada
st.sidebar.markdown("""
<div style="text-align:center; padding: 10px 0 20px;">
    <div style="font-size:2.8rem; margin-bottom:6px;">🐱</div>
    <div style="
        font-family:'Syne',sans-serif;
        font-weight:800;
        font-size:1.3rem;
        color:#f5e642;
        letter-spacing:1px;
    ">WeatherCat</div>
    <div style="color:#444466; font-size:0.72rem; margin-top:2px;">v1.0 · by Breno Rodrigues</div>
</div>

<hr style="border-color:#1e1e30; margin: 0 0 20px;">

<div style="margin-bottom:20px;">
    <div style="
        color:#f5e642;
        font-family:'Syne',sans-serif;
        font-weight:700;
        font-size:0.8rem;
        letter-spacing:1.5px;
        text-transform:uppercase;
        margin-bottom:12px;
    ">📖 Sobre</div>
    <div style="color:#7777aa; font-size:0.82rem; line-height:1.7;">
        Usa a API do <strong style="color:#aaaacc;">OpenWeather</strong> para obter dados climáticos em tempo real
        e exibe um gatinho cujo humor muda com o tempo. 😺
    </div>
</div>

<hr style="border-color:#1e1e30; margin: 0 0 20px;">

<div style="margin-bottom:20px;">
    <div style="
        color:#f5e642;
        font-family:'Syne',sans-serif;
        font-weight:700;
        font-size:0.8rem;
        letter-spacing:1.5px;
        text-transform:uppercase;
        margin-bottom:12px;
    ">⚙️ Tecnologias</div>
    <div style="display:flex; flex-direction:column; gap:8px;">
        <div style="background:#16161f; border:1px solid #22223a; border-radius:10px; padding:8px 12px; color:#aaaacc; font-size:0.8rem;">🐍 Python</div>
        <div style="background:#16161f; border:1px solid #22223a; border-radius:10px; padding:8px 12px; color:#aaaacc; font-size:0.8rem;">🎈 Streamlit</div>
        <div style="background:#16161f; border:1px solid #22223a; border-radius:10px; padding:8px 12px; color:#aaaacc; font-size:0.8rem;">🌤️ OpenWeather API</div>
    </div>
</div>

<hr style="border-color:#1e1e30; margin: 0 0 20px;">

<div style="text-align:center; color:#333350; font-size:0.7rem; line-height:1.8;">
    © 2025 Breno Rodrigues Freitas<br>Todos os direitos reservados
</div>
""", unsafe_allow_html=True)