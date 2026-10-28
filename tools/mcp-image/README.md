# image-lab (MCP)

Servidor MCP local para generar **íconos** e **imágenes** desde OpenCode.

| Herramienta | Qué hace | Necesita internet |
|---|---|---|
| `generate_icon` | Dibuja un PNG determinista (video, llave, cerebro, escudo, etc.) | No |
| `generate_image` | Genera una imagen con IA (OpenAI o Gemini) | Sí, y una clave |
| `list_providers` | Dice qué claves están configuradas y qué estilos hay | No |

## Cómo está configurado

En `~/.config/opencode/opencode.jsonc`:

```jsonc
"mcp": {
  "image-lab": {
    "type": "local",
    "command": [
      "uv", "run", "--with", "mcp>=2,<3", "--with", "pillow", "python",
      "C:/Users/marga/OneDrive/Desktop/agent-lab/tools/mcp-image/server.py"
    ],
    "enabled": true
  }
}
```

`uv` descarga `mcp` y `pillow` en un entorno efímero la primera vez. No hay que crear un `.venv` en el repo.

Verificar:

```powershell
opencode mcp list
```

Tiene que decir `✓ image-lab connected`.

## Íconos (funciona ya, sin claves)

Desde OpenCode, pedir por ejemplo:

> Generá un ícono `video` de 512 px en `tmp/iconos/video.png`.

Estilos disponibles:

`video`, `key`, `brain`, `wrench`, `shield`, `download`, `globe`, `chat`,
`sparkle`, `film`, `tag`, `eye`, `gear`, `robot`, `doc`, `mic`, `lock`,
`browser`, `box`, `code`, `layers`, `terminal`, `window`, `list`, `plug`,
`cross`, `expand`, `eraser`, `play`, `star`.

Salida: PNG con fondo circular suave y línea del color pedido (`#1F8A70` por defecto).

## Imágenes con IA (requiere clave)

El servidor lee la clave del **entorno de OpenCode**:

```powershell
# OpenAI
setx OPENAI_API_KEY "sk-..."

# o Gemini
setx GEMINI_API_KEY "..."
```

Después de `setx`, cerrar y abrir OpenCode para que tome la variable.

Modelos por defecto:

- OpenAI: `gpt-image-1` (se puede cambiar con `OPENAI_IMAGE_MODEL`).
- Gemini: `gemini-2.5-flash-image-preview` (se puede cambiar con `GEMINI_IMAGE_MODEL`).

Ejemplo:

> Generá una ilustración simple de un taller con herramientas, estilo dibujo plano, y guardala en `tmp/iconos/taller.png`.

Si no hay clave, `generate_image` devuelve un error explicado y **no** intenta descargar nada.

## Probar el servidor a mano

```powershell
uv run --with mcp --with pillow python tools/mcp-image/server.py
```

Queda esperando JSON-RPC por stdin. Para una prueba completa:

```powershell
uv run --with mcp --with pillow python tmp/test_mcp.py
```

## Límites

- Los íconos son deterministas: el mismo estilo y tamaño dan el mismo dibujo.
- La IA puede inventar texto o detalles; revisar siempre el resultado.
- `generate_image` no acepta URLs ni ejecuta código: solo prompt, proveedor y ruta de salida.
- Las imágenes generadas van a la ruta que se indique; usar `tmp/` para pruebas.
- El servidor no guarda claves ni las escribe en disco.
