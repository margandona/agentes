---
name: shorts-to-skill
description: >
  Turn a YouTube Short, Reel or TikTok (up to ~3 minutes) into a verified ficha
  and, only if it survives a gate, a skill. Handles ASR-garbled tool names,
  hype claims, engagement-bait CTAs and listicles that are not procedures.
  Use when the user shares a short-form video and asks "does this deserve a
  skill", "turn this short into a skill", or "what is this short really saying".
  Triggers: "procesá este short", "sacá un skill de este short", "este reel
  vale la pena", "short a skill", "analizá este short".
---

# Shorts → skill

## Qué hace

Procesa videos de formato corto (≤3 min) sin tratarlos como videos largos: recupera los nombres que el ASR destruyó, extrae las afirmaciones, las verifica contra fuentes primarias y decide si hay material para un skill o solo para una ficha.

Es la rama corta de `video-a-skill`. El resto del pipeline (`VIDEO → FICHA → SKILL → PLAN → AGENTE`) no cambia.

## Cuándo usarlo

- El usuario pasa un Short, Reel o TikTok y quiere saber si sirve.
- El video dura ≤3 min y es una lista, un demo de una herramienta o un anuncio.
- Hay que decidir rápido entre ficha, skill o descarte.
- Sospechás clickbait ("no uses X sin esto", "comenta Y", "link en la bio").

## Cuándo NO usarlo

- Videos de más de 3 min con capítulos: usá `video-a-skill` y la ficha completa.
- Contenido de entretenimiento sin herramienta ni procedimiento.
- Cuando el usuario solo quiere un resumen para leer: no hace falta skill.
- Cuando no hay forma de acceder a una fuente primaria: se puede hacer ficha, nunca skill.

## Reglas no negociables

1. **El ASR no es fuente de nombres.** Un nombre propio transcripto por YouTube es una hipótesis, no un dato.
2. **Toda cifra se verifica.** Tokens gratis, estrellas, precios, porcentajes de ahorro: sin fuente primaria, va a *Humo*.
3. **CTA ≠ contenido.** "Comenta X", "link en la bóveda", "sígueme" no son pasos. Se descarta el CTA y se busca la fuente real.
4. **Una lista no es un procedimiento.** "5 herramientas que tenés que instalar" no enseña a hacer nada; a lo sumo sugiere una práctica.
5. **Un short = una idea.** Si el video tiene cinco, se elige la que se pueda verificar y repetir.
6. **Estrellas no son evidencia de calidad.** Popularidad ≠ precisión, seguridad ni licencia compatible.

## Procedimiento

### 1. Ingesta

```powershell
python tools/transcript.py "<URL>"
```

Anotá la duración real de `metadata.json`. Si dura más de 3 min, volvé a `video-a-skill`.

**Atajo:** `python tools/draft_pack.py "<URL>"` hace la ingesta y además deja `videos/<slug>/draft.md` con gate, nombres a confirmar y afirmaciones candidatas. No reemplaza la verificación.

### 2. Recuperar nombres (paso obligatorio)

Listá cada token raro del transcript: mayúsculas, palabras que no existen, marcas conocidas mal escritas.

| Token del ASR | Candidato | Cómo se confirma |
|---|---|---|
| "Cloud Mem" | `claude-mem` | repo `thedotmack/claude-mem`, README y comando de instalación |
| "Jet Room" | `headroom` | paquete `headroom-ai`, docs del wrapper |
| "Yuks" | `hooks` | documentación oficial de hooks |
| "Cloud Setup" | `claude-code-setup` | directorio `anthropics/claude-plugins-official` |

Regla: **dos candidatos por token**, y se confirma en la fuente primaria (repo, registro de paquetes, docs oficiales). Si no se confirma, el token queda como `no identificado` y no se usa en ninguna afirmación.

### 3. Extraer afirmaciones

Tabla obligatoria en la ficha:

| Afirmación [mm:ss] | Tipo | Estado | Fuente |
|---|---|---|---|
| "1.600 millones de tokens gratis" [00:00] | cifra | engañoso: techo teórico | docs del proyecto |

Tipos: `cifra`, `capacidad`, `precio`, `integración`, `licencia`, `procedimiento`.
Estados: `verificado`, `falso`, `engañoso`, `no verificable`, `pendiente`.

Cada afirmación sin fuente queda `pendiente` y va a *Humo / a verificar* con una pregunta concreta.

### 4. Gate: ¿merece skill?

Respondé las cuatro preguntas:

1. ¿Nombra al menos una herramienta o técnica que exista y se pueda verificar?
2. ¿Hay una práctica que se repita más de una vez?
3. ¿El resultado se puede comprobar (archivo, comando, captura, diff)?
4. ¿Se puede escribir el procedimiento sin depender de un CTA o de un link privado?

Veredictos:

| Resultado | Veredicto | Salida |
|---|---|---|
| 4/4 y el video enseña los pasos | `skill-directo` | skill con timestamps |
| 4/4 pero el video solo sugiere la práctica | `skill-derivado` | skill diseñada por nosotros, marcada como adaptación |
| 2–3/4 | `solo-ficha` | ficha + nota; sin skill |
| 0–1/4 | `descartar` | una fila en `videos/INDEX.md` con el motivo |

`skill-derivado` es legítimo: el video aporta el problema, no el método. Se declara en *Origen* y no se le atribuyen pasos que el video no da.

### 5. Ficha corta

Copiar [`templates/ficha-short.md`](../../templates/ficha-short.md) a `videos/<slug>/ficha.md`. La ficha corta prioriza afirmaciones sobre enseñanzas, y no rellena secciones vacías: si no hay procedimiento, se dice.

### 6. Proponer y escribir

En el chat, una línea:

```
veredicto: skill-derivado — <una línea>
skill: <nombre> — <una línea>
no: <qué se descarta y por qué>
```

Esperar aprobación. Después escribir **un solo** `skills/<nombre>/SKILL.md` desde `templates/SKILL.md`, con `## Origen` apuntando al video y al timestamp.

### 7. Registrar

- `videos/INDEX.md`: fila con relevancia y artefactos.
- `skills/INDEX.md` y `plans/INDEX.md` si corresponde.
- Espejar el skill en `.opencode/skills/` y `.agents/skills/`.

## Salida esperada

```
videos/<slug>/
  metadata.json
  transcript.txt
  ficha.md            # plantilla corta, con tabla de afirmaciones
skills/<nombre>/SKILL.md   # solo si el gate dio skill-directo o skill-derivado
```

**Criterio de éxito:** cada afirmación tiene estado y fuente; cada nombre propio tiene confirmación; el veredicto se puede defender con la tabla, no con una corazonada.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Creerle el nombre al ASR | skill sobre una tool que no existe | Recuperar nombres y confirmar en repo/registro |
| Convertir un listicle en skill | "instalá estas 5 cosas" sin pasos | Aplicar el gate; a lo sumo `skill-derivado` sobre la práctica |
| Tomar el CTA como fuente | "el link está en la bio" | Buscar el repo o los docs; si no aparece, queda pendiente |
| Repetir cifras de marketing | "unlimited", "1.600 M gratis" | Verificar el número y explicar qué mide |
| Tratar estrellas como validación | "75k estrellas, debe funcionar" | Buscar límites, licencia, issues y evidencia de precisión |
| Ficha rellena | secciones inventadas para completar el template | Usar la plantilla corta y escribir "no aplica" |
| Skill sin verificación | no se puede probar que funcionó | Definir salida observable y criterio de éxito |

## Origen

- `videos/hVlnCKQXYkk-comenta-claude-y-recibe-los-5-plugins-para-claude-code-claud/` [00:00], [00:33], [01:03] — lista de cinco herramientas, sin procedimiento y con CTA.
- `videos/-1t8wdk8O14-prueba-tu-lanzamiento-con-clientes-falsos-mirofish-en-claude/` [00:00], [00:31] — demo de producto con afirmación falsa de "gratis dentro de Claude".
- Método: adaptación del pipeline de `docs/metodologia.md` para formato corto; knobs de verificación inspirados en la sección *Humo / a verificar* de las fichas del repo. Verificado el 2026-10-27.
