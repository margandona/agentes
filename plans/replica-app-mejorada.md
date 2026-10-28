# Plan: replica-app-mejorada

- **Origen:** `videos/-PItFh9VLa4-clona-cualquier-app-con-claude-y-vendela-mejorada-replica-sk/` [00:00], [00:30]
- **Objetivo:** pipeline portable para reconstruir la funcionalidad de una app (clean-room) y convertirla en una versión mejor y vendible, con evidencia en cada fase.
- **No-objetivo:** copiar código, assets, logos, copy o catálogos; decompilar binarios; prometer un clon exacto; saltar paywalls o cuentas ajenas.
- **Riesgo principal:** legal — marca registrada, derechos de autor y términos del servicio de la app original. El riesgo técnico (clon incompleto) se controla con el parity score y el sizing honesto.
- **Estado:** borrador. Fases 1 y 8 implementadas como skills; el resto se ejecuta con skills existentes del lab o trabajo directo.

## Precondiciones

- [ ] App y plataforma elegidas, con un **slice** acotado (el loop que se paga).
- [ ] Uso definido por escrito: **aprendizaje/interno** o **producto a vender**. Cambia los chequeos legales, no el método.
- [ ] Acceso a la app con cuenta propia (si aplica) y disposición del usuario a navegar con el agente.
- [ ] Repo destino con carpeta `replica/` (se crea sola) y control de versiones.
- [ ] Decisión sobre stack; si es app nueva, correr antes `six-docs-before-build`.

## Contrato de artefactos

Todo el pipeline escribe en `replica/`, relativo a la raíz del proyecto destino:

| Archivo | Fase | Contenido |
|---|---|---|
| `replica/recon.md` | 1 | alcance, fuentes, pantallas, flujos, componentes, modelo inferido, skips, tamaño |
| `replica/features.csv` | 1 | matriz `must/should/could` con `original` y `clone` |
| `replica/screens/` | 1 | capturas de referencia (nunca se publican) |
| `replica/design/tokens.json` | 3 | color, tipografía, espaciado y componentes propios |
| `replica/reviews.csv` | 8 | reseñas crudas con link |
| `replica/feedback.md` | 8 | temas rankeados, citas, temas finos |
| `replica/fixes.md` | 8 | tres listas, plan de fixes y ángulos |
| `replica/launch/` | 10 | landing, precios y ficha de tienda |

## Pasos

1. **Recon clean-room** — skill [`app-replica-recon`](../skills/app-replica-recon/SKILL.md); archivos: `replica/recon.md`, `replica/features.csv`, `replica/screens/`.
   - Verificación: cada pantalla tiene estados; cada feature rastrea a una fuente; cada `skip` tiene motivo; tamaño declarado.
2. **Arquitectura y alcance técnico** — skill [`six-docs-before-build`](../skills/six-docs-before-build/SKILL.md); archivos: PRD, TRD, flujo, esquema de backend y plan dentro de `docs/` del proyecto destino.
   - Verificación: el PRD solo incluye features `must`/`should` del recon; el esquema cubre el modelo inferido con confianza alta; no hay requisitos sin origen.
3. **Sistema de diseño propio** — skill `frontend-design` (global) o trabajo directo; archivos: `replica/design/tokens.json` y componentes.
   - Verificación: paleta, tipografía e iconografía propias; contraste WCAG AA; nada copiado del original.
4. **Build pantalla por pantalla** — agente de coding sobre el recon; archivos: el proyecto destino.
   - Verificación: cada pantalla del recon existe con sus seis estados; `features.csv` pasa `clone` a `partial`/`yes`; el loop central funciona de punta a punta.
5. **Backend** — auth, base de datos, pagos e integraciones con claves propias del usuario; skills de Firebase si el stack lo usa.
   - Verificación: un usuario nuevo completa el loop central en un entorno limpio; reglas de acceso probadas; sin endpoints ni claves del original.
6. **Test de flujos** — skill `webapp-testing` (Playwright) o tests del stack; archivos: specs y `replica/test-plan.md`.
   - Verificación: cada flujo `F01…` tiene test de camino feliz y al menos un borde; no quedan bugs S1/S2 abiertos.
7. **Parity score** — cálculo desde `replica/features.csv` contra el recon.
   - Fórmula: `Σ(peso × avance) / Σ(peso)` sobre las features en alcance; `must=3`, `should=2`, `could=1`; `yes=1`, `partial=0.5`, `no=0`. Se excluyen `skip` y lo agregado propio.
   - Verificación: si falta un `must`, el clon **no es publicable**; el número queda escrito con la lista de faltantes.
8. **Brechas y posicionamiento** — skill [`app-gap-analysis`](../skills/app-gap-analysis/SKILL.md); archivos: `replica/reviews.csv`, `replica/feedback.md`, `replica/fixes.md`.
   - Verificación: 100+ reseñas de 3+ fuentes o muestra declarada; cada cita con link; temas finos marcados; 5–8 fixes con evidencia y costo; un ángulo recomendado.
9. **Marca propia** — nombre, paleta, logo, voz; barrido del código y de la ficha.
   - Verificación: `rg` sin coincidencias del nombre, dominio, colores ni identificadores del original (`OriginalAppEmbed` incluido); chequeo de marca y dominio pendiente anotado.
10. **Lanzamiento** — landing, precios contra la página pública del original y ficha de tienda.
    - Verificación: la landing usa el ángulo con evidencia; los límites de caracteres de la tienda se respetan; el nombre del original no aparece en la ficha.
11. **Deploy** — preflight (tests, parity, barrido, ficha), producción, DNS del dominio propio.
    - Verificación: deploy reproducido desde cero; `.env` fuera del repo; el preflight falla si el barrido no está limpio.

## Legal: los dos usos

| Uso | Qué se exige |
|---|---|
| **Aprendizaje / interno** | Fuentes públicas y cuenta propia; sin publicar el clon; sin copiar código, assets ni copy; respetar términos del servicio. |
| **Producto a vender** | Todo lo anterior + rebrand completo + chequeo de marca registrada y dominio + revisión de términos + abogado antes del launch. Sin el nombre ni el contenido del original en la app, anuncios ni ficha. |

En ambos casos: nada de reseñas falsas, ni propias ni contra la competencia. El pack original tampoco es asesoría legal y lo dice.

## Criterios de aceptación

- [ ] Existen los siete artefactos de `replica/` con el contenido mínimo de la tabla.
- [ ] El loop central se completa en un entorno limpio.
- [ ] Parity score ≥ 80 con todos los `must` en `yes`.
- [ ] Ningún `must` abierto; bugs S1/S2 cerrados.
- [ ] Barrido de marca limpio antes del deploy.
- [ ] Cada afirmación del análisis de reseñas tiene URL y el tamaño de muestra está escrito.
- [ ] El pipeline corre en un proyecto sin `agent-lab`: solo necesita las dos skills, el plan y un agente.

## Cómo saber si falló

- El recon tiene pantallas sin estados o features sin fuente → el build va a improvisar.
- Se descubre código, assets o copy del original en el repo → parar, borrar y volver a la regla clean-room.
- El parity score se calcula "a ojo" sin `features.csv` → no es un número, es una opinión.
- El análisis de reseñas no declara muestra o cita sin link → no es evidencia.
- Hay que decompilar o scrapear para avanzar → el alcance está mal elegido, no la herramienta.

## Portabilidad

Este plan está escrito para no depender de `agent-lab`:

1. Copiar `skills/app-replica-recon/`, `skills/app-gap-analysis/` y este plan al proyecto destino.
2. Instalar las skills en `.opencode/skills/`, `.claude/skills/` o `.agents/skills/` según el cliente; el `SKILL.md` es autosuficiente.
3. Crear `replica/` en la raíz del proyecto y agregar `replica/screens/` al `.gitignore`.
4. Las fases 2–7, 9–11 usan skills genéricas (`six-docs-before-build`, `frontend-design`, `webapp-testing`) o trabajo directo; no hay rutas absolutas ni scripts propios.
5. Si el proyecto no tiene las skills genéricas, las fases 2–7 y 9–11 se ejecutan igual: el contrato es `features.csv` y los documentos, no una herramienta.

## Rollback

- Todo el material de referencia vive en `replica/`, separado del producto: borrarlo no toca el código.
- Antes de cada fase destructiva (rebrand, migraciones, deploy) hay commit o rama.
- Si el chequeo legal falla, se detiene el plan; el trabajo de recon queda como documento, no como producto.

## Atribución

Método adaptado de [`Jakeschincariol/replica-skill`](https://github.com/Jakeschincariol/replica-skill), autor Jake Schincariol, licencia MIT. Se reescribieron los procedimientos en español y se adaptaron al flujo del lab; no se vendorizaron las 11 skills ni sus scripts. Verificado el 2026-10-22.
