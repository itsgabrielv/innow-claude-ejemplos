import os
import json
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

# Cargamos las variables del archivo .env (ahí está la ANTHROPIC_API_KEY)
load_dotenv()

# Creamos el "cliente": es el objeto que habla con los servidores de Claude.
client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# Elegimos el modelo. Haiku es rápido y barato, ideal para clases.
MODEL = "claude-haiku-4-5"


def buscar_ciudad(nombre_ciudad: str):
    """
    Convierte una ciudad en latitud, longitud y zona horaria usando Open-Meteo.
    No requiere API key.
    """
    print(f"   🌍 [API ciudad] Buscando coordenadas de '{nombre_ciudad}'...")

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": nombre_ciudad,
        "count": 1,
        "language": "es",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        print(f"   ❌ [API ciudad] No se encontró: {nombre_ciudad}")
        return {"error": f"No encontré la ciudad: {nombre_ciudad}"}

    ciudad = data["results"][0]
    print(f"   ✅ [API ciudad] Encontrada: {ciudad.get('name')}, {ciudad.get('country')}")

    return {
        "nombre": ciudad.get("name"),
        "pais": ciudad.get("country"),
        "latitud": ciudad.get("latitude"),
        "longitud": ciudad.get("longitude"),
        "timezone": ciudad.get("timezone", "auto")
    }


def obtener_clima(nombre_ciudad: str):
    """
    Obtiene el clima actual y pronóstico horario.
    """
    # Paso 1: pasar de "nombre de ciudad" a coordenadas
    ciudad = buscar_ciudad(nombre_ciudad)

    if "error" in ciudad:
        return ciudad

    # Paso 2: con las coordenadas pedimos el clima real
    print("   ☁️  [API clima] Consultando temperatura y viento...")
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": ciudad["latitud"],
        "longitude": ciudad["longitud"],
        "current": "temperature_2m,precipitation,wind_speed_10m",
        "hourly": "temperature_2m,precipitation_probability,wind_speed_10m",
        "forecast_days": 1,
        "timezone": ciudad["timezone"]
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    clima = response.json()
    print("   ✅ [API clima] Datos recibidos.")

    return {
        "ciudad": ciudad,
        "clima_actual": clima.get("current"),
        "pronostico_horario": clima.get("hourly")
    }


# Aquí le DESCRIBIMOS a Claude qué herramienta existe y cuándo usarla.
# Claude no ejecuta nada; solo decide si quiere llamarla y con qué datos.
tools = [
    {
        "name": "obtener_clima",
        "description": "Obtiene el clima real de una ciudad usando Open-Meteo. Úsalo cuando el usuario pregunte si conviene hacer una actividad al aire libre.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre_ciudad": {
                    "type": "string",
                    "description": "Nombre de la ciudad, por ejemplo: Santiago, Valparaíso, Temuco, Bogotá."
                }
            },
            "required": ["nombre_ciudad"]
        }
    }
]


def preguntar_a_claude(pregunta: str):
    # 'messages' es el historial de la conversación. Empieza con lo del usuario.
    messages = [
        {
            "role": "user",
            "content": pregunta
        }
    ]

    print("\n🤖 [Claude] Pensando si necesita datos del clima...")

    respuesta = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        tools=tools,
        system="""
Eres un asistente para estudiantes de colegios técnicos.
Tu tarea es ayudar a decidir si una actividad al aire libre conviene o no.

Cuando tengas datos climáticos, responde con:
1. Semáforo: VERDE, AMARILLO o ROJO.
2. Explicación simple.
3. Riesgos técnicos.
4. Lista de materiales recomendados.
5. Una pregunta final para seguir explorando.

Sé claro, práctico y educativo.
""",
        messages=messages
    )

    # Si Claude pide usar una herramienta, la ejecutamos.
    if respuesta.stop_reason == "tool_use":
        print("🛠️  [Claude] Decidió usar una herramienta. Ejecutándola...")
        tool_results = []

        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                if bloque.name == "obtener_clima":
                    # Ejecutamos NUESTRA función real con los datos que pidió Claude
                    resultado = obtener_clima(
                        bloque.input["nombre_ciudad"]
                    )

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": json.dumps(resultado, ensure_ascii=False)
                    })

        messages.append({
            "role": "assistant",
            "content": respuesta.content
        })

        messages.append({
            "role": "user",
            "content": tool_results
        })

        print("📤 [Claude] Le devolvemos los datos para que arme la respuesta final...\n")

        respuesta_final = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            tools=tools,
            system="""
Eres un asistente para estudiantes de colegios técnicos.
Usa los datos climáticos recibidos para dar una recomendación práctica.
No inventes datos. Si falta información, dilo.
""",
            messages=messages
        )

        return respuesta_final.content[0].text

    # Si no necesitó herramienta, responde directo.
    print("💬 [Claude] Respondió sin usar herramientas.\n")
    return respuesta.content[0].text


if __name__ == "__main__":
    print("=" * 60)
    print("Demo: Asistente de salida técnica con clima real")
    print("=" * 60)
    print("Ejemplo: ¿Conviene hacer una práctica con drones mañana en Valparaíso?")
    print()

    pregunta = input("Pregunta: ")
    respuesta = preguntar_a_claude(pregunta)

    print()
    print("=" * 60)
    print("Respuesta de Claude:")
    print("=" * 60)
    print(respuesta)