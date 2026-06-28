# =============================================================
# EJEMPLO 3: Conversación con memoria
# =============================================================
# Claude NO recuerda nada por sí solo. Para que "recuerde",
# nosotros guardamos TODO el historial en la lista 'messages'.
# Cada turno: usuario -> assistant -> usuario -> assistant ...
# =============================================================

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# El historial empieza vacío
messages = []

print("Chat con Claude. Escribe 'salir' para terminar.\n")

while True:
    texto = input("Tú: ")
    if texto.lower() == "salir":
        break

    # 1) Agregamos lo que dijo el usuario al historial
    messages.append({"role": "user", "content": texto})

    # 2) Mandamos TODO el historial (por eso Claude "recuerda")
    respuesta = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        system="Eres un asistente breve y amable.",
        messages=messages
    )

    texto_claude = respuesta.content[0].text
    print("Claude:", texto_claude, "\n")

    # 3) Guardamos también la respuesta de Claude para el próximo turno
    messages.append({"role": "assistant", "content": texto_claude})
