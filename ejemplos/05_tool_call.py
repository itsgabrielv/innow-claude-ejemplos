# =============================================================
# EJEMPLO 5: Primer "tool call" (Claude usa una herramienta)
# =============================================================
# Ahora juntamos las dos ideas anteriores:
#   - Claude (ejemplo 1) + una API externa (ejemplo 4)
#
# Claude NO ejecuta funciones. El proceso es:
#   1. Le decimos qué herramientas existen.
#   2. Claude responde "quiero usar la herramienta X con estos datos".
#   3. NOSOTROS ejecutamos la función.
#   4. Le devolvemos el resultado y Claude responde en lenguaje normal.
# =============================================================

import os
import json
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def temperatura_de(ciudad: str):
    """Función real que consulta el clima (como el ejemplo 4)."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1}, timeout=10
    ).json()
    lugar = geo["results"][0]
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lugar["latitude"], "longitude": lugar["longitude"],
                "current": "temperature_2m"}, timeout=10
    ).json()
    return clima["current"]["temperature_2m"]


# 1) Describimos la herramienta para Claude
tools = [{
    "name": "temperatura_de",
    "description": "Devuelve la temperatura actual de una ciudad.",
    "input_schema": {
        "type": "object",
        "properties": {"ciudad": {"type": "string"}},
        "required": ["ciudad"]
    }
}]

messages = [{"role": "user", "content": "¿Qué temperatura hace en Temuco?"}]

# 2) Claude decide si quiere usar la herramienta
r = client.messages.create(model="claude-haiku-4-5", max_tokens=300,
                           tools=tools, messages=messages)

if r.stop_reason == "tool_use":
    bloque = next(b for b in r.content if b.type == "tool_use")
    print(f"Claude pidió: {bloque.name}({bloque.input})")

    # 3) Ejecutamos la función real
    resultado = temperatura_de(bloque.input["ciudad"])

    # 4) Devolvemos el resultado a Claude para que responda
    messages.append({"role": "assistant", "content": r.content})
    messages.append({"role": "user", "content": [{
        "type": "tool_result",
        "tool_use_id": bloque.id,
        "content": json.dumps({"temperatura": resultado})
    }]})

    final = client.messages.create(model="claude-haiku-4-5", max_tokens=300,
                                   tools=tools, messages=messages)
    print("\nClaude:", final.content[0].text)
else:
    print(r.content[0].text)
