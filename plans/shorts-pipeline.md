# Plan: pipeline para Shorts

- **Origen:** `videos/hVlnCKQXYkk-.../` [00:00]–[01:03] y `videos/-1t8wdk8O14-.../` [00:00]–[00:31]
- **Objetivo:** que un video de ≤3 min entre al pipeline con un gate explícito, nombres recuperados y afirmaciones verificadas, sin rellenar la ficha de video largo.
- **No-objetivo:** instalar OmniRoute, Headroom, Claude-Mem, Task Observer ni MiroFish. Este plan no adopta herramientas: mejora cómo las evaluamos.
- **Riesgo principal:** que el gate heurístico dé falsa confianza y descarte un video bueno (o promueva uno malo). Mitigación: el gate **aconseja**, no decide; el veredicto final queda en la ficha con evidencia.

## Estado

| Fase | Estado |
|---|---|
| 1. Plantilla `ficha-short.md` | hecho (2026-10-27) |
| 2. Skill `shorts-to-skill` | hecho (2026-10-27) |
| 3. Gate automático `tools/shorts_gate.py` | hecho y verificado (2026-10-27) |
| 4. Gancho en `video-a-skill` | hecho (2026-10-27) |
| 5. Registro y espejos | hecho (2026-10-27): drift en cero |

## Precondiciones

- [ ] `python --version` ≥ 3.11 y `python -c "import yt_dlp"` funciona.
- [ ] `git status` limpio o cambios actuales commiteados (para poder revertir).
- [ ] Los dos videos de prueba siguen accesibles: `hVlnCKQXYkk` y `-1t8wdk8O14`.

## Pasos

### 3. Gate automático

**Archivo:** `tools/shorts_gate.py`.

**Interfaz:**

```powershell
python tools/shorts_gate.py "https://youtube.com/shorts/XXXX"
python tools/shorts_gate.py "URL1" "URL2" --json
```

**Comportamiento:**

1. `yt_dlp` en modo probe: id, título, duración, canal. Sin descargar video.
2. Si hay subtítulos `es,en,es-orig`, bajarlos a `tmp/gate/<id>/` y parsearlos con las funciones de `tools/transcript.py` (importar, no duplicar).
3. Calcular señales sobre el texto:

| Señal | Detección | Por qué |
|---|---|---|
| `duracion_corta` | `duration ≤ 180` | Rutea a ficha corta |
| `cta` | "comenta", "link en la bio", "bóveda", "sígueme", "dm", "telegram" | CTA ≠ contenido |
| `cifras` | números con `%`, `millones`, `mil`, `USD`, `gratis`, `ilimitado` | Afirmaciones a verificar |
| `pasos` | imperativos: "instala", "abre", "ejecuta", "configura", "copia", "añadí", "agregá" | ¿Hay procedimiento? |
| `fuentes` | URLs, `github.com`, `docs.`, nombres de paquetes | ¿Se puede verificar? |
| `nombres_raros` | tokens con mayúscula interna o que no son español (`Cloud Code`, `Yuks`) | ASR a recuperar |

4. Veredicto **preliminar** (advisory):

| Condición | Etiqueta |
|---|---|
| `pasos` y (`fuentes` o nombres confirmables) | `prometedor` |
| `cta` y no `pasos` | `revisar: sin procedimiento, posible CTA` |
| sin `pasos`, sin `fuentes`, sin `cifras` | `descartar: sin contenido verificable` |
| cualquier otro caso | `revisar` |

5. Salida humana (default) o JSON estable:

```json
{
  "id": "hVlnCKQXYkk",
  "duration": 70,
  "signals": {"duracion_corta": true, "cta": true, "cifras": true, "pasos": false, "fuentes": false},
  "verdict": "revisar",
  "reasons": ["cta sin procedimiento", "cifras sin fuente en el video"],
  "next": "Abrir ficha corta; recuperar nombres y verificar afirmaciones."
}
```

6. Códigos de salida: `0` si procesó al menos un video, `2` si no pudo bajar subtítulos (con mensaje claro), `1` si error de uso.

**Verificación:**

```powershell
python tools/shorts_gate.py "https://youtube.com/shorts/hVlnCKQXYkk"
python tools/shorts_gate.py "https://youtube.com/shorts/-1t8wdk8O14"
```

Esperado: ambos `revisar` con `pasos: false` y `cta: true`; ninguno `prometedor`. Si el gate los marca `prometedor`, las heurísticas están mal calibradas.

**Restricciones:** no escribir fuera de `tmp/gate/`; no pedir API keys; no descargar el MP4.

**Notas de implementación (2026-10-27):**

- Se quitaron los `extractor_args` (`player_client`) del probe y de los subtítulos: en `hVlnCKQXYkk` provocaban `Requested format is not available`. Con el cliente por defecto baja bien.
- La descarga de subtítulos va en `try/except`: si un idioma falla (por ejemplo 429), se usa el que haya bajado.
- Los nombres dudosos se detectan por CamelCase y por pares de palabras capitalizadas, con lista de exclusión para arranques de frase ("Entonces Claude" no cuenta). Es una heurística: la confirmación sigue siendo manual.
- `--json` emite una línea por video (JSONL), sin rutas absolutas.

**Verificación ejecutada:**

```powershell
python tools/shorts_gate.py "https://youtube.com/shorts/hVlnCKQXYkk" --json
python tools/shorts_gate.py "https://youtube.com/shorts/-1t8wdk8O14"
```

| Caso | Esperado | Obtenido |
|---|---|---|
| `hVlnCKQXYkk` | `revisar`, `pasos: false`, `cta: true` | `revisar`; nombres: Cloud Code, Cloud Mem, Jet Room, Cloud Setup, Task Observer |
| `-1t8wdk8O14` | `revisar`, `pasos: false`, `cta: true` | `revisar`; cifras: 75.000, gratis |
| Texto con `instala` + `npm install` + repo | `prometedor` | `prometedor` |
| Texto solo con CTA | `descartar` | `descartar` |
| Video de 900 s | `revisar` con aviso de duración | `revisar` |

### 4. Gancho en `video-a-skill`

**Archivo:** `.opencode/skills/video-a-skill/SKILL.md` (y su espejo si corresponde).

Agregar al inicio del paso 1:

> Si `duration ≤ 180`, no seguir este procedimiento: usar `shorts-to-skill` y `templates/ficha-short.md`. Volver acá solo si el usuario pide explícitamente el tratamiento largo.

**Verificación:** cargar la skill en una sesión nueva y comprobar que la instrucción aparece con `grep`.

**Hecho:** se agregó la sección "Atajo para videos cortos" y una fila en Errores comunes. Verificado con `Select-String -Path .opencode/skills/video-a-skill/SKILL.md -Pattern "shorts-to-skill"`.

### 5. Registro y espejos

- `videos/INDEX.md`: ya actualizado con los dos Shorts (2026-10-27).
- `skills/INDEX.md`: agregar `shorts-to-skill`, `agent-stack-audit`, `synthetic-audience-test`.
- `plans/INDEX.md`: agregar este plan.
- `docs/herramientas-y-skills.md`: tabla de skills y mapa rápido.
- Espejar las skills nuevas en `.opencode/skills/` y `.agents/skills/`; comparar por nombre, no por cantidad.
- Dejar anotado en `docs/decisiones.md` por qué no se adoptan los cinco plugins ni MiroFish.

**Verificación del drift:**

```powershell
$canon = (Get-ChildItem skills -Directory).Name
$oc    = (Get-ChildItem .opencode/skills -Directory).Name
Compare-Object $canon $oc
```

Esperado después del paso 5: sin diferencias para las skills canónicas (`.opencode/skills` puede tener `video-a-skill` como extra local).

**Hecho:** canon 11, `.opencode/skills` 12 (extra `video-a-skill`), `.agents/skills` 11. Sin faltantes.

## Criterios de aceptación

- [x] El gate corre en Windows/PowerShell con `python tools/shorts_gate.py "<url>"`.
- [x] Los dos videos de prueba devuelven `revisar` con `pasos: false`; un texto con procedimiento real devuelve `prometedor`.
- [x] El JSON no cambia de forma entre corridas y no incluye rutas absolutas.
- [x] `video-a-skill` deriva los videos ≤180 s sin ambigüedad.
- [x] Los índices y espejos coinciden con el disco (solo queda el extra local esperado).
- [x] Cada afirmación de las dos fichas nuevas tiene estado y fuente.

## Cómo saber si falló

- El gate tarda más de 60 s por video o depende de una API key.
- Marca `prometedor` un video que solo tiene CTA y cifras.
- Marca `descartar` un video con pasos claros (falso negativo).
- Después de sincronizar, `Compare-Object` sigue mostrando faltantes.
- Alguien usa el veredicto del gate como sustituto de la tabla de afirmaciones.

## Rollback

- Fase 3: borrar `tools/shorts_gate.py` y la carpeta `tmp/gate/`; no toca datos del repo.
- Fase 4: revertir el párrafo agregado en `video-a-skill` con `git checkout -- .opencode/skills/video-a-skill/SKILL.md`.
- Fase 5: `git revert` del commit de índices; las skills nuevas se archivan en `skills/_archivo/`, no se borran.
