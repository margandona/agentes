# Plan: IA local en esta máquina (RTX 4050, 6 GB VRAM)

- **Origen:** hardware verificado en [`local-ai/README.md`](../local-ai/README.md) (no viene de un video)
- **Objetivo:** tener un modelo local usable para programar en **VS Code** (y opcionalmente OpenCode), y saber **con datos** qué se puede y qué no con 6 GB de VRAM
- **No-objetivo:** fine-tuning, servir a terceros, comprar hardware
- **Riesgo principal:** que el hardware no dé para un modelo útil y se pierda tiempo optimizando algo que igual no sirve
- **Estado:** en curso — falta validar la experiencia real en el editor y decidir 7B vs 3B

## Hardware (verificado 2026-10-18)

| Pieza | Valor |
|---|---|
| Notebook | HP Victus 15-fb2xxx, Windows 11 |
| CPU | AMD Ryzen 7 8845HS (16 hilos) |
| RAM | 24 GB (23,3 usables) |
| GPU | NVIDIA RTX 4050 Laptop, **6 GB VRAM** (6.141 MiB) |
| Disco libre | ~469 GB |
| Runtime | Ollama 0.40.4 (runner llama.cpp) |

## Precondiciones

- [x] Ollama instalado (0.40.4) y funcionando
- [x] Modelos descargados: `qwen2.5-coder:7b`, `:7b-instruct-q4_K_S`, `:3b`, `:1.5b`, `:14b`
- [x] Extensión **Continue** (`continue.continue`) instalada en VS Code
- [ ] `OLLAMA_KEEP_ALIVE` configurado (`setx OLLAMA_KEEP_ALIVE "30m"` + reabrir terminal)
- [ ] ffmpeg instalado (solo si vamos a transcribir audio local)

## Pasos

1. **[hecho] Línea base de velocidad** — mismo prompt de código, `num_ctx=4096`, dos corridas por modelo, midiendo tok/s, TTFT y reparto CPU/GPU.
   - Verificación: tabla completa en [`local-ai/benchmarks.md`](../local-ai/benchmarks.md), variación <1% entre corridas.
2. **[hecho] Descartar el 14B** — 9 GB no entran en 6 GB; corre en RAM a velocidad inutilizable.
   - Verificación: `ollama ps` muestra reparto CPU/GPU; con 14B la respuesta útil supera los 30 s.
3. **[hecho] Sumar modelos chicos** — `qwen2.5-coder:7b-instruct-q4_K_S` (mejor cuantización), `:3b` y `:1.5b` (autocompletado).
   - Verificación: 3B y 1.5B al 100% en GPU; ambos conviven en VRAM (3,4 GB combinados).
4. **[hecho] Configurar Continue en VS Code** — config versionada en [`local-ai/continue-config.yaml`](../local-ai/continue-config.yaml) y aplicada en `%USERPROFILE%\.continue\config.yaml` (backup `.bak`).
   - Verificación: los tres modelos aparecen en el selector de Continue. **Pendiente de confirmar en vivo.**
5. **Validar en el editor** — recargar VS Code, elegir modelo, probar Tab + chat.
   - Verificación: ghost text en <1 s y un chat que cita el archivo seleccionado.
   - Si el chat tarda >10 s en arrancar después de usar Tab: es el swap de modelos → pasar a 3B.
6. **Fijar `OLLAMA_KEEP_ALIVE`** — `setx OLLAMA_KEEP_ALIVE "30m"` y reabrir la terminal.
   - Verificación: dos preguntas seguidas sin los 8-12 s de carga en frío.
7. **Comparar 3B vs 7B en calidad** — 3 tareas reales del repo (explicar función, escribir test, arreglar bug chico).
   - Verificación: si el 7B no es claramente mejor, el 3B pasa a default (81 vs 22 tok/s es mucha diferencia).
8. **Probar tool calling** — elegir entre 5 tools y armar argumentos JSON.
   - Verificación: 8/10 llamadas con JSON válido y tool correcta. Si falla, no se usa como agente.
9. **Correr las 5 tareas de calidad** de `local-ai/benchmarks.md` (resumen, JSON, código, tool calling, español).
10. **Decidir y cerrar** — default definitivo de chat; actualizar `docs/decisiones.md` y `plans/INDEX.md` (estado → `hecho`).
11. **(Opcional) Conectar OpenCode** al proveedor `ollama` para tareas de agente.

## Resultados del 2026-10-18

### Velocidad medida

Método: mismo prompt, `num_ctx=4096`, modelo ya cargado, 2 corridas por modelo vía `/api/generate` (ver anexo).

| Modelo | Cuant. | En memoria | Reparto | tok/s | TTFT | Carga en frío |
|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | Q4_K_M | 5,2 GB | 18% CPU / 82% GPU | 17,9 | 0,06 s | 8,6 s |
| `qwen2.5-coder:7b-instruct-q4_K_S` | Q4_K_S | 4,9 GB | **16% CPU** / 84% GPU | **22,0** | 0,05 s | 12,1 s |
| `qwen2.5-coder:3b` | Q4_K_M | 2,2 GB | 100% GPU | **81,2** | 0,02 s | 4,0 s |
| `qwen2.5-coder:1.5b` | Q4_K_M | 1,2 GB | 100% GPU | **142,5** | 0,02 s | 1,8 s |

### Qué se aprendió (y qué se corrigió del plan original)

1. **Ningún 7B entra completo en 6 GB.** Aun en Q4_K_S y con contexto 2048 queda 13-18% en CPU. La causa no es el tamaño del modelo sino el overhead de Windows/WDDM más el buffer de cómputo. Techo real: **~22 tok/s**.
2. **El 14B quedó descartado.** 9 GB no entran: corre en RAM a velocidad inutilizable. Se deja descargado por si cambia el hardware; no es candidato.
3. **Los modelos ≤3B sí entran 100% en GPU** y son 4-7x más rápidos.
4. **El 7B no convive con el autocompletado.** Cuando entra el 1.5B, Ollama descarga el 7B y recargarlo cuesta 12 s. Con 7B como chat + Tab activo hay *swap* constante.
5. **La carga en frío manda.** Sin `KEEP_ALIVE`, cada pregunta paga 8-12 s con un 7B.
6. **El plan original asumía que un 7B entraba cómodo.** Era falso; quedó corregido en `local-ai/README.md`, `local-ai/benchmarks.md` y `docs/decisiones.md`.

### Modelo elegido para programar en VS Code

| Rol | Modelo | Motivo |
|---|---|---|
| Chat / edición (calidad) | `qwen2.5-coder:7b-instruct-q4_K_S` | 22 tok/s, lo mejor que da el hardware; aceptable en streaming |
| Chat (velocidad) | `qwen2.5-coder:3b` | 81 tok/s, 100% GPU, convive con el autocompletado |
| Autocompletado (Tab) | `qwen2.5-coder:1.5b` | 142 tok/s, 1,2 GB; con el 7B tardaría ~2,5 s y no serviría |
| Descartado | `qwen2.5-coder:14b` | No entra en VRAM |

### Artefactos generados

| Archivo | Contenido |
|---|---|
| [`local-ai/benchmarks.md`](../local-ai/benchmarks.md) | Mediciones, conclusión de hardware y tareas de calidad pendientes |
| [`local-ai/vscode-local.md`](../local-ai/vscode-local.md) | Guía paso a paso: instalar, configurar, verificar, troubleshooting |
| [`local-ai/continue-config.yaml`](../local-ai/continue-config.yaml) | Config versionada de Continue (chat 7B/3B + autocomplete 1.5B) |
| `%USERPROFILE%\.continue\config.yaml` | Config activa del editor (backup en `.bak`) |
| [`local-ai/README.md`](../local-ai/README.md) | Lectura de hardware corregida + punteros |
| [`docs/decisiones.md`](../docs/decisiones.md) | Decisión registrada con motivo y alternativa descartada |

## Criterios de aceptación

- [x] `local-ai/benchmarks.md` tiene al menos 3 modelos medidos con la misma tarea
- [x] Hay una recomendación escrita de qué modelo usar para qué
- [x] Config de Continue versionada y aplicada
- [ ] Un modelo local responde desde VS Code (Tab + chat verificados en vivo)
- [ ] Default de chat decidido con evidencia de calidad (3B vs 7B)
- [ ] Resultado de tool calling documentado

## Cómo saber si falló

- El autocompletado tarda >2 s o sugiere código irrelevante de forma sistemática.
- El chat con 7B no aporta nada que el 3B no haga (entonces el 7B no se justifica).
- El swap 7B ↔ 1.5B hace que cada interacción tenga una pausa de >10 s.
- El 3B/7B no completa tool calls válidos en 8/10 intentos → no sirve como agente, solo como chat.
- En uso real terminás volviendo a la nube: la conclusión sería "local no alcanza para programar en esta máquina" (resultado válido, se documenta igual).

## Rollback

- Restaurar `%USERPROFILE%\.continue\config.yaml.bak` y recargar VS Code.
- Sacar el rol `autocomplete` de la config si el autocompletado molesta.
- `ollama rm <modelo>` para liberar disco: `:14b` (9 GB) y `:7b` Q4_K_M (4,7 GB) son los candidatos, ya reemplazados.
- OpenCode: quitar el proveedor `ollama` de `opencode.jsonc` y volver al provider en la nube.

## Anexo: cómo se midió (reproducible)

```powershell
# con el modelo ya cargado (hacer una llamada corta antes para evitar el cold start)
$body = @{
  model   = "qwen2.5-coder:7b-instruct-q4_K_S"
  prompt  = "Escribe una funcion Python que valide un email con regex. Solo el codigo, sin explicacion."
  stream  = $false
  options = @{ num_ctx = 4096 }
} | ConvertTo-Json -Depth 4

$r = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json"
"tok/s = {0}" -f [math]::Round($r.eval_count / ($r.eval_duration / 1e9), 1)
"TTFT  = {0} s" -f [math]::Round(($r.load_duration + $r.prompt_eval_duration) / 1e9, 2)
ollama ps   # tamaño y reparto CPU/GPU real
```

Notas de método:
- `eval_count / eval_duration` = tokens de salida por segundo.
- `ollama ps` es la fuente de verdad sobre si el modelo está 100% en GPU; `ollama show <modelo>` da la cuantización.
- Para medir carga en frío: `ollama stop <modelo>`, esperar 2 s y mirar `load_duration` de la llamada siguiente.
