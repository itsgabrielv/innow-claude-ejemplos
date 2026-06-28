# =============================================================
# EJEMPLO 2: El "system prompt" (la personalidad)
# =============================================================
# El parámetro 'system' define CÓMO se comporta Claude.
# Es como darle un rol o instrucciones permanentes.
# Cambia el system y verás cómo cambia el estilo de la respuesta.
# =============================================================

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

pregunta = "¿Conviene volar un dron hoy?"

print("PREGUNTA:", pregunta)
print("-" * 50)

respuesta = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    # 👇 ESTA es la diferencia: le damos un rol claro.
    system=(
        "Eres profesor de un colegio técnico. "
        "Respondes corto, simple y con ejemplos prácticos. "
        "Siempre terminas con una pregunta para hacer pensar al alumno."
    ),
    messages=[
        {"role": "user", "content": pregunta}
    ]
)

print("Claude (con personalidad de profesor):\n")
print(respuesta.content[0].text)
