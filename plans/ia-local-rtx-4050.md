# Plan: IA local en esta máquina (RTX 4050, 6 GB VRAM)

- **Origen:** hardware verificado en `local-ai/README.md` (no viene de un video)
- **Objetivo:** tener un modelo local usable desde OpenCode y saber con datos qué se puede y qué no con 6 GB de VRAM
- **No-objetivo:** fine-tuning, servir a terceros, comprar hardware
- **Riesgo principal:** perder tiempo optimizando un modelo que igual no sirve para agentes (tool calling flojo)

## Precondiciones

- [x] Ollama instalado (0.40.4)
- [x] Modelos `qwen2.5-coder:7b` y `qwen2.5-coder:14b` descargados
- [ ] ffmpeg instalado (solo si vamos a transcribir audio local)

## Pasos

1. **Línea base de velocidad** — correr cada modelo con el mismo prompt y medir tokens/s y tiempo hasta el primer token.
   - Comando: `ollama run qwen2.5-coder:7b` y cronometrar una respuesta de ~300 tokens.
   - Verificación: dos mediciones por modelo, anotadas en `local-ai/benchmarks.md`.
2. **Comparar 7b vs 14b** — mismo prompt de código, misma salida esperada.
   - Verificación: el 14b debe ser claramente mejor en calidad para justificar la caída de velocidad; si no, se descarta.
3. **Probar tool calling** — pedirle al modelo que elija entre 5 tools y arme argumentos JSON.
   - Verificación: 8/10 llamadas con JSON válido y tool correcta. Si falla, no se usa como agente.
4. **Sumar un modelo chico** — `ollama pull qwen3:4b` para tareas rápidas y contexto largo.
   - Verificación: entra completo en VRAM y responde en menos de 1s al primer token.
5. **Conectar OpenCode** — configurar el proveedor `ollama` en `~/.config/opencode/opencode.jsonc`.
   - Verificación: una sesión real de OpenCode resuelve una tarea chica (leer 2 archivos y editar 1) sin errores de tool.
6. **Decidir** — quedarse con 1 modelo para coding y 1 para tareas rápidas.
   - Verificación: la decisión queda escrita en `docs/decisiones.md`.

## Criterios de aceptación

- [ ] `local-ai/benchmarks.md` tiene al menos 3 modelos medidos con la misma tarea
- [ ] Un modelo local responde desde OpenCode
- [ ] Hay una recomendación escrita de qué modelo usar para qué

## Cómo saber si falló

- El 7b no completa tool calls válidos en 8/10 intentos.
- El 14b tarda más de 30s por respuesta útil (señal de que está en RAM).
- OpenCode se queda colgado esperando al proveedor local.

## Rollback

- Quitar el proveedor local de `opencode.jsonc` y volver al provider en la nube.
- `ollama rm <modelo>` para liberar disco.
