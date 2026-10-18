# Programar en VS Code con IA local

Guía para usar Ollama desde VS Code con Continue, sin nube.
Hardware: RTX 4050 Laptop **6 GB VRAM** + 24 GB RAM (ver `local-ai/README.md`).
Números medidos en esta máquina: `local-ai/benchmarks.md`.
Config lista para copiar: `local-ai/continue-config.yaml`.

## Qué modelo usar (medido, no estimado)

| Uso en VS Code | Modelo | Velocidad real | Por qué |
|---|---|---|---|
| Chat, explicar código, escribir una función | `qwen2.5-coder:7b-instruct-q4_K_S` | 22 tok/s | Lo mejor que entra en local; en streaming se siente bien |
| Chat ágil + Tab sin recargas | `qwen2.5-coder:3b` | 81 tok/s | 100% GPU; convive con el autocompletado |
| Autocompletado con Tab | `qwen2.5-coder:1.5b` | 142 tok/s | 1,2 GB, respuesta casi instantánea |
| **Descartado** | `qwen2.5-coder:14b` | — | 9 GB: no entra ni de cerca, corre en RAM |

**Dato clave:** ningún 7B entra completo en 6 GB. Aun en Q4_K_S queda 16% en CPU y rinde ~22 tok/s en vez de ~50. Es el techo real de esta notebook.

**Ojo con alternar modelos:** el 7B (4,9 GB) + el 1.5B (1,2 GB) no entran juntos. Cada vez que el autocompletado se activa, Ollama descarga el 7B, y la próxima pregunta de chat paga **12 s** de recarga. Si vas a usar mucho Tab y chat mezclados, elegí el **3B** para chat: entran los dos y no hay recargas.

## Paso 1 — Modelos

```powershell
ollama pull qwen2.5-coder:7b-instruct-q4_K_S
ollama pull qwen2.5-coder:3b
ollama pull qwen2.5-coder:1.5b
ollama list
```

Verificación: los tres aparecen listados (≈4,5 GB · 1,9 GB · 1,0 GB).

## Paso 2 — Evitar los 12 s de carga en frío

```powershell
setx OLLAMA_KEEP_ALIVE "30m"
```

Cerrar y reabrir la terminal para que tome la variable. Sin esto, la primera pregunta después de un rato paga la carga completa del modelo.

## Paso 3 — Continue en VS Code

1. Extensión **Continue** (`continue.continue`): ya está instalada.
2. Abrir la barra lateral de Continue (ícono en la actividad de la izquierda).
3. Si pide proveedor, elegir **Ollama**.

## Paso 4 — Config

La config activa es `%USERPROFILE%\.continue\config.yaml`. Conviene respaldarla antes de pisarla (comandos desde la raíz del repo).

```powershell
Copy-Item "$env:USERPROFILE\.continue\config.yaml" "$env:USERPROFILE\.continue\config.yaml.bak" -Force
Copy-Item ".\local-ai\continue-config.yaml" "$env:USERPROFILE\.continue\config.yaml" -Force
```

Verificación: en el selector de modelos de Continue aparecen los tres Qwen. Para chat, elegir el 7B (calidad) o el 3B (velocidad).

> El archivo trae los roles ya asignados: `chat`/`edit` para el 7B, `chat` extra para el 3B, `autocomplete` solo para el 1.5B. Si la versión de Continue rechaza el YAML, usar el botón de configuración de la extensión y cargar los modelos desde la UI con los mismos valores.

## Paso 5 — Evitar sugerencias duplicadas

Si GitHub Copilot está activo, apagar su autocompletado inline (`github.copilot.enable`) para que no compita con el de Continue.

## Verificación (esto define si sirve)

1. **Autocompletado:** escribir el inicio de una función Python y esperar el ghost text. Debe aparecer en ~1 s.
2. **Chat con contexto:** seleccionar un archivo y preguntar "¿qué hace esta función?"; debe citar el archivo correcto.
3. **Edición:** pedir un cambio puntual y aceptar el diff.
4. **Sin recargas:** usar Tab y después chat; si el chat tarda >10 s en arrancar, es el swap de modelos → pasar a 3B.
5. **Anotar** tok/s y TTFT en `local-ai/benchmarks.md` si cambia algo (driver, versión de Ollama).

## Problemas típicos

| Síntoma | Causa | Arreglo |
|---|---|---|
| "Connection refused" | Ollama no está corriendo | Abrir la app o `ollama serve` |
| Primer token en >10 s | Modelo descargado de VRAM | `setx OLLAMA_KEEP_ALIVE "30m"` y reiniciar |
| Chat lento después de usar Tab | Swap 7B ↔ 1.5B | Usar el 3B para chat |
| ~20 tok/s y no más | 7B parcialmente en CPU (techo del hardware) | Aceptarlo o bajar a 3B |
| Autocompletado no aparece | Rol mal asignado | Revisar `roles: [autocomplete]` y recargar la ventana |
| Sugerencias malas | Modelo chico para el contexto | 3B/7B en chat; 1.5B solo para Tab |
| Continue no ve el modelo | `apiBase` incorrecto | `http://localhost:11434` y recargar |

## Expectativa honesta

Esto sirve para autocompletar, explicar código y escribir funciones aisladas con privacidad total y costo cero. **No** reemplaza a un modelo grande en refactors de varios archivos, debugging con mucho contexto ni diseño de arquitectura: ahí un 7B alucina con seguridad. Para eso conviene seguir usando un modelo de nube.
