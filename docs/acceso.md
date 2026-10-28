# Acceso a los servicios del lab

Mapa de todo lo que corre (o puede correr) en esta máquina y cómo acceder.

## Servicios activos ahora

| Servicio | URL / Puerto | Tipo | Cómo abrir | Web UI |
|---|---|---|---|---|
| **OpenCode** | http://127.0.0.1:45278 | Web app + TUI | `opencode` en la terminal, o abrir la URL | Sí |
| **Ollama** | http://127.0.0.1:11434 | API (sin UI) | `ollama serve` (arranca solo) | No (usar Open WebUI) |
| **VoiceStudio** | http://127.0.0.1:3900 | Backend API + MCP | Abrir la app de VoiceStudio | Sí (app de escritorio) |
| **VoiceStudio MCP** | http://127.0.0.1:3900/mcp/ | MCP para agentes | Requiere la app abierta | — |

## Servicios disponibles pero no instalados

| Servicio | Qué es | Cómo instalar | Web UI |
|---|---|---|---|
| **Open WebUI** | Chat tipo ChatGPT contra Ollama | `pip install open-webui` o Docker | Sí (localhost:3000) |
| **LTX Desktop** | Generación de video local | Descargar de GitHub Releases | Sí (app de escritorio) |
| **Continue (VS Code)** | Copilot local con Ollama | Extensión de VS Code | Sí (dentro de VS Code) |

## Cómo arrancar todo

```powershell
# 1. Ollama (si no está corriendo)
ollama serve

# 2. VoiceStudio (app de escritorio, arranca el backend en 3900)
#    Abrir desde el menú de inicio o el acceso directo

# 3. OpenCode (TUI o web)
opencode            # TUI en la terminal
opencode web        # Web UI en http://127.0.0.1:45278

# 4. Open WebUI (si está instalado)
open-webui serve    # http://localhost:3000

# 5. LTX Desktop (si está instalado)
#    Abrir desde el menú de inicio
```

## Endpoints útiles

| Endpoint | Qué devuelve |
|---|---|
| `http://127.0.0.1:3900/system/diagnose` | Estado del backend de VoiceStudio (device, RAM, VRAM, modelos) |
| `http://127.0.0.1:3900/model/loaded` | Modelos residentes en memoria |
| `http://127.0.0.1:3900/mcp/` | Servidor MCP para agentes |
| `http://127.0.0.1:11434/api/tags` | Modelos de Ollama instalados |
| `http://127.0.0.1:45278` | Interfaz web de OpenCode |

## MCP para agentes

Para que OpenCode use VoiceStudio (voz clonada, TTS, transcripción), agregar en `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "mcp": {
    "voicestudio": {
      "type": "remote",
      "url": "http://localhost:3900/mcp/",
      "enabled": true
    }
  }
}
```

Requiere que VoiceStudio esté abierto. Las tools disponibles: `generate_speech`, `clone_voice`, `transcribe`, `list_voices`, `check_health`.

### image-lab (MCP local, sin puerto)

Servidor **stdio** para generar íconos e imágenes. No abre puerto: OpenCode lo arranca con `uv` cuando inicia la sesión.

- `generate_icon`: íconos PNG deterministas, sin internet.
- `generate_image`: imágenes con IA; requiere `OPENAI_API_KEY` o `GEMINI_API_KEY`.
- `list_providers`: claves configuradas y estilos disponibles.

Configurado en `~/.config/opencode/opencode.jsonc`. Verificar con `opencode mcp list`. Detalle: [`tools/mcp-image/README.md`](../tools/mcp-image/README.md).

## Dashboard local

Un panel visual con links a todo: `local-ai/dashboard.html`. Abrilo en el navegador (doble click) y tenés los accesos en un solo lugar.

## Notas

- VoiceStudio **no** tiene web UI independiente: la app de escritorio es la interfaz. El backend (puerto 3900) es API/MCP.
- Ollama **no** tiene UI: es solo API. Para chatear contra modelos locales, usar Open WebUI o Continue en VS Code.
- OpenCode tiene TUI (terminal) y Web UI (puerto 45278). Ambas son la misma sesión.
- LTX Desktop no está instalado (no-go por VRAM de 6 GB).
- El dashboard es estático: refleja el estado al momento de creación. Para ver qué está corriendo ahora, usar `tools/doctor.ps1`.
