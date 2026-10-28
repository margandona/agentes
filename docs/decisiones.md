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

## 2026-10-18 — IA local en VS Code: 7B Q4_K_S + 3B + 1.5B

**Decisión:** usar Continue + Ollama en VS Code con tres modelos: `qwen2.5-coder:7b-instruct-q4_K_S` para chat/edición (calidad), `qwen2.5-coder:3b` para chat rápido y `qwen2.5-coder:1.5b` para autocompletado. Config en `local-ai/continue-config.yaml`.
**Motivo:** medido en `local-ai/benchmarks.md` — 22 / 81 / 142 tok/s respectivamente. Ningún 7B entra completo en 6 GB (16% de las capas caen a CPU); los ≤3B sí entran 100% en GPU.
**Alternativa descartada:** `qwen2.5-coder:14b` (9 GB, corre en RAM) y autocompletado con el 7B (~2,5 s por sugerencia).
**Costo:** 0. El único gasto es el disco (~11 GB de modelos).
**Revisar cuando:** se prueben las 5 tareas de calidad, o si el swap 7B ↔ 1.5B resulta molesto en el uso diario (en ese caso el 3B pasa a ser el default de chat).

## 2026-10-27 — No adoptar en bloque los "5 plugins" del Short hVlnCKQXYkk

**Decisión:** no instalar OmniRoute, Claude-Mem, Headroom, Claude Code Setup y Task Observer como pack. Se adopta la práctica de auditar el stack (`agent-stack-audit`) y cada herramienta se evalúa por separado cuando exista un problema medible.
**Motivo:** solo dos son plugins (Claude-Mem y Claude Code Setup); OmniRoute es gateway, Headroom es CLI/proxy y Task Observer es una skill. "1.600 millones de tokens gratis" es un techo teórico, no un saldo. OmniRoute pide secretos propios y su predecesor tuvo una vulnerabilidad crítica de autenticación. Claude-Mem captura actividad y tiene planes pagos. Headroom ahorra menos en código que en logs.
**Alternativa descartada:** instalar los cinco de golpe.
**Revisar cuando:** haya dolor concreto (cuota agotada, contexto saturado, correcciones repetidas) y la herramienta pase el checklist de terceros de `agent-stack-audit`.

## 2026-10-27 — MiroFish no se instala; se adopta el método

**Decisión:** no instalar MiroFish. El ensayo de lanzamiento se hace con `synthetic-audience-test` usando subagentes aislados.
**Motivo:** no es "gratis dentro de Claude": es una app self-hosted (Node 18+, Python 3.11–3.12, `uv`) que requiere `LLM_API_KEY` y `ZEP_API_KEY`, con licencia AGPL-3.0 y recomendación de <40 rondas por costo. Además, colapso de persona y gregarismo hacen que sobreestime el entusiasmo. Para probar un copy, 8–12 personas aisladas dan la misma señal sin dos runtimes ni dos claves.
**Alternativa descartada:** instalar MiroFish para testear landings.
**Revisar cuando:** la dinámica social emergente sea el objeto de estudio (cascadas, polarización, difusión) o se necesiten miles de agentes con memoria persistente.
