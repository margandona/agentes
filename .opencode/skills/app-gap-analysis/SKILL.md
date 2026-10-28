---
name: app-gap-analysis
description: >
  Read real public reviews of an app and turn them into evidence-backed fixes
  and a positioning angle for your version: what users hate, what is missing,
  what is unsolved. Every quote is verbatim and linked; thin themes are marked
  thin. Use after a recon or clone when the user asks "how do I make mine
  better", "what do people hate about X", "find the gap", "read the reviews",
  "how do I position this", or "make it sellable".
  Triggers: "analizar reseñas", "qué odian de X", "cómo mejoro el clon",
  "gap analysis", "diferenciarme de", "posicionamiento".
---

# Análisis de brechas y posicionamiento

## Qué hace

Encuentra la razón por la que tu versión merece existir: lee reseñas públicas reales, las agrupa por tema y las convierte en un plan de mejoras priorizado y un ángulo de venta. Una copia exacta no tiene motivo para venderse; esto produce el motivo.

Es la fase 8 del pipeline `replica-app-mejorada` (plan en [`plans/replica-app-mejorada.md`](../../plans/replica-app-mejorada.md) de este repo; si copiás la skill sola, funciona igual), antes de marca y lanzamiento. Método adaptado de `Jakeschincariol/replica-skill` (MIT), skill `replica-entrepreneur`.

## Cuándo usarlo

- Después de tener el recon (`replica/features.csv`) y, idealmente, el clon funcionando.
- Para decidir **si vale la pena** clonar una app: el análisis de reseñas se puede correr antes de escribir código.
- Cuando el usuario pide diferenciarse, poner precio o elegir nicho.
- Después de un parity check, para saber qué construir a continuación.

## Cuándo NO usarlo

- Para inventar testimonios o pruebas sociales de tu producto.
- Para reseñas privadas, de cuentas ajenas o detrás de un login/paywall.
- Como sustituto de investigación de mercado primaria (entrevistas, ventas) cuando hay dinero grande en juego.
- Cuando la app no tiene reseñas públicas suficientes: decilo y buscá otra señal.

## Reglas no negociables

1. **Nunca inventar.** Ni reseñas, ni citas, ni ratings, ni cantidades, ni fuentes. Si una fuente no se alcanza, se dice y se sigue.
2. **Cita textual y con link.** Se copia exactamente y se guarda la URL de la reseña o del hilo. Una fila sin link se descarta.
3. **Leer, no scrapear.** Navegación humana; respetar términos. Se permiten APIs públicas y oficiales dentro de sus términos:
   - App Store: `https://itunes.apple.com/us/rss/customerreviews/id=<APP_ID>/sortBy=mostRecent/json`
   - Hacker News: `https://hn.algolia.com/api/v1/search?query=...`
   - Reddit: API oficial bajo sus términos.
4. **Reseñas falsas, jamás.** Ni para tu app ni contra la original; es ilegal en EE. UU. (regla FTC 2024) y en muchos otros países.
5. **Los reseñadores no son tus testimonios.** Su texto es investigación; no va en la landing ni en anuncios.
6. **Muestra declarada.** Siempre decir cuántas reseñas y cuántas fuentes. Menos de 3 reseñas o una sola fuente = tema **fino**, no tendencia.
7. **No "arreglar" lo ya arreglado.** Revisar el changelog de la app antes de proponer un fix.

## Procedimiento

1. **Recolectar.** Objetivo: 100+ reseñas de al menos 3 fuentes, recientes primero.
   | Fuente | Dónde |
   |---|---|
   | App Store | ficha → Ratings and Reviews → See All, o el RSS de arriba |
   | Google Play | ficha → ver todas → ordenar por más recientes |
   | G2 / Capterra / Trustpilot | páginas de reseñas, filtrando también 1–3 estrellas |
   | Reddit | buscar "X alternative", "switched from X", "X sucks", "X vs" |
   | Hacker News | Algolia o búsqueda del sitio, mismas queries |
   | Board público de la app | roadmap o feature requests (Canny y similares) con votos |
   | Changelog | qué ya lanzaron |

   Leer también las de 3 y 4 estrellas: "me encanta, pero…" es donde están los mejores fixes.

2. **Registrar.** Un CSV `replica/reviews.csv` con cabecera:
   ```csv
   source,url,date,rating,text
   App Store,https://apps.apple.com/...,2026-08-14,2,"No puedo reprogramar sin cancelar primero"
   ```
   El texto se copia exacto, sin corregir ortografía.

3. **Agrupar y rankear.** Temas del rubro (agenda, precios, notificaciones, onboarding, permisos, performance…). Ponderación simple y explícita:
   - 1–2 estrellas ×2;
   - últimos 12 meses ×1,5;
   - cada tema: cantidad de reseñas, cantidad de fuentes y 1–2 citas con link.
   Marcar `fino` si tiene <3 reseñas o una sola fuente. Revisar a mano las reseñas negativas que no cayeron en ningún tema: suele estar ahí lo mejor.

4. **Tres listas** en `replica/fixes.md`, cada ítem con problema en una línea, cantidad de reseñas, cantidad de fuentes y citas:
   1. **Lo que odian** — quejas sobre lo que la app hace.
   2. **Lo que falta** — features pedidas por nombre.
   3. **Lo que no está resuelto** — trabajos o grupos enteros que la app ignora ("no sirve para equipos", "inútil para terapeutas"). Esto alimenta el posicionamiento.

5. **Plan de fixes.** Elegir los 5–8 mejores por `evidencia × costo de arreglarlo`. Para cada uno: qué construir, tamaño (`S/M/L`), qué fase/skill lo ejecuta y la evidencia que lo respalda. Agregar cada uno a `replica/features.csv` con `original=no`.

6. **Ángulo.** Tres opciones de posicionamiento, cada una anclada a un tema:
   ```
   Para {quién} que {odia esto de la original, en palabras simples},
   {tu app} {hace esto en su lugar}.
   Evidencia: {tema}, {n} reseñas en {n} fuentes.
   ```
   Recomendar una. Sin el nombre de la original en el nombre de tu app, anuncios ni ficha de tienda. Una página comparativa factual es una decisión legal para un abogado.

## Salida esperada

- `replica/reviews.csv` — reseñas crudas, todas con link.
- `replica/feedback.md` — temas rankeados, citas, temas finos y negativas sin clasificar.
- `replica/fixes.md` — tres listas, plan de fixes y tres ángulos con recomendación.
- Filas nuevas en `replica/features.csv`.
- Resumen en el chat que declare el tamaño de muestra y las fuentes.

**Criterio de éxito:** cada afirmación se puede rastrear a una fila con URL; el plan de fixes tiene evidencia y costo; el ángulo se puede defender con la muestra, no con una corazonada.

## Portabilidad

- Todo vive en `replica/` del proyecto donde se corre; no depende de `agent-lab`.
- No requiere el script `reviews.py` del pack original: el agente puede agrupar temas a mano. Si se quiere automatizar, se puede portar ese script (MIT) o escribir uno propio.
- El CSV es el contrato: cualquier proyecto o herramienta que lo lea puede reproducir el análisis.
- Para otro proyecto: copiar `app-gap-analysis/` a la carpeta de skills del destino. El `SKILL.md` es autosuficiente.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Presentar 3 comentarios de Reddit como tendencia | conclusión frágil, decisiones caras | Exigir ≥3 reseñas y ≥2 fuentes; marcar `fino` |
| Parafrasear una cita | pierde verificabilidad | Copiar textual y linkear |
| Inventar cantidad o rating | destruye la credibilidad del análisis | Contar y declarar la muestra real |
| Usar reseñas en la landing | problema legal y ético | Investigación interna, nunca testimonio |
| Proponer un fix ya lanzado | el usuario paga por algo que existe | Leer changelog antes |
| Confundir queja con pedido | plan de fixes desordenado | Separar odian / falta / no resuelto |

## Origen

- Video: `videos/-PItFh9VLa4-clona-cualquier-app-con-claude-y-vendela-mejorada-replica-sk/` [00:30].
- Método: adaptado de `Jakeschincariol/replica-skill` (MIT), `replica-entrepreneur/SKILL.md`; verificado el 2026-10-22.
