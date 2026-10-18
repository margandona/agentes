# Ficha de video — App a la Store, sin código

## Metadatos

- **Título:** App a la Store, sin código
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/IpnMvP6cKzE
- **Duración:** 0:56
- **Fecha:** 2026-07-24
- **Relevancia para el lab (1-5):** 3 (shipping: de idea a app publicada sin saber programar)

## Tesis en una frase

> Con Claude Code podés construir una app móvil completa y publicarla en la App Store sin saber programar, usando React Native + Expo y una skill para generar las capturas.

## Qué enseña

- [00:00] Se puede construir una app móvil completa con Claude Code y publicarla en la App Store sin saber programar.
- [00:05] Pedirle a Claude que instale **React Native** y **Expo** en la terminal. Es la forma más rápida de construir apps para iOS y Android con un solo código.
- [00:12] Construir primero la versión más básica (MVP) y luego añadir funcionalidades poco a poco. Cosas pequeñas que hagan que la gente vuelva (bucle de reactivación).
- [00:22] Testear en Chrome y escanear el código QR de Expo para comprobar que funcione en el móvil.
- [00:33] Pedirle a Claude que escriba el título, la descripción y los certificados.
- [00:38] Usar una skill de Claude para generar automáticamente las capturas de pantalla para la App Store.
- [00:43] Enviar a aprobación. Cuando Apple da luz verde, la app está disponible para descarga.

## Procedimiento que propone

1. Pedir a Claude que instale React Native + Expo.
2. Construir el MVP (versión más básica).
3. Añadir funcionalidades incrementales (bucle de reactivación).
4. Testear en Chrome y en el móvil vía QR de Expo.
5. Generar metadatos (título, descripción, certificados) con Claude.
6. Generar capturas de pantalla con una skill.
7. Enviar a revisión de Apple.
8. Publicar cuando se apruebe.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Claude Code | Programar la app | OpenCode |
| React Native + Expo | App para iOS y Android con un solo código | Flutter, nativo |
| Expo QR | Testear en móvil real | emulador |
| Skill de capturas | Generar screenshots para la store | manual |

## Ideas aprovechables para mí

- El patrón **MVP → funcionalidades incrementales → test → publicar** es un plan de implementación estándar que se puede aplicar a cualquier proyecto del lab.
- La separación "Claude escribe el código, una skill genera las capturas" es un ejemplo de agente con herramientas: cada pieza hace una cosa.
- Expo como forma de testear en móvil real sin compilar es un patrón de verificación rápida (construye, abre, mira).

## Humo / a verificar

- [ ] **"Sin saber programar"** — exageración. Expo, certificados y revisión de Apple requieren conocimiento técnico o asistencia.
- [ ] No se menciona el costo de la cuenta de Apple Developer ($99/año).
- [ ] No se mencionan los tiempos de revisión de Apple (días o semanas).
- [ ] No se muestra la calidad de la app resultante.
- [ ] El video cierra con "ve al link del avío": captación de tráfico.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| nota | `local-ai/herramientas/frontend-tools.md` | Actualizar con Expo/React Native |
| plan | — | El flujo MVP → publicar es genérico, no requiere plan nuevo |

## Citas textuales

> "Ahora puedes construir una app móvil completa con Claude Code y publicarla en la App Store sin saber programar." [00:00]

> "Construye la versión más básica de tu idea, el MVP, y a partir de ahí ve añadiendo funcionalidades poco a poco." [00:12]
