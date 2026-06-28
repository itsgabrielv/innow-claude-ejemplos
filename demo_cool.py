# =============================================================
# DEMO COOL: Pokémon como métricas de ingeniería
# =============================================================
# Tool call completo con dos herramientas usando PokeAPI:
#   - obtener_pokemon(nombre): stats, tipos, peso, altura...
#   - obtener_especie(nombre): descripción, hábitat, generación...
#
# Claude consulta PokeAPI y luego explica los stats como si
# fueran KPIs de un equipo de ingeniería o de un jugador
# competitivo. Mismo flujo que demo.py pero con bucle de tools.
# =============================================================

import os
import json
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5"


def obtener_pokemon(nombre: str):
    """Consulta un Pokémon por nombre o id en PokeAPI (sin API key)."""
    print(f"   🎮 [PokeAPI] Buscando Pokémon '{nombre}'...")
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    r = requests.get(url, timeout=10)
    if r.status_code == 404:
        print(f"   ❌ [PokeAPI] No existe: {nombre}")
        return {"error": f"No encontré el Pokémon: {nombre}"}
    r.raise_for_status()
    data = r.json()

    # Aplanamos los stats a algo simple: {"hp": 35, "attack": 55, ...}
    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
    print(f"   ✅ [PokeAPI] {data['name']} listo (stats: {stats})")

    return {
        "nombre": data["name"],
        "numero": data["id"],
        "tipos": [t["type"]["name"] for t in data["types"]],
        "altura_dm": data["height"],
        "peso_hg": data["weight"],
        "habilidades": [a["ability"]["name"] for a in data["abilities"]],
        "stats": stats,
    }


def obtener_especie(nombre: str):
    """Recurso complementario: descripción, hábitat y generación."""
    print(f"   📖 [PokeAPI species] Datos de especie de '{nombre}'...")
    url = f"https://pokeapi.co/api/v2/pokemon-species/{nombre.lower()}"
    r = requests.get(url, timeout=10)
    if r.status_code == 404:
        return {"error": f"No hay especie para: {nombre}"}
    r.raise_for_status()
    data = r.json()

    # Buscamos una descripción en español, si no, la primera disponible
    texto = ""
    for e in data.get("flavor_text_entries", []):
        if e["language"]["name"] == "es":
            texto = e["flavor_text"].replace("\n", " ").replace("\f", " ")
            break

    return {
        "habitat": (data.get("habitat") or {}).get("name"),
        "generacion": data["generation"]["name"],
        "color": data["color"]["name"],
        "descripcion": texto,
    }


# Mapa: nombre de herramienta -> función real
FUNCIONES = {"obtener_pokemon": obtener_pokemon, "obtener_especie": obtener_especie}

# Le describimos las herramientas a Claude
tools = [
    {
        "name": "obtener_pokemon",
        "description": "Obtiene stats, tipos, peso, altura y habilidades de un Pokémon desde PokeAPI.",
        "input_schema": {
            "type": "object",
            "properties": {"nombre": {"type": "string", "description": "Nombre o número, ej: pikachu, 25"}},
            "required": ["nombre"],
        },
    },
    {
        "name": "obtener_especie",
        "description": "Obtiene descripción, hábitat, color y generación de un Pokémon.",
        "input_schema": {
            "type": "object",
            "properties": {"nombre": {"type": "string"}},
            "required": ["nombre"],
        },
    },
]

SYSTEM = """
Eres un analista que explica datos de Pokémon como si fueran KPIs.
Cuando tengas los stats, presenta:
1. Rol del Pokémon (tanque, atacante, soporte, velocista).
2. Sus stats explicados como métricas de un equipo de ingeniería o jugador competitivo.
3. Fortalezas y cuellos de botella.
4. Una recomendación táctica.
Sé claro, divertido y educativo. No inventes datos.
"""


def analizar(pregunta: str):
    messages = [{"role": "user", "content": pregunta}]
    print("\n🤖 [Claude] Analizando la consulta...")

    while True:
        r = client.messages.create(model=MODEL, max_tokens=1200,
                                   tools=tools, system=SYSTEM, messages=messages)
        if r.stop_reason != "tool_use":
            return r.content[0].text

        print("🛠️  [Claude] Pidió herramientas. Ejecutando PokeAPI...")
        messages.append({"role": "assistant", "content": r.content})
        resultados = []
        for b in r.content:
            if b.type == "tool_use":
                salida = FUNCIONES[b.name](**b.input)
                resultados.append({"type": "tool_result", "tool_use_id": b.id,
                                   "content": json.dumps(salida, ensure_ascii=False)})
        messages.append({"role": "user", "content": resultados})


if __name__ == "__main__":
    print("=" * 60)
    print("Demo Cool: Pokémon como métricas de equipo 🐉")
    print("=" * 60)
    print("Ejemplo: Analiza a Charizard como si fuera un jugador competitivo")
    print()

    pregunta = input("Pregunta: ")
    print(analizar(pregunta))
