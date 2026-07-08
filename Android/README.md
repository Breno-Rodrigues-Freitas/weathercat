# WeatherCat — App Mobile (Flutter)

Este pacote transforma o WeatherCat (antes um site Streamlit) em um app nativo
para Android/iOS, mantendo a mesma lógica e o mesmo visual.

## Estrutura

```
weathercat_app/
├── backend/          → API (FastAPI) que expõe cat_engine.py
└── flutter_app/       → App mobile em Flutter
```

A lógica de clima e humor do gato (`cat_engine.py`) **não foi alterada** —
apenas envolvida numa API para o app poder consumi-la.

---

## 1. Rodando o backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edite o .env e coloque sua chave da OpenWeather em API_KEY

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Teste no navegador: `http://localhost:8000/weather-mood?cidade=London`

### Colocando o backend online (para o app funcionar fora do seu wifi)

Recomendo o **Render** (tem plano gratuito) ou **Railway**:
1. Suba a pasta `backend/` para um repositório GitHub.
2. Crie um novo "Web Service" no Render, apontando pro repo.
3. Comando de start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Configure a variável de ambiente `API_KEY` nas configurações do serviço.
5. Copie a URL pública gerada (ex: `https://weathercat-api.onrender.com`).

---

## 2. Rodando o app Flutter

Pré-requisitos: [instalar o Flutter SDK](https://docs.flutter.dev/get-started/install)
e ter um emulador Android/iOS ou aparelho físico conectado.

```bash
cd flutter_app
flutter pub get
```

### Passo importante: imagens dos gatos

Copie todas as imagens `.webp` (e o `cat_animation.gif`) da pasta `images/`
do seu projeto Streamlit original para:

```
flutter_app/assets/images/
```

Os nomes dos arquivos devem ser mantidos (ex: `normal_cat.webp`, `rain_cat.webp`,
`storm_cat.webp`, etc.) — o app já sabe escolher a imagem certa com base no humor.

### Passo importante: URL do backend

Abra `lib/services/weather_service.dart` e ajuste a constante `baseUrl`:

- **Emulador Android**: `http://10.0.2.2:8000` (já configurado por padrão)
- **Emulador iOS**: `http://localhost:8000`
- **Celular físico na mesma rede Wi-Fi**: `http://SEU_IP_LOCAL:8000`
- **Depois do deploy**: a URL pública (ex: `https://weathercat-api.onrender.com`)

### Rodar

```bash
flutter run
```

### Gerar o instalável

```bash
# Android (.apk)
flutter build apk --release

# iOS (precisa de Mac + Xcode)
flutter build ios --release
```

O `.apk` fica em `build/app/outputs/flutter-apk/app-release.apk` e já pode
ser instalado direto no celular Android ou publicado na Play Store.

---

## O que foi mantido do original

- Toda a lógica de clima e humor do gato (`cat_engine.py`), sem alterações
- Paleta de cores, tipografia (Syne + DM Sans) e cards visuais
- Barra de progresso de temperatura, badges de umidade/vento, ciclo solar
- Tratamento de erro de "cidade não encontrada" com dicas
- Loading animado com as patinhas 🐾

## Próximos passos sugeridos

- Adicionar splash screen e ícone do app (`flutter_launcher_icons`)
- Salvar a última cidade pesquisada localmente (`shared_preferences`)
- Suporte a localização atual do usuário (GPS)
