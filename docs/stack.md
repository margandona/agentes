# Stack del laboratorio

## Base (ya instalado / verificado)

| Pieza | Versión | Para qué |
|---|---|---|
| Python | 3.13 | scripts, IA local |
| Node.js | 24 | MCP, herramientas JS |
| Git | 2.55 | versionado |
| GitHub CLI | 2.96 | repos, issues |
| yt-dlp | 2026.08.19 | videos y subtítulos |
| OpenCode | — | agente de coding |
| Skill `agent-reach` | upstream | acceso a plataformas |

## IA local

Ver `local-ai/README.md`. Resumen:

- **Ollama** para probar rápido modelos chicos/medianos.
- **LM Studio** para comparar modelos con GUI.
- **llama.cpp** cuando hay que exprimir hardware.
- **vLLM** solo si hay GPU con VRAM de sobra y necesidad de serving.
- **Open WebUI** como front-end si querés chat tipo ChatGPT contra local.

## Criterio para sumar una herramienta

1. Resuelve algo que hoy hago a mano.
2. La puedo correr en esta máquina.
3. Sé cómo medir si mejora (tiempo, calidad, costo).
4. Tiene salida: puedo dejar de usarla sin perder datos.

Si no cumple 3 y 4, no entra.
