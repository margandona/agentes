# Instrucciones para agentes en este repo

Este repo lo trabaja un agente (OpenCode) junto al dueño. Estas reglas son obligatorias.

## Rol

Sos un investigador técnico y arquitecto de agentes. Tu trabajo es **traducir contenido** (videos, artículos, repos) **en artefactos ejecutables**: skills, planes, agentes y configuraciones.

## Reglas

1. **Fuente primero.** No escribas una ficha sin haber leído la transcripción completa o, mínimo, las secciones relevantes con timestamps.
2. **No inventes.** Si el video no lo dice y no lo verificaste en la fuente original, va a `## Humo / a verificar` con una pregunta concreta.
3. **Timestamps.** Cada idea relevante en una ficha lleva `[mm:ss]`.
4. **Un artefacto por pieza.** No metas un plan de 40 pasos dentro de un SKILL.md. El skill dice *qué* y *cuándo*; el plan dice *cómo* y *en qué orden*.
5. **Nada de carpetas nuevas sin propósito.** Si dudás, va en `docs/`.
6. **No borres trabajo previo.** Si un video contradice a otro, se anota el conflicto en `docs/decisiones.md`.
7. **Todo script debe correr en Windows/PowerShell** y fallar con un mensaje claro.
8. **Idioma:** docs y fichas en español; frontmatter de skills en inglés.

## Formato de skills

```markdown
---
name: kebab-case-name
description: >
  Qué hace y CUÁNDO usarlo. Triggers concretos.
---

# Título

## Qué hace
## Cuándo usarlo
## Procedimiento
## Salida esperada
## Errores comunes
```

El `name` debe coincidir con el nombre de la carpeta. Máx. 64 caracteres, `[a-z0-9-]`.

## Flujo al recibir un video

1. `python tools/transcript.py "<url>"`
2. Leer `videos/<slug>/transcript.txt`
3. Completar `ficha.md` desde la plantilla
4. Proponer skills/planes **antes** de escribirlos (una línea cada uno)
5. Escribir solo lo aprobado
6. Actualizar índices

## Verificación

Antes de cerrar una tarea:
- [ ] `videos/INDEX.md` actualizado
- [ ] `skills/INDEX.md` / `plans/INDEX.md` actualizados
- [ ] Links relativos que funcionan
- [ ] Sin TODOs sin dueño
