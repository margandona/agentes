# Ficha de video — Skill que convierte tu web en video de lanzamiento

## Metadatos

- **Título:** Esta Skill de Claude Convierte Tu Web en un Vídeo de Lanzamiento
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/1Fg8ryhDbgk
- **Duración:** 0:26
- **Fecha:** 2026-10-06
- **Relevancia para el lab (1-5):** 4 (ejemplo de skill con formato reutilizable)

## Tesis en una frase

> Una skill de Claude lee tu proyecto entero y te monta un vídeo de lanzamiento con música, movimientos y subtítulos, sin que le expliques de qué va el producto.

## Qué enseña

- [00:00] "Se acabó para los diseñadores de Motion Graphics": alguien creó una skill de Claude que convierte cualquier web en un vídeo de lanzamiento.
- [00:05] Una vez añadida a Claude Code, lee tu proyecto entero.
- [00:10] Te monta un vídeo corto de lanzamiento con música, movimientos y subtítulos.
- [00:15] No le explicas de qué va el producto: ella misma lee el proyecto.

## Procedimiento que propone

1. Añadir la skill a Claude Code.
2. La skill lee el proyecto entero.
3. Genera un vídeo de lanzamiento con música, motion y subtítulos.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Skill de Claude (sin nombre) | Web → video de lanzamiento | ninguna (no genero videos) |

## Ideas aprovechables para mí

- El patrón "la skill lee el proyecto y genera el artefacto" es exactamente lo que hace `video-a-skill` en este lab, pero para video de salida. Es una validación del enfoque.
- El claim "no le explicas de qué va el producto" implica que la skill extrae contexto del código y del README: es un patrón de skill que vale la pena replicar en nuestro formato.
- Ejemplo de skill de una sola responsabilidad y con salida verificable (un archivo de video).

## Humo / a verificar

- [ ] **No se nombra la skill ni el repositorio.** No se puede instalar ni estudiar.
- [ ] "Se acabó para los diseñadores de motion" — exageración de marketing.
- [ ] No se muestra calidad ni duración del video generado.
- [ ] No se mencionan requisitos (API de video, render, tiempo).
- [ ] El video cierra con "la bóveda": captación de tráfico.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| nota | `local-ai/herramientas/web-to-video-skill.md` | Patrón de skill "lee el proyecto y genera artefacto" |
| skill | — | No se puede crear sin el código de la skill original |

## Citas textuales

> "Una vez le añades a tu Claude Code, lee tu proyecto entero y te monta un vídeo corto de lanzamiento con música, movimientos y hasta subtítulos." [00:05]

> "Tú no le explicas de qué va el producto, simplemente lee tu propio proyecto." [00:15]
