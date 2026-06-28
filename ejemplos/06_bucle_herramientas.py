# =============================================================
# EJEMPLO 6: Bucle de herramientas (varias seguidas)
# =============================================================
# En el ejemplo 5 ejecutamos UNA herramienta una vez.
# En la práctica, Claude puede querer usar varias herramientas
# (y a veces varias veces). Lo correcto es un BUCLE que sigue
# llamando hasta que Claude deje de pedir herramientas.
# =============================================================

import os
import json
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5"


def temperatura_de(ciudad: str):
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                       params={"name": ciudad, "count": 1}, timeout=10).json()
    if not geo.get("results"):
        return {"error": f"No encontré {ciudad}"}
    l = geo["results"][0]
    c = requests.get("https://api.open-meteo.com/v1/forecast",
                     params={"latitude": l["latitude"], "longitude": l["longitude"],
                             "current": "temperature_2m"}, timeout=10).json()
    return {"ciudad": l["name"], "temperatura": c["current"]["temperature_2m"]}


# Diccionario: nombre -> función real (así es fácil agregar más)
FUNCIONES = {"temperatura_de": temperatura_de}

tools = [{
    "name": "temperatura_de",
    "description": "Temperatura actual de una ciudad.",
    "input_schema": {"type": "object",
                     "properties": {"ciudad": {"type": "string"}},
                     "required": ["ciudad"]}
}]

messages = [{"role": "user",
             "content": "Compara la temperatura de Santiago y Valparaíso y dime cuál es mejor para correr."}]

# 🔁 Seguimos llamando mientras Claude pida herramientas
while True:
    r = client.messages.create(model=MODEL, max_tokens=500, tools=tools, messages=messages)

    if r.stop_reason != "tool_use":
        print("\nClaude:", r.content[0].text)
        break

    messages.append({"role": "assistant", "content": r.content})
    resultados = []
    for b in r.content:
        if b.type == "tool_use":
            print(f"-> Ejecutando {b.name}({b.input})")
            salida = FUNCIONES[b.name](**b.input)
            resultados.append({"type": "tool_result", "tool_use_id": b.id,
                               "content": json.dumps(salida, ensure_ascii=False)})
    messages.append({"role": "user", "content": resultados})
