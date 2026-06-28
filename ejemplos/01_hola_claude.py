# =============================================================
# EJEMPLO 1: Hola, Claude 👋
# =============================================================
# Lo más básico: enviar UN mensaje y recibir UNA respuesta.
# Aquí aprendemos a crear el cliente y llamar al modelo.
# =============================================================

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# 1) Cargar la API key desde el archivo .env
load_dotenv()

# 2) Crear el cliente (el objeto que habla con Claude)
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

print("Enviando mensaje a Claude...\n")

# 3) Pedir una respuesta. Lo mínimo necesario:
#    - model: qué modelo usar
#    - max_tokens: largo máximo de la respuesta
#    - messages: la lista de mensajes (mínimo, el del usuario)
respuesta = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "Explícame qué es una API en una frase."}
    ]
)

# 4) La respuesta viene en una lista de "bloques". El texto está en el primero.
print("Claude dice:")
print(respuesta.content[0].text)
