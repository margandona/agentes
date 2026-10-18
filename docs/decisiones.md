# Decisiones

Formato: fecha, decisión, motivo, alternativa descartada.

## 2026-10-18 — Repo único en vez de un repo por video

**Decisión:** un solo repo con carpetas por video, skill y plan.
**Motivo:** los skills se reutilizan entre videos; separarlos fragmenta el conocimiento.
**Alternativa descartada:** un repo por video (mucho overhead, cero reutilización).

## 2026-10-18 — Un repo, dos pistas (agentes e IA local)

**Decisión:** los videos de herramientas/modelos locales no van a un repo aparte; van a `local-ai/`, con evaluación en `local-ai/herramientas/`.
**Motivo:** comparten ingesta (transcripción, ficha) e índices. Un segundo repo duplicaría el pipeline para 2-3 notas por mes.
**Alternativa descartada:** repo `local-ai-lab` separado. Se reconsidera si la pista local supera ~20 artefactos o necesita su propio pipeline de benchmarks.
**Consecuencia:** una ficha de video puede terminar en dos artefactos: procedimiento en `skills/`, herramienta en `local-ai/herramientas/`.

## 2026-10-18 — Video con IA: solo documentado, ruta API recomendada

**Decisión:** no instalar nada por ahora. La guía `local-ai/generar-video.md` queda como referencia, con la Ruta 2 (LTX Desktop + API) como recomendada para cuando se decida ejecutar.
**Motivo:** la máquina no corre LTX local (6 GB vs 15 GiB) y el objetivo todavía no está definido. Documentar primero evita gastar en una ruta que no se va a usar.
**Tope de gasto si se ejecuta:** $10/mes, con prueba inicial de $0,09.
**Alternativa descartada:** instalar ComfyUI ya. Mucho esfuerzo para calidad 480p.
**Revisar cuando:** haya objetivo concreto de publicación, o aparezca una GPU con ≥16 GB.
