# Patrón: skill que lee el proyecto y genera un artefacto

- **Origen:** video `videos/1Fg8ryhDbgk-esta-skill-de-claude-convierte-tu-web-en-un-video-de-lanzami/`
- **Fecha de evaluación:** 2026-10-18

## El claim

Una skill de Claude lee tu proyecto entero y te monta un vídeo de lanzamiento con música, movimientos y subtítulos, sin que le expliques de qué va el producto.

## Lo que no se sabe

- Nombre de la skill o del repositorio.
- Calidad real del video generado.
- Requisitos (API de video, tiempo de render, costo).
- Si funciona con cualquier proyecto o solo con ciertos stacks.

## El patrón (lo valioso)

La idea central es reutilizable y ya existe en este lab:

```
skill lee el proyecto → extrae contexto (código, README, estructura) → genera artefacto
```

Es exactamente lo que hace `video-a-skill` en este repo:

```
video → transcripción → ficha → skill y/o plan
```

La diferencia es la dirección: el video va de **contenido externo → artefacto**; la skill del video va de **proyecto propio → artefacto**.

## Aplicaciones posibles en el lab

| Dirección | Skill existente | Mejora posible |
|---|---|---|
| Video de YouTube → ficha/skill/plan | `video-a-skill` | agregar Gemini como backend |
| Proyecto propio → README actualizado | — | skill `readme-from-code` |
| Proyecto propio → video de lanzamiento | — | skill `web-to-launch-video` (requiere API de video) |
| Proyecto propio → documentación | — | skill `docs-from-code` |

## Acción

1. Si se identifica el repositorio original, estudiar su implementación.
2. Si no, el patrón ya está capturado en `video-a-skill` y en `templates/SKILL.md`.
3. No crear una skill nueva sin tener una implementación verificable.
