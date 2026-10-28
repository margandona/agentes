# Ficha de video

## Metadatos

- **Título:** Prueba Tu Lanzamiento Con Clientes Falsos: MiroFish En Claude
- **Canal:** revolutia
- **URL:** https://www.youtube.com/shorts/-1t8wdk8O14
- **Duración:** 0:44
- **Fecha:** 2026-10-23
- **Relevancia para el lab (1-5):** 3 — la idea (ensayo de lanzamiento con audiencia sintética) sirve; el "gratis dentro de Claude" es falso.

## Tesis en una frase

> "Probá tu lanzamiento con miles de usuarios falsos antes de lanzarlo: mirá quién lo ama, quién lo ignora y preguntale al que no compró por qué." [00:00]

## Veredicto del gate

| Pregunta | Sí/No | Evidencia |
|---|---|---|
| ¿Nombra una herramienta o técnica verificable? | Sí | MiroFish, repo público |
| ¿Hay una práctica repetible? | Sí | Ensayo de lanzamiento + entrevista al no comprador |
| ¿El resultado se puede comprobar? | Parcial | Reporte de simulación; no es predicción calibrada |
| ¿Se puede escribir sin depender del CTA? | Sí | El repo es público; la "bóveda" no hace falta |

**Veredicto:** `skill-derivado` — el método se diseña con subagentes; el video solo plantea el caso de uso.

## Nombres recuperados del ASR

| Token del transcript | Nombre real | Fuente que lo confirma |
|---|---|---|
| "Miro Fish" | MiroFish | repo `666ghj/MiroFish` |
| "Claude" | Claude | correcto en el transcript |

## Qué enseña (3-6 bullets, con timestamp)

- [00:00] MiroFish: engine de simulación multi-agente; "75.000 estrellas en GitHub". Le das página de producto, precio o anuncio y devuelve reacción anticipada.
- [00:00] Claude interpreta una multitud de clientes con edades, trabajos y presupuestos distintos.
- [00:00] Los agentes hablan entre ellos sobre el lanzamiento como en un feed de Instagram/Facebook; se ve quién lo ama, quién pasa de largo y por qué.
- [00:31] Se puede preguntar a cualquiera de esos clientes por qué no compró — la conversación que normalmente no tenés.
- [00:31] Cierre comercial: "dentro de Claude, gratis, link en la bóveda". [música]

## Procedimiento que propone

1. Preparar el material del lanzamiento: landing, precio o anuncio [00:00].
2. Cargarlo en MiroFish y pedir una predicción de reacción [00:00].
3. Dejar correr la simulación de personas que interactúan en un feed [00:00].
4. Leer el reporte: quién ama, quién ignora y por qué [00:00].
5. Entrevistar a los clientes que no compraron [00:31].

**Nivel de detalle:** nulo. No hay instalación, requisitos, costo, ni cómo se conecta con Claude.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| MiroFish (`666ghj/MiroFish`) | Simulación multi-agente de opinión pública | **No tenemos**; se puede emular con subagentes + personas |
| OASIS (CAMEL-AI) | Motor de simulación social (Twitter/Reddit) que usa MiroFish | — |
| Zep Cloud | Memoria temporal de cada agente | — |
| Claude | "Interpreta" a los clientes | OpenCode + subagentes |
| Qwen-plus / API OpenAI-compatible | LLM recomendado por el repo | DeepSeek/otros proveedores |

## Verificación de las afirmaciones (2026-10-27)

| Afirmación del video | Estado | Evidencia |
|---|---|---|
| "75.000 estrellas en GitHub" | **Correcto al momento de grabar** | El repo declara 82,4k estrellas el 2026-10-27; un artículo del 2026-09-30 registra ~75k. |
| "Se llama MiroFish" | **Correcto** | `github.com/666ghj/MiroFish`, AGPL-3.0, creado 2025-11-26. |
| "Dentro de Claude, gratis" | **Falso / engañoso** | No es plugin ni app de Claude. Es una app self-hosted: Node 18+, Python 3.11–3.12, `uv`, frontend :3000, backend :5001, Docker opcional. "Gratis" solo si ponés tus claves: `LLM_API_KEY` + `ZEP_API_KEY`. |
| "Miles de usuarios falsos" | **Matizado** | Miles de agentes son posibles, pero el propio README recomienda simulaciones de **menos de 40 rondas** por el consumo de tokens. |
| "Te enseña cómo va a reaccionar la gente de verdad" | **Exagerado** | Es exploración de escenarios, no predicción calibrada. Ver límites abajo. |
| "El enlace está en la bóveda / bio" | **No verificable** | CTA de captación; no hay enlace ni documento técnico en la pieza. |

### Límites que el video omite (y que importan)

- **Colapso de persona:** los LLM conservan sesgos propios aunque se les asigne una personalidad; la diversidad simulada es más angosta que la real (investigación citada en análisis de terceros sobre MiroFish/OASIS).
- **Gregarismo:** el paper de OASIS muestra que los agentes tienden a seguir la opinión mayoritaria más que los humanos. La simulación subestima el rechazo y la heterodoxia.
- **Ventana corta:** por defecto simula 72 h según la discusión del repo; no sirve para pronósticos de largo plazo.
- **Costo y dependencia:** Zep Cloud + proveedor de LLM + cómputo. Nada de eso es gratis por defecto.
- **Licencia AGPL-3.0:** si se integra en un producto o servicio de red, arrastra obligaciones de liberar el código. Decisión legal, no técnica.
- **Sesgo de confirmación:** el reporte lo escribe un agente dentro de la misma simulación. Auditar el mundo con sus propios registros no es evidencia independiente.

## Ideas aprovechables para mí

- **Ensayo de lanzamiento antes de publicar** es un paso que hoy no tenemos: `app-gap-analysis` usa reseñas reales (evidencia fuerte) pero llega después de que el producto existe.
- **La entrevista al que no compró** es la parte transferible y barata. Se puede hacer con 8–12 personas sintéticas bien definidas, sin instalar MiroFish.
- **Separar "explorar escenarios" de "predecir".** El output válido son hipótesis y preguntas para entrevistas reales, no un porcentaje de conversión.
- **No adoptar MiroFish para este lab (por ahora).** Requiere dos claves, dos runtimes y un motor de simulación para producir algo que se puede prototipar con subagentes en una sesión. Reevaluar solo si aparece un caso donde la dinámica social emergente sea el objeto de estudio.

## Humo / a verificar

- [x] ¿Es un plugin de Claude? **No**: app self-hosted.
- [x] ¿Es gratis? **No**: claves de LLM y Zep; cómputo propio.
- [x] ¿75k estrellas? **Sí**, coherente con la fecha.
- [ ] ¿Existe una integración oficial MCP/Claude de MiroFish? El README no la menciona. Verificar issues/discussions antes de afirmarlo.
- [ ] ¿Cuánto cuesta una simulación de 40 rondas con un caso real? Medir con claves propias antes de prometer nada.
- [ ] ¿La demo pública (`mirofish-live-demo`) permite probar sin claves? No verificado.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `synthetic-audience-test` (propuesta) | Ensayo de landing/precio/anuncio con personas sintéticas, etiquetado como hipótesis, con entrevistas al que no compra |
| plan | ninguno | No hace falta instalar MiroFish para capturar el método |
| nota | `docs/decisiones.md` | Registrar por qué no se adopta MiroFish y qué lo haría cambiar |

## Citas textuales

> "Alguien acaba de liberar una forma de probar tu lanzamiento con miles de usuarios falsos y ya lleva 75.000 estrellas en GitHub." [00:00]

> "Tú le das tu página de producto, tu precio o tu anuncio y le preguntas si a la gente lo va a amar o simplemente lo va a odiar y lo va a ignorar." [00:00]

> "Claude se pone a interpretar una multitud de clientes con edades, trabajos y presupuestos distintos." [00:00]

> "Y después puedes preguntarle a cualquiera de esos clientes por qué no te ha comprado." [00:31]

> "Menos mal que lo puedes probar dentro de Claude de manera gratuita." [00:31]
