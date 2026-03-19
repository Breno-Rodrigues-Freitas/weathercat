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

# Título e descrição
st.title("🐱 WeatherCat")
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
                st.write(f"**🌅 Nascer do sol:** {nascer}")
                st.write(f"**🌇 Pôr do sol:** {por_sol}")
                
                st.write(f"**Humor:** {humor_desc}")
                
                # Hora local atual da cidade
                agora_utc = time.time()
                hora_local = datetime.fromtimestamp(agora_utc + dados['timezone']).strftime("%d/%m/%Y %H:%M:%S")
                st.write(f"**🕐 Hora local:** {hora_local}")

            with col2:
                st.image(imagem_path, caption=humor_desc, use_container_width=True)

            st.divider()
            st.caption("WeatherCat – trazendo o humor felino para o seu dia ☁️😺")

# Barra lateral (opcional)
st.sidebar.header("Sobre")
st.sidebar.info(
    "Este app usa a API do OpenWeather para obter dados climáticos "
    "e um gatinho que muda de humor de acordo com o tempo.\n\n"
    "Imagens personalizadas tornam a experiência mais divertida!"
)