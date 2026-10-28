# Ficha de video

## Metadatos

- **Título:** Clona Cualquier App Con Claude Y Véndela Mejorada: Replica Skill
- **Canal:** revolutia
- **URL:** https://www.youtube.com/watch?v=-PItFh9VLa4
- **Duración:** 46 s
- **Fecha:** 2026-10-20
- **Relevancia para el lab (1-5):** 4 — el video es publicidad, pero el pack que menciona es real, MIT y verificable; su método (recon clean-room + análisis de reseñas) sí es aprovechable.

## Tesis en una frase

> Clonar una app es solo el primer paso: el valor comercial está en reconstruir su funcionalidad y corregir en tu versión lo que los usuarios de la original odian.

## Qué enseña (3-6 bullets, con timestamp)

- [00:00] Existe un pack llamado Replica Skill, gratis, que según el video permite clonar cualquier aplicación con Claude.
- [00:00] No es una sola skill: son 11, con funciones separadas. Una hace ingeniería inversa de la app, otra la reconstruye y otra la testea buscando fallos, para que salga un clon funcional y no una maqueta.
- [00:30] La pieza que el video considera más valiosa es la "skill de emprendedor": investiga la app clonada, lee opiniones de usuarios y extrae funciones faltantes, problemas sin resolver y quejas; después aplica esas correcciones en la versión propia.
- [00:30] La propuesta de negocio: no terminás con una copia, terminás con una versión mejor que la original, que es lo que se puede vender.
- [00:38] Instalación: se pega el enlace dentro de Claude y se le pide que instale la skill. El enlace y la configuración están en la "bóveda" del canal (link en la bio).

## Procedimiento que propone

El video solo explicita el paso 1; el resto se infiere del pack verificado en GitHub:

1. Pegar el enlace del pack en Claude y pedir "install skill" [00:38].
2. Correr la skill de ingeniería inversa sobre la app objetivo [00:00].
3. Reconstruir la app con la skill de build [00:00].
4. Testear los flujos buscando fallos [00:00].
5. Leer reseñas reales y convertir quejas/faltantes en mejoras [00:30].
6. Vender la versión mejorada, no la copia [00:30].

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Claude (chat o Claude Code) | Ejecutar las 11 skills | OpenCode, con skills en `skills/` |
| Replica Skill (11 skills) | Recon, arquitectura, diseño, build, backend, test, diff, mejoras, marca, launch, deploy | No hay equivalente en el repo |
| "Bóveda" del canal | Enlace de descarga y configuración | Innecesaria: el repo público es `github.com/Jakeschincariol/replica-skill` (MIT) |

## Ideas aprovechables para mí

- **Recon map como contrato:** inventario de pantallas (S01…), flujos (F01…), componentes, modelo de datos inferido con evidencia/confianza y matriz `features.csv` (must/should/could). Es la parte que evita el clon-maqueta.
- **Clean-room explícito:** reconstruir funcionalidad y patrones de UX, nunca código, assets, logo, copy ni APIs privadas. Solo fuentes públicas y la cuenta propia del usuario.
- **Parity score:** comparar el clon contra el original con un número (features + diff de layout), no con una opinión.
- **Reviews con evidencia:** cada cita textual y con link; temas con menos de 3 reseñas o una sola fuente se marcan como "finos". Prohibido inventar reseñas o métricas.
- **Rebrand obligatorio antes de publicar:** barrido del código para que no quede nombre, dominio ni colores del original.
- **Honestidad de alcance:** el propio pack admite que "cualquier app" significa features y flujos, no catálogos licenciados, redes de usuarios ni datos propios.

## Humo / a verificar

- [ ] **"Clonar cualquier aplicación".** El repo lo desmiente en su letra chica: un motor de planillas o un catálogo musical licenciado no son clonables. Verificar caso por caso antes de prometer.
- [ ] **"Lo arregla todo dentro de tu versión".** El pack produce un plan de fixes priorizado; ejecutarlo depende de viabilidad y presupuesto. No es automático.
- [ ] **"No vuelvas a pagar una suscripción nunca más".** Clickbait: un clon no migra los datos, la red de usuarios ni las integraciones del servicio original, y puede violar sus términos.
- [ ] **Legalidad.** El repo pide chequeos de marca y abogado antes de vender. Falta definir acá qué uso permite el lab (¿solo aprendizaje/interno?).
- [ ] **Origen del enlace.** El video manda a una "bóveda" que no está en la descripción. El repo real se verificó el 2026-10-22: 4.6k estrellas, licencia MIT, autor Jake Schincariol.
- [ ] **Nombre "Replica Skill".** Confirmar que el pack sigue siendo MIT y que las 11 skills no cambiaron de alcance antes de vendorizar nada.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `app-replica-recon` | Convierte una app en mapa verificable (pantallas, flujos, datos, features) con límites legales |
| skill | `app-gap-analysis` | Convierte reseñas reales en fixes priorizados y ángulo de posicionamiento |
| plan | `replica-app-mejorada` | Orden de las 11 fases, herramientas y criterios de aceptación |

## Citas textuales

> "No es una skill, son 11, cada una con su función. Una hace ingeniería inversa de la app que quieres clonar, otra la reconstruye, otra la testea buscando fallos." [00:00]

> "Investiga la app que acabas de clonar, se lee las opiniones de sus usuarios y saca las funciones que faltan, los problemas sin resolver y las cosas que la gente odia de ella." [00:30]

> "No acabas con una copia, acabas con una versión mejor que la original, que es la que de verdad puedes vender." [00:30]
