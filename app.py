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

            col1, col2 = st.columns([1.1, 1], gap="large")

            with col1:
                st.markdown(f"""<div style="text-align:center;margin-bottom:14px;"><div style="color:#6666aa;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;">📍 Localização</div><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:#f5e642;">{cidade.strip().title()}</div></div>""", unsafe_allow_html=True)

                # Barra de progresso de temperatura
                temp = dados['temperatura']
                sensacao = dados['sensacao']

                # Define cor e label baseado na temperatura
                if temp <= 0:
                    cor_temp = "#48dbfb"
                    label_temp = "❄️ Gelado"
                elif temp <= 10:
                    cor_temp = "#48dbfb"
                    label_temp = "🥶 Frio"
                elif temp <= 18:
                    cor_temp = "#f5e642"
                    label_temp = "🌤️ Fresco"
                elif temp <= 26:
                    cor_temp = "#ff9f43"
                    label_temp = "😊 Agradável"
                elif temp <= 33:
                    cor_temp = "#ff6b6b"
                    label_temp = "🥵 Quente"
                else:
                    cor_temp = "#ff4757"
                    label_temp = "🔥 Muito Quente"

                # Calcula progresso (escala de -10°C a 45°C)
                temp_min, temp_max = -10, 45
                progresso = max(0, min(100, (temp - temp_min) / (temp_max - temp_min) * 100))

                st.markdown(f"""
<div style="background:#16161f;border:1px solid #22223a;border-radius:14px;padding:16px 18px;margin-bottom:12px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <div>
            <div style="color:#6666aa;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;">🌡️ Temperatura</div>
            <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:2rem;color:{cor_temp};line-height:1.1;margin-top:2px;">{temp}°C</div>
            <div style="color:#555568;font-size:0.75rem;margin-top:2px;">Sensação: {sensacao}°C</div>
        </div>
        <div style="background:{cor_temp}22;color:{cor_temp};font-size:0.75rem;font-weight:700;padding:6px 12px;border-radius:50px;letter-spacing:0.5px;">{label_temp}</div>
    </div>
    <div style="margin-top:8px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="color:#444466;font-size:0.65rem;">-10°C</span>
            <span style="color:#444466;font-size:0.65rem;">45°C</span>
        </div>
        <div style="background:#22223a;border-radius:50px;height:8px;width:100%;overflow:hidden;">
            <div style="height:100%;width:{progresso}%;background:linear-gradient(90deg,#48dbfb,#f5e642,#ff9f43,#ff4757);border-radius:50px;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

                st.markdown(f"""<div style="text-align:center;margin:8px 0 12px;"><span style="background:#22223a;color:#d8d8e8;font-size:0.85rem;padding:6px 16px;border-radius:50px;">🌥️ {dados['condicao'].capitalize()}</span></div>""", unsafe_allow_html=True)

                # Badges visuais de umidade e vento
                umidade = dados['umidade']
                vento = dados['vento_velocidade']

                # Cor da umidade baseada no nível
                if umidade < 30:
                    cor_umidade = "#ff6b6b"
                    label_umidade = "Seco"
                elif umidade < 60:
                    cor_umidade = "#f5e642"
                    label_umidade = "Agradável"
                else:
                    cor_umidade = "#48dbfb"
                    label_umidade = "Úmido"

                # Cor do vento baseada na velocidade
                if vento < 3:
                    cor_vento = "#48dbfb"
                    label_vento = "Calmo"
                elif vento < 8:
                    cor_vento = "#f5e642"
                    label_vento = "Moderado"
                else:
                    cor_vento = "#ff6b6b"
                    label_vento = "Forte"

                st.markdown(f"""
<div style="display:flex; gap:10px; margin: 10px 0;">
    <div style="
        flex:1;
        background:#16161f;
        border:1px solid #22223a;
        border-radius:14px;
        padding:12px 14px;
        text-align:center;
    ">
        <div style="font-size:1.4rem; margin-bottom:4px;">💧</div>
        <div style="color:#6666aa; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Umidade</div>
        <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1.2rem; color:{cor_umidade};">{umidade}%</div>
        <div style="
            display:inline-block;
            background:{cor_umidade}22;
            color:{cor_umidade};
            font-size:0.68rem;
            font-weight:600;
            padding:2px 8px;
            border-radius:50px;
            margin-top:4px;
            letter-spacing:0.5px;
        ">{label_umidade}</div>
    </div>
    <div style="
        flex:1;
        background:#16161f;
        border:1px solid #22223a;
        border-radius:14px;
        padding:12px 14px;
        text-align:center;
    ">
        <div style="font-size:1.4rem; margin-bottom:4px;">💨</div>
        <div style="color:#6666aa; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Vento</div>
        <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1.2rem; color:{cor_vento};">{vento} m/s</div>
        <div style="
            display:inline-block;
            background:{cor_vento}22;
            color:{cor_vento};
            font-size:0.68rem;
            font-weight:600;
            padding:2px 8px;
            border-radius:50px;
            margin-top:4px;
            letter-spacing:0.5px;
        ">{label_vento}</div>
    </div>
</div>
""", unsafe_allow_html=True)

                # Nascer e pôr do sol estilizados
                nascer = formatar_hora(dados.get('nascer_sol'), dados.get('timezone', 0))
                por_sol = formatar_hora(dados.get('por_sol'), dados.get('timezone', 0))

                st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a1a2e 0%,#16161f 100%);border:1px solid #22223a;border-radius:14px;padding:14px 16px;margin:10px 0;">
    <div style="color:#6666aa;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">☀️ Ciclo Solar</div>
    <div style="display:flex;align-items:center;gap:8px;">
        <div style="flex:1;text-align:center;">
            <div style="font-size:1.5rem;">🌅</div>
            <div style="color:#ff9f43;font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;margin-top:4px;">{nascer}</div>
            <div style="color:#6666aa;font-size:0.68rem;margin-top:2px;">Nascer</div>
        </div>
        <div style="flex:2;display:flex;flex-direction:column;align-items:center;gap:4px;">
            <div style="width:100%;height:6px;border-radius:50px;background:linear-gradient(90deg,#ff9f43,#f5e642,#f5e642,#ff6b6b);"></div>
            <div style="color:#444466;font-size:0.65rem;">dia</div>
        </div>
        <div style="flex:1;text-align:center;">
            <div style="font-size:1.5rem;">🌇</div>
            <div style="color:#ff6b6b;font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;margin-top:4px;">{por_sol}</div>
            <div style="color:#6666aa;font-size:0.68rem;margin-top:2px;">Pôr do sol</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

                st.markdown(f"""<div style="text-align:center;margin:10px 0 4px;"><span style="background:#f5e64222;color:#f5e642;font-size:0.82rem;font-weight:600;padding:6px 16px;border-radius:50px;">😸 {humor_desc}</span></div>""", unsafe_allow_html=True)

                # Hora local atual da cidade
                agora_utc = time.time()
                hora_local = datetime.fromtimestamp(agora_utc + dados['timezone']).strftime("%d/%m/%Y %H:%M")
                st.markdown(f"""<div style="text-align:center;color:#555568;font-size:0.78rem;margin-top:6px;">🕐 Hora local: {hora_local}</div>""", unsafe_allow_html=True)

            with col2:
                st.image(imagem_path, caption=humor_desc, use_container_width=True)

                # Curiosidade felina do dia
                import random
                curiosidades = [
                    "Gatos passam até 70% da vida dormindo. Vida boa, né? 😴",
                    "O ronron de um gato pode curar ossos — a frequência de 25-50Hz estimula a regeneração. 🦴",
                    "Gatos não sentem o sabor doce. Sorvete? Nem aí. 🍦",
                    "Um gato doméstico pode atingir 48 km/h em rajadas curtas. 🏃",
                    "Gatos têm 32 músculos em cada orelha. DJs naturais. 🎧",
                    "O nariz de cada gato é único como uma impressão digital. 🐾",
                    "Gatos piscam devagar para demonstrar amor e confiança. 😌",
                    "Gatos bebem água virando a língua para trás, ao contrário dos cachorros. 💧",
                    "Um grupo de gatos se chama 'clowder'. Agora você sabe. 🐱",
                    "Gatos podem fazer mais de 100 sons diferentes. Cachorros fazem apenas 10. 🔊",
                ]
                curiosidade = random.choice(curiosidades)

                st.markdown(f"""<div style="background:#16161f;border:1px solid #22223a;border-radius:14px;padding:16px;margin-top:12px;"><div style="color:#6666aa;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">🐾 Curiosidade Felina do Dia</div><div style="color:#d8d8e8;font-size:0.88rem;line-height:1.6;">{curiosidade}</div></div>""", unsafe_allow_html=True)

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