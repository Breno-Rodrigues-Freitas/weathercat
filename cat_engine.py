from datetime import datetime

def choose_cat(temp, weather):

    hour = datetime.now().hour

    if hour < 8:
        return "😴 Sleeping cat"

    if temp < 15:
        return "🧣 Cold cat with scarf"

    if temp > 30:
        return "🥵 Melting from heat"

    if "rain" in weather.lower():
        return "🌧️ Watching the rain"

    return "😺 Chill cat"