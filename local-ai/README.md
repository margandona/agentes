# IA local

Objetivo: correr modelos en esta máquina para (a) no depender de la nube, (b) entender qué se puede hacer con hardware real, (c) servir de backend a agentes del lab.

## Máquina actual (verificado 2026-10-18)

| Pieza | Valor |
|---|---|
| Modelo | HP Victus 15-fb2xxx |
| CPU | AMD Ryzen 7 8845HS (16 hilos) |
| RAM | 24 GB (23,3 usables) |
| GPU | NVIDIA RTX 4050 Laptop, **6 GB VRAM** + Radeon 780M integrada |
| Disco libre | ~469 GB |
| Ollama | 0.40.4, con `qwen2.5-coder:7b` y `:14b` descargados |

**Lectura rápida del hardware (corregida con mediciones):** 6 GB de VRAM es el límite duro, pero **ni un 7B en Q4 entra completo**: el overhead de Windows deja ~16% de las capas en CPU y el techo es ~22 tok/s. Los modelos ≤3B sí entran 100% en GPU y son 4-7x más rápidos. Un 14B Q4 (9 GB) desborda a RAM y queda inutilizable para programar.

**Recomendación para empezar:** `qwen2.5-coder:7b-instruct-q4_K_S` para calidad, `qwen2.5-coder:3b` para velocidad (convive con el autocompletado) y `qwen2.5-coder:1.5b` para Tab. Números en `local-ai/benchmarks.md`.

**Programar en VS Code:** `local-ai/vscode-local.md` — Continue + Ollama, con la config lista en `local-ai/continue-config.yaml`.

Herramientas evaluadas (video, imagen, audio): `local-ai/herramientas/INDEX.md`.

**Generar video con IA:** `local-ai/generar-video.md` — las 3 rutas (local gratis, API por segundo, GPU alquilada) con precios comparados.

## Decisión rápida

| Querés... | Usá |
|---|---|
| Probar un modelo en 5 minutos | **Ollama** |
| Comparar modelos con GUI y ver tokens/s | **LM Studio** |
| Exprimir cada MB de VRAM / CPU-only | **llama.cpp** |
| Servir un modelo a varios clientes con throughput | **vLLM** (GPU grande) |
| Chat tipo ChatGPT contra local | **Open WebUI** |
| Usar el modelo local desde OpenCode | proveedor `ollama` |

## Instalación (Windows)

```powershell
# Ollama
winget install Ollama.Ollama

# verificar
ollama --version

# modelo chico para empezar (rápido, corre en casi todo)
ollama pull qwen3:4b

# modelo mediano, buena relación calidad/VRAM
ollama pull qwen3:8b

# ver qué está corriendo
ollama list
```

LM Studio: descargar de https://lmstudio.ai y usar el servidor local en `http://localhost:1234/v1` (compatible OpenAI).

## Regla de VRAM (aproximada, Q4)

| VRAM | Modelos cómodos | Contexto práctico |
|---|---|---|
| 6-8 GB | 3B-4B (7B parcial en CPU) | 4k-8k |
| 12 GB | 8B-14B | 16k-32k |
| 16 GB | 14B | 32k |
| 24 GB | 27B-32B | 32k-64k |
| 48 GB+ | 70B Q4 | 32k |

Si el modelo no entra en VRAM, parte se va a RAM y la velocidad cae 5-20x. Medir siempre con `ollama run` y mirar tokens/s.

## Benchmark propio

Cada modelo que se sume al lab se mide con la misma tarea:

1. **Latencia**: tiempo hasta el primer token.
2. **Throughput**: tokens/s en la misma máquina.
3. **Calidad**: 5 tareas fijas (resumen, extracción JSON, código, tool calling, español).
4. **Costo**: 0, pero anotar vatios/hora si se usa seguido.

Los resultados van a `local-ai/benchmarks.md`.

## Integración con OpenCode

Un proveedor local compatible con OpenAI se configura así (ejemplo, LM Studio en 1234):

```jsonc
{
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio",
      "options": { "baseURL": "http://localhost:1234/v1" },
      "models": { "qwen3-8b": { "name": "Qwen3 8B" } }
    }
  }
}
```

Para Ollama, OpenCode trae proveedor nativo: `ollama/<modelo>`.

## Riesgos

- **Modelos chicos alucinan tool calls.** Probar el tool calling antes de confiar.
- **Contexto largo mata velocidad.** 32k en un 8B puede ser más lento que 8k en un 14B.
- **Licencias.** Verificar antes de usar en producción (Llama, Qwen, Gemma tienen términos distintos).
- **Discos.** Un modelo de 70B Q4 pesa ~40 GB. Medir espacio antes.

## Pendientes

- [x] Instalar Ollama
- [x] Correr benchmark base (7B vs 3B vs 1.5B) → `local-ai/benchmarks.md`
- [x] Conectar OpenCode/VS Code a un modelo local → `local-ai/vscode-local.md`
- [ ] Correr las 5 tareas de calidad del benchmark (tool calling incluido)
- [ ] Evaluar RAG local con `nomic-embed-text`
- [ ] Instalar ffmpeg (lo necesita whisper para transcribir videos sin subtítulos)

Plan asociado: `plans/ia-local-rtx-4050.md`.
