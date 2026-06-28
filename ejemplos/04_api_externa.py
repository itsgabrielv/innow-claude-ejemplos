# =============================================================
# EJEMPLO 4: Una API externa (SIN Claude todavía)
# =============================================================
# Antes de conectar Claude con una herramienta, hay que entender
# qué es una API externa. Aquí pedimos el clima a Open-Meteo,
# que es gratis y no necesita API key.
#
# Idea clave: una API es una "función" que vive en internet.
# Le mandamos datos (params) y nos devuelve datos (JSON).
# =============================================================

import requests

ciudad = "Valparaíso"

# 1) Convertir el nombre de la ciudad a coordenadas (latitud/longitud)
print(f"Buscando coordenadas de {ciudad}...")
geo = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": ciudad, "count": 1, "language": "es"},
    timeout=10
).json()

lugar = geo["results"][0]
lat = lugar["latitude"]
lon = lugar["longitude"]
print(f"  -> {lugar['name']}, {lugar['country']} ({lat}, {lon})")

# 2) Pedir el clima actual con esas coordenadas
print("Consultando el clima...")
clima = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={"latitude": lat, "longitude": lon, "current": "temperature_2m,wind_speed_10m"},
    timeout=10
).json()

actual = clima["current"]
print(f"\nTemperatura: {actual['temperature_2m']} °C")
print(f"Viento: {actual['wind_speed_10m']} km/h")
