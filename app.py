import streamlit as st
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

# Entrada do usuário
cidade = st.text_input("Digite o nome da cidade", placeholder="Ex: London, São Paulo")

# Botão de busca
if st.button("Ver clima e humor do gato"):
    if not cidade.strip():
        st.warning("Por favor, digite o nome de uma cidade.")
    else:
        with st.spinner("Consultando o tempo..."):
            dados, erro = get_weather_and_mood(cidade.strip())

        if erro:
            # Exibe a mensagem de erro de forma amigável
            st.error(f"😿 {erro}")
            # Imagem fallback (caso haja erro)
            st.image("images/sleep_cat.webp", caption="Gato dormindo de tédio...")
        else:
            # Sucesso: exibe os dados e a imagem correspondente
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Clima em {cidade}")
                st.metric("Temperatura", f"{dados['temperatura']} °C")
                st.write(f"**Condição:** {dados['condicao'].capitalize()}")
                st.write(f"**Umidade:** {dados['umidade']}%")
                st.write(f"**Humor:** {dados['humor_desc']}")

            with col2:
                # Caminho completo da imagem
                imagem_path = f"images/{dados['humor_nome']}.webp"
                st.image(imagem_path, caption=dados['humor_desc'], use_container_width=True)

            # Linha separadora e mensagem final
            st.divider()
            st.caption("WeatherCat – trazendo o humor felino para o seu dia ☁️😺")

# Instruções laterais ou rodapé (opcional)
st.sidebar.header("Sobre")
st.sidebar.info(
    "Este app usa a API do OpenWeather para obter dados climáticos "
    "e um gatinho que muda de humor de acordo com o tempo.\n\n"
    "Imagens personalizadas tornam a experiência mais divertida!"
)