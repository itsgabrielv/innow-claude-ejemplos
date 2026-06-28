# Demo Claude: de menos a más 🤖

Material para clase. Vas a aprender a usar la **API de Claude** y a conectarla con
**APIs externas** (tool calls), un paso a la vez. Cada archivo agrega UN concepto nuevo.

> Idea clave: programar con IA es como armar un robot por partes. Primero le enseñamos
> a hablar, después a recordar, y al final a usar herramientas. Sin apuro. 💪

> ¿No sabes usar git? Mira esta guía rápida primero: [Git para principiantes (GitHub Docs)](https://docs.github.com/es/get-started/start-your-journey/about-github-and-git)

---

## 🧰 Antes de empezar: ¿qué necesitas?

- **Python 3.10 o superior** instalado. Para revisar, abre una terminal y escribe:
  ```bash
  python --version
  ```
  Si dice `Python 3.10.x` o mayor, vas bien. (En algunos PC se usa `python3`.)
- Una **API key de Anthropic** (te la da el profesor o la sacas en https://console.anthropic.com).
- Conexión a internet (los scripts hablan con servidores en la nube).

---

## 🚀 Instalación paso a paso

1. **Abre una terminal** dentro de la carpeta del proyecto.

2. **Instala las librerías** que usan los scripts:
   ```bash
   pip install -r requirements.txt
   ```
   Esto instala: `anthropic` (para hablar con Claude), `requests` (para llamar APIs) y
   `python-dotenv` (para leer la llave secreta).

3. **Crea un archivo llamado `.env`** en la carpeta del proyecto y pega tu llave dentro:
   ```
   ANTHROPIC_API_KEY=pega_aqui_tu_llave
   ```
   ⚠️ El `.env` guarda tu llave secreta. Nunca la subas a internet ni la compartas.

4. **Listo.** Para correr cualquier ejemplo escribe `python` y el nombre del archivo:
   ```bash
   python ejemplos/01_hola_claude.py
   ```

---

## 📚 Ruta de aprendizaje (carpeta `ejemplos/`)

Corre los ejemplos **en orden**. Cada uno suma una idea nueva.

| # | Archivo | Qué aprendes | Cómo correrlo |
|---|---------|--------------|---------------|
| 1 | `01_hola_claude.py` | Enviar un mensaje y recibir respuesta | `python ejemplos/01_hola_claude.py` |
| 2 | `02_personalidad.py` | El `system` prompt: darle un rol a Claude | `python ejemplos/02_personalidad.py` |
| 3 | `03_conversacion.py` | Memoria: guardar el historial de mensajes | `python ejemplos/03_conversacion.py` |
| 4 | `04_api_externa.py` | Qué es una API externa (sin Claude) | `python ejemplos/04_api_externa.py` |
| 5 | `05_tool_call.py` | Primer "tool call": Claude + una API | `python ejemplos/05_tool_call.py` |
| 6 | `06_bucle_herramientas.py` | Varias herramientas con un bucle | `python ejemplos/06_bucle_herramientas.py` |

---

## 🎯 Demos completas

Cuando termines los ejemplos, prueba las demos grandes que juntan todo:

- **`demo.py`** — asistente que decide si conviene una actividad al aire libre usando
  el clima real (semáforo VERDE/AMARILLO/ROJO).
  ```bash
  python demo.py
  ```
- **`demo_cool.py`** — analiza un Pokémon usando PokeAPI y explica sus stats como si
  fueran métricas de un equipo. 🐉
  ```bash
  python demo_cool.py
  ```

Algunos scripts te van a **pedir que escribas algo** (una pregunta). Escríbela y presiona Enter.

---

## ❓ Si algo falla

- **`ModuleNotFoundError`** → faltan librerías. Repite el paso `pip install -r requirements.txt`.
- **`KeyError: 'ANTHROPIC_API_KEY'`** → falta el archivo `.env` o la llave. Revisa el paso 3.
- **`python: command not found`** → prueba con `python3` en vez de `python`.
- **Errores de conexión** → revisa tu internet, los scripts hablan con servidores en la nube.
