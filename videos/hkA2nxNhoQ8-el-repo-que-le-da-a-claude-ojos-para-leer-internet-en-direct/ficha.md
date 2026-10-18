# Ficha de video — El repo que le da ojos a Claude para leer internet

## Metadatos

- **Título:** El Repo Que Le Da A Claude Ojos Para Leer Internet En Directo
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/hkA2nxNhoQ8
- **Duración:** 0:32
- **Fecha:** 2026-10-14
- **Relevancia para el lab (1-5):** 4 (acceso a internet para agentes, tema central)

## Tesis en una frase

> Un repositorio le da a Claude la capacidad de leer internet en vivo, entrando a 17 plataformas sin pagar APIs, y ya va por las 71.000 estrellas.

## Qué enseña

- [00:00] Anthropic no le dio ojos a Claude; este repositorio lo arregla.
- [00:00] Le da a Claude la capacidad de leer internet en vivo.
- [00:00] El repositorio tiene ~71.000 estrellas en GitHub.
- [00:10] Muchas plataformas encierran su información detrás de muros de registro, límites de peticiones o APIs de 500 dólares.
- [00:15] Con este repositorio se entra a **17 de las plataformas más grandes**, todas gratis.
- [00:20] Ejemplos: sacar contactos de LinkedIn, analizar vídeos de YouTube, revisar publicaciones virales en X, ver qué funciona en Instagram.

## Procedimiento que propone

1. Instalar el repositorio (no se nombra en el video).
2. Usarlo para que Claude lea plataformas en vivo.
3. Extraer contactos, analizar videos, revisar posts.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Repositorio sin nombre | Acceso a 17 plataformas | `agent-reach` (ya instalado) |

## Ideas aprovechables para mí

- Es exactamente el mismo problema que resuelve `agent-reach` (ya instalado en este lab). La diferencia puede estar en la cantidad de plataformas (17) y en el número de estrellas (71k vs 138).
- Si el repositorio es mejor que `agent-reach`, convendría migrar o complementar.
- El claim "todas gratis" es la promesa central: hay que verificar si hay rate limits o bloqueos por IP.

## Humo / a verificar

- [ ] **No se nombra el repositorio.** No se puede instalar ni comparar sin el nombre. Buscar en GitHub "17 platforms" + "LinkedIn" + "YouTube" + "Instagram".
- [ ] **"71.000 estrellas"** — verificar. `agent-reach` tiene 138. Si es otro repo, identificarlo.
- [ ] **"Todas gratis"** — verificar si requiere cookies, tokens o proxies para LinkedIn/X.
- [ ] **"Sin límite de peticiones"** — improbable; verificar rate limits.
- [ ] El video cierra con "la bóveda" y "link de bio": captación de tráfico, no review neutral.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| nota | `local-ai/herramientas/internet-access.md` | Comparar este repo contra `agent-reach` una vez identificado |
| skill | — | No se puede crear sin saber qué repo es |

## Citas textuales

> "Muchísimas plataformas tienen su información encerrada detrás de un muro de registro, de un límite de peticiones o de una API de 500 dólares." [00:10]
> 
> "Con este repositorio entras a 17 de las plataformas más grandes y todas ellas gratis." [00:15]
