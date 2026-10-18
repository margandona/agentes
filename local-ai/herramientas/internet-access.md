# Acceso a internet para agentes — comparación

- **Origen:** video `videos/hkA2nxNhoQ8-el-repo-que-le-da-a-claude-ojos-para-leer-internet-en-direct/`
- **Fecha de evaluación:** 2026-10-18

## El claim del video

Un repositorio (sin nombre) le da a Claude la capacidad de leer internet en vivo, entrando a **17 plataformas** (LinkedIn, YouTube, X, Instagram, etc.) **gratis**, y ya va por las **71.000 estrellas**.

## Lo que ya tenemos: `agent-reach`

| Aspecto | `agent-reach` (instalado) | Claim del video |
|---|---|---|
| Estrellas | 138 (upstream EdisonChenAI) | 71.000 |
| Plataformas | 13+ (web, search, X, YouTube, Bilibili, Reddit, GitHub, XiaoHongShu, Douyin, WeChat, LinkedIn, Boss, RSS) | 17 |
| Costo | gratis | "gratis" |
| Herramienta base | yt-dlp, curl, mcporter, gh, xreach | no identificada |
| Licencia | MIT | no verificada |

## Estado

**No identificado.** El video no nombra el repositorio ni da un link. No se puede instalar ni comparar sin eso.

## Candidatos probables (a verificar)

| Repo | Estrellas aprox. | Plataformas | Nota |
|---|---|---|---|
| `agent-reach` (EdisonChenAI) | 138 | 13+ | ya instalado |
| `firecrawl` (mendableai) | ~25k | scraping web | no plataformas sociales |
| `Crawl4AI` | ~30k | web | no plataformas sociales |
| `browser-use` | ~50k+ | navegador completo | genérico, no 17 plataformas específicas |
| `gpt-researcher` | ~15k | investigación web | no 17 plataformas |

Ninguno coincide exactamente con "17 plataformas + LinkedIn contacts + YouTube + X + Instagram + gratis".

## Acción

1. Buscar en GitHub: `"17 platforms" LinkedIn YouTube Instagram free` o `"read internet" Claude`.
2. Si se identifica, comparar contra `agent-reach` en: cantidad de plataformas, calidad de extracción, rate limits, mantenimiento.
3. Si es mejor, migrar o complementar. Si no, descartar.

## Regla del lab

No se instala ninguna herramienta de acceso a internet sin antes verificar:
- Nombre y repo real.
- Licencia.
- Rate limits y bloqueos por IP.
- Si requiere cookies o tokens.

Mientras no se identifique, `agent-reach` sigue siendo la herramienta del lab.
