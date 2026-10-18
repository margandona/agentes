# IA local

Objetivo: correr modelos en esta máquina para (a) no depender de la nube, (b) entender qué se puede hacer con hardware real, (c) servir de backend a agentes del lab.

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
| 6-8 GB | 3B-8B | 8k-16k |
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

- [ ] Instalar Ollama
- [ ] Correr benchmark base (3 modelos)
- [ ] Conectar OpenCode a un modelo local
- [ ] Evaluar RAG local con `nomic-embed-text`
