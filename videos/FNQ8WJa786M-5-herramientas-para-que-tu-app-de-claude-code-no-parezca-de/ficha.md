# Ficha de video — 5 herramientas para que tu app de Claude Code no parezca de 2006

## Metadatos

- **Título:** 5 Herramientas Para Que Tu App De Claude Code No Parezca De 2006
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/FNQ8WJa786M
- **Duración:** 1:14
- **Fecha:** 2026-10-15
- **Relevancia para el lab (1-5):** 4 (tooling frontend para apps construidas por agentes)

## Tesis en una frase

> Las apps que hace todo el mundo con Claude Code se ven premium y la tuya se ve del 2006 porque te faltan cinco herramientas de diseño y verificación.

## Qué enseña

- [00:00] El problema: las apps de Claude Code parecen costar 10.000 euros o parecen del 2006.
- [00:05] **1. Taste Skill**: ayuda a Claude a desarrollar criterio estético real, para que entienda qué significa "premium".
- [00:15] **2. Guías de diseño web**: revisan lo que Claude ya construyó contra guías reales de diseño, en lugar de mirar la pantalla sin saber qué falla.
- [00:25] **3. Awesome Design**: le da al agente referencias y sistemas de diseño (tipografía, colores, espaciado, componentes, estructuras).
- [00:30] **4. Image to Code**: capturas un diseño que te gusta, se lo das a Claude y él lo recrea. Convierte Pinterest en herramienta de desarrollo.
- [00:40] **5. Playwright CLI**: Claude abre el navegador, interactúa con la web, hace capturas y comprueba lo que construyó. Construye, abre y mira.

## Procedimiento que propone

1. Instalar Taste Skill para criterio estético.
2. Usar guías de diseño web para auditar la UI ya construida.
3. Usar Awesome Design para referencias de tipografía, color, espaciado.
4. Usar Image to Code para recrear diseños desde capturas.
5. Usar Playwright CLI para que Claude verifique su propio trabajo en el navegador.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Taste Skill | Criterio estético para Claude | — |
| Guías de diseño web | Auditoría de UI contra estándares | revisión manual |
| Awesome Design | Referencias de sistemas de diseño | — |
| Image to Code | Captura → código | — |
| Playwright CLI | Verificación automatizada en navegador | webapp-testing (Playwright) |

## Ideas aprovechables para mí

- **Playwright CLI** es exactamente la skill `webapp-testing` que ya tengo en este lab. El patrón "Claude abre el navegador, interactúa, hace capturas y verifica" es reusable.
- **Image to Code** es útil para reproducir componentes de referencia: captura → código. Se puede aplicar a cualquier UI.
- **Guías de diseño web** (auditar lo construido) es un patrón de revisión que complementa `code-review`.
- La idea de que el agente **verifique su propio trabajo** (construye, abre, mira) es un loop de verificación que merece estar en `docs/metodologia.md`.

## Humo / a verificar

- [ ] **No se nombran los repositorios** de ninguna de las cinco herramientas. No se pueden instalar sin buscarlas.
- [ ] "Parecen costar 10.000 euros" — exageración de marketing.
- [ ] No se muestra un ejemplo real de ninguna herramienta en acción.
- [ ] El video cierra con "la bóveda": captación de tráfico.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `ui-review-with-playwright` | Verificar UIs construidas por agentes (construye, abre, mira) |
| nota | `local-ai/herramientas/frontend-tools.md` | Las 5 herramientas con links verificados |

## Citas textuales

> "Claude abre el navegador, interactúa con tu web, hace capturas y comprueba lo que ha construido. Lo construye, lo abre y lo mira." [01:01]
> 
> "Si veo otra vez un degradado morado con más de tres tarjetas redondeadas, eh, llamo a la policía." [00:05]
