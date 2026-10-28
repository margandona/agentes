---
description: Video de YouTube → ficha verificada y, si pasa el gate, skill (protocolo del repo)
---

Video: $ARGUMENTS

Si `$ARGUMENTS` está vacío, pedí la URL y detenete.

Seguí este protocolo sin saltear pasos. No escribas fichas ni skills antes del paso 6.

1. **Paquete de borrador**

   ```powershell
   python tools/draft_pack.py "$ARGUMENTS"
   ```

   Si sale con código 2 (sin subtítulos), reintentá con `--langs "es,en"`. Si sigue fallando, reportá y detenete: no inventes la transcripción.

2. **Leer**

   Leé `videos/<slug>/draft.md`, `transcript.txt` y `metadata.json`.
   - Duración ≤180 s → `shorts-to-skill` + `templates/ficha-short.md`.
   - Duración >180 s → `video-a-skill` + `templates/ficha-video.md`.

3. **Verificar** (obligatorio)

   - Cada nombre de la tabla: dos candidatos y confirmación en repo, registro de paquetes o docs oficiales. El ASR no es fuente.
   - Cada afirmación: estado (`verificado`, `falso`, `engañoso`, `no verificable`, `pendiente`) y fuente.
   - Usá `websearch`/`webfetch`. Si no hay fuente, queda `pendiente` y va a *Humo / a verificar*.

4. **Ficha**

   Escribí `videos/<slug>/ficha.md` desde la plantilla que corresponda. Sin relleno: si una sección no aplica, "no aplica".

5. **Gate final**

   Veredicto: `skill-directo` / `skill-derivado` / `solo-ficha` / `descartar`. Un video = una idea como máximo.

6. **Propuesta y alto**

   Mostrá exactamente:

   ```
   veredicto: <...> — <una línea>
   skill: <nombre> — <una línea>
   plan:  <nombre> — <una línea>
   no:    <qué se descarta y por qué>
   ```

   **Detenete y esperá aprobación.** No escribas `SKILL.md` todavía.

7. **Solo si aprueba**

   - Skill → `skills/<nombre>/SKILL.md` desde `templates/SKILL.md`.
   - Plan → `plans/<nombre>.md` desde `templates/plan.md`.
   - Actualizá `videos/INDEX.md` y el índice que corresponda.
   - Espejá la skill en `.opencode/skills/` y `.agents/skills/`.

8. **Cierre**

   Verificá links relativos y faltantes entre espejos. Reportá en 3–5 líneas: veredicto, afirmaciones refutadas, artefactos creados y qué quedó pendiente.

Reglas: no inventar; CTA ≠ contenido; una lista no es un procedimiento; cifra sin fuente = `pendiente`; no instalar las herramientas mencionadas sin auditarlas primero.
