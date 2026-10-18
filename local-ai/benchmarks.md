# Benchmarks de modelos locales

Máquina: HP Victus 15 · Ryzen 7 8845HS · 24 GB RAM · RTX 4050 Laptop 6 GB VRAM · Windows 11
Fecha de medición: 2026-10-18 · Ollama 0.40.4 · llama.cpp

## Resultados (prompt fijo, `num_ctx=4096`, 2 corridas por modelo)

Prompt: "Escribe una función Python que valide un email con regex. Solo el código, sin explicación."
TTFT = tiempo hasta el primer token con el modelo **ya cargado** (no incluye carga).

| Modelo | Cuant. | Tamaño en memoria | Reparto | tok/s | TTFT | Carga en frío |
|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | Q4_K_M | 5,2 GB | **18% CPU** / 82% GPU | 17,9 | 0,06 s | ~8,6 s |
| `qwen2.5-coder:7b-instruct-q4_K_S` | Q4_K_S | 4,9 GB | **16% CPU** / 84% GPU | 22,0 | 0,05 s | 12,1 s |
| `qwen2.5-coder:3b` | Q4_K_M | 2,2 GB | 100% GPU | 81,2 | 0,02 s | 4,0 s |
| `qwen2.5-coder:1.5b` | Q4_K_M | 1,2 GB | 100% GPU | 142,5 | 0,02 s | 1,8 s |

Dos corridas por modelo dieron menos de 1% de diferencia: las cifras son estables.

## Lo que dicen los números

- **Ningún 7B entra completo en 6 GB.** Aun con Q4_K_S y contexto 2048 queda 13-18% en CPU.
  La causa es el overhead de Windows (WDDM) más el buffer de cómputo, no el tamaño del modelo.
  Por eso un 7B rinde ~20 tok/s y no los ~50 que daría 100% en GPU.
- **Los modelos ≤3B sí entran completos** y son 4-7x más rápidos.
- **El 3B y el 1.5B conviven en VRAM** (2,2 + 1,2 = 3,4 GB). El 7B no convive con otro modelo:
  cuando entra el autocompletado, Ollama descarga el 7B y volver a cargarlo cuesta 12 s.
- **La carga en frío manda.** Sin `OLLAMA_KEEP_ALIVE`, cada pregunta paga 12 s de carga con el 7B.

## Consecuencia práctica

| Necesidad | Modelo |
|---|---|
| Calidad máxima posible en local | `7b-instruct-q4_K_S` (22 tok/s, aceptable en streaming) |
| Chat ágil + Tab sin recargas | `3b` (81 tok/s) + `1.5b` (142 tok/s) |
| Autocompletado | `1.5b` — con 7B tarda ~2,5 s por sugerencia y no sirve |

## Tareas fijas de evaluación (calidad, pendiente)

1. Resumir un texto de 2.000 palabras en 5 bullets.
2. Extraer JSON válido de un email (schema fijo).
3. Escribir una función Python con tests.
4. Tool calling: elegir la tool correcta entre 5 y armar los argumentos.
5. Responder en español rioplatense sin anglicismos innecesarios.

Estado: velocidades medidas; las 5 tareas de calidad todavía no se corrieron.
