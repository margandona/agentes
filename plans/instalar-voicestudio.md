# Plan: instalar VoiceStudio y conectar su MCP

- **Origen:** `videos/mmdSu0GoBtU-clon-gratis-de-elevenlabs-voice-studio-clona-tu-voz-en-tu-or/` [00:18]
- **Objetivo:** tener clonación de voz local funcionando en esta laptop y disponible como herramienta para agentes vía MCP
- **No-objetivo:** doblar videos largos, entrenar modelos propios, publicar contenido con voz clonada
- **Riesgo principal:** usar la herramienta sin reglas de consentimiento y terminar con audio sintético de alguien sin permiso
- **Costo esperado:** $0 (solo luz y disco)
- **Tiempo estimado:** 60-90 min incluyendo descargas

## Precondiciones

- [ ] Leer `docs/consentimiento-voz.md` y aceptar las reglas
- [ ] ~10 GB libres en disco (hay 469 GB)
- [ ] Windows 10/11 x64
- [ ] Voz propia grabada, o permiso escrito de la persona cuya voz se va a clonar
- [ ] OpenCode funcionando (para la fase MCP)

## Fases

### Fase 1 — Instalación (20-30 min)

1. Descargar el instalador `VoiceStudio-Electron-<version>-win-x64.exe` desde https://github.com/debpalash/VoiceStudio/releases/latest
2. Comparar el hash con `SHA256SUMS.txt` del release
3. Instalar para el usuario actual (no requiere admin)
4. Abrir la app y dejar que prepare Python, FFmpeg y el entorno

**Verificación:** la app abre y muestra el catálogo de modelos sin errores.

**Si falla:** probar el instalador por script (`irm https://voicestudio.sh/install | iex`) y revisar `docs/install/troubleshooting.md`.

### Fase 2 — Primer arranque y motor (15-20 min)

1. En el setup, elegir **OmniVoice** (motor por defecto, 646 idiomas)
2. Descargar el modelo (~2,3 GB)
3. En **Settings → Performance** verificar el device: debería decir `cuda` con la RTX 4050; si dice `cpu`, revisar el driver NVIDIA
4. Desactivar telemetría y cualquier servicio remoto en **Settings → General/Privacy**
5. Confirmar que no hay proveedor LLM en la nube configurado para doblaje (usar NLLB local)

**Verificación:** `Settings → About → Run self-check` no reporta errores y el device es `cuda`.

**Nota:** con 6 GB de VRAM la app serializa las generaciones. No tocar `OMNIVOICE_GPU_WORKERS`.

### Fase 3 — Referencia de voz y consentimiento (10 min)

1. Grabar **30-60 segundos** de voz propia: sin música, sin ruido, tono natural
2. Guardar el audio **fuera del repo**, en una carpeta privada (ej. `%USERPROFILE%\voces\`)
3. Transcribir exactamente lo que dice el clip y guardarlo junto al audio
4. Completar el registro de consentimiento de `docs/consentimiento-voz.md` (aunque sea tu propia voz)
5. Crear el perfil en **Voice cloning → Add voice**

**Verificación:** el perfil tiene clip + transcripción, y el registro de consentimiento está completo.

**Si falla:** si la clonación suena metálica o inestable, probar un clip más limpio antes de cambiar de motor.

### Fase 4 — Prueba de calidad (10 min)

1. Generar una frase de prueba en español de ~40 palabras
2. Generar la misma frase una segunda vez (la primera es más lenta por carga de modelo)
3. Evaluar: pronunciación, naturalidad, pausas, acento
4. Si no convence, probar un motor alternativo del catálogo (IndexTTS, Qwen3-TTS) antes de descartar la herramienta
5. Anotar en `local-ai/benchmarks.md`: motor, device, tiempo por 100 palabras, VRAM

**Verificación:** una frase de 40 palabras se genera en tiempo razonable y se entiende sin esfuerzo.

**Criterio de fallo:** si en 3 motores distintos el español no es inteligible, la herramienta no sirve para este caso; se documenta y se para.

### Fase 5 — MCP para agentes (15 min)

1. Con la app abierta, verificar el backend: `curl http://localhost:3900/system/diagnose`
2. Configurar el MCP en `~/.config/opencode/opencode.jsonc`:

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

3. Definir variables de entorno del backend para no llenar el contexto de audio:

```
OMNIVOICE_MCP_OUTPUT_MODE=files
OMNIVOICE_MCP_BASE_PATH=C:\Users\marga\voces\salidas
```

4. Reiniciar OpenCode y probar en una sesión:
   - `check_health` → debe devolver JSON con device `cuda`
   - `list_voices` → debe listar el perfil creado
   - `generate_speech` con un texto corto → debe dejar un archivo en la carpeta base

**Verificación:** las tres tools responden y el audio generado existe en disco.

**Si falla:** revisar que la URL termine en `/mcp/`, que la app esté abierta y que el puerto 3900 no esté ocupado.

### Fase 6 — Doblaje de prueba (opcional, 20 min)

1. Usar un video propio de 20-30 segundos
2. Doblarlo a inglés con traducción **NLLB local**
3. Verificar que no se haya usado ningún proveedor en la nube
4. Comparar sincronización y naturalidad

**Verificación:** el video doblado se entiende y no salió tráfico a internet durante el proceso.

## Criterios de aceptación

- [ ] VoiceStudio abre y detecta la GPU (`cuda`)
- [ ] Existe un perfil de voz propio con consentimiento registrado
- [ ] Una frase de 40 palabras en español se genera y se entiende
- [ ] OpenCode ve las tools MCP y genera un archivo de audio
- [ ] Telemetría y servicios remotos desactivados
- [ ] Benchmark anotado en `local-ai/benchmarks.md`
- [ ] Nada de audio de referencia quedó dentro del repo

## Cómo saber si falló

- La app no detecta CUDA después de reinstalar el driver.
- La clonación no se parece a la voz después de 3 clips de referencia distintos.
- El MCP no responde con la app abierta (revisar logs del backend).
- El audio queda ininteligible en todos los motores probados.
- Aparece tráfico a la nube sin haberlo configurado.

## Rollback

1. Quitar el bloque `voicestudio` de `opencode.jsonc` y reiniciar OpenCode.
2. Borrar los perfiles de voz desde la app.
3. Desinstalar VoiceStudio desde Configuración → Aplicaciones.
4. Borrar modelos y datos si se quiere recuperar el disco (`%LOCALAPPDATA%\VoiceStudio` o la carpeta elegida).
5. Borrar los clips de referencia de la carpeta privada.

## Después de este plan

- Skill candidato: `tts-local` (cómo pedirle audio a VoiceStudio por MCP con criterios de calidad).
- Skill candidato: `doblaje-local` (video → transcripción → traducción → TTS → mezcla).
- Evaluar el uso combinado con LTX: video generado + locución clonada.
