# Demo Claude: de menos a más

Material para clase. Cada archivo agrega UN concepto nuevo. Recórrelos en orden.

## Requisitos
1. Instalar dependencias: `pip install -r requirements.txt`
2. Crear un archivo `.env` con tu llave: `ANTHROPIC_API_KEY=tu_llave_aqui`

## Ruta de aprendizaje (`ejemplos/`)

| # | Archivo | Concepto que enseña |
|---|---------|---------------------|
| 1 | `01_hola_claude.py` | Enviar un mensaje y recibir una respuesta |
| 2 | `02_personalidad.py` | El `system` prompt: darle un rol a Claude |
| 3 | `03_conversacion.py` | Memoria: guardar el historial de mensajes |
| 4 | `04_api_externa.py` | Qué es una API externa (sin Claude) |
| 5 | `05_tool_call.py` | Primer "tool call": Claude + una API |
| 6 | `06_bucle_herramientas.py` | Varias herramientas con un bucle |

## Demo final
`demo.py` junta todo: un asistente que decide si conviene una actividad al aire libre usando el clima real

```bash
python ejemplos/01_hola_claude.py
python demo.py
```
