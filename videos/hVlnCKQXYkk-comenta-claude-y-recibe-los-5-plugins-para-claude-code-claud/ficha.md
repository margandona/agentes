# Ficha de video

## Metadatos

- **Título:** Comenta "CLAUDE" y recibe los 5 plugins para Claude Code
- **Canal:** Salvatore Giuseppe | IA
- **URL:** https://www.youtube.com/shorts/hVlnCKQXYkk
- **Duración:** 1:10
- **Fecha:** 2026-10-19
- **Relevancia para el lab (1-5):** 4 — el tema (auditar el stack de un agente) sirve; la lista y las cifras, no.

## Tesis en una frase

> "No uses Claude Code sin estos cinco plugins: router de modelos, memoria, compresión de contexto, setup oficial y observador de tareas." [00:00]

## Veredicto del gate

| Pregunta | Sí/No | Evidencia |
|---|---|---|
| ¿Nombra una herramienta o técnica verificable? | Sí | Cinco nombres; todos existen salvo el ASR |
| ¿Hay una práctica repetible? | Sí, pero no la del video | Auditar el stack antes de sumar tools |
| ¿El resultado se puede comprobar? | Sí | Inventario, drift, decisiones aplicadas |
| ¿Se puede escribir sin depender del CTA? | Sí | La fuente es la documentación de cada tool, no "comenta CLAUDE" |

**Veredicto:** `skill-derivado` — el video da la práctica ("auditá y podá"), no el procedimiento.
**Por qué:** no hay pasos, y la mitad de la lista no son plugins.

## Nombres recuperados del ASR

| Token del transcript | Nombre real | Fuente que lo confirma |
|---|---|---|
| "Cloud Code" / "Cloud" | Claude Code | docs de Anthropic |
| "Cloud Mem" | Claude-Mem (`claude-mem`) | repo `thedotmack/claude-mem` |
| "Jet Room" | Headroom (`headroom-ai`) | docs del paquete y guías |
| "Cloud Setup" | Claude Code Setup (`claude-code-setup`) | `anthropics/claude-plugins-official` |
| "Task Observer" | Task Observer | `rebelytics/one-skill-to-rule-them-all` |
| "Yuks" | hooks | docs oficiales de hooks |
| "CLOD" | "CLAUDE" (palabra del CTA) | contexto de la frase |

## Qué enseña (3-6 bullets, con timestamp)

- [00:00] **OmniRoute**: gateway local que conecta Claude Code con "más de 200 proveedores" y cambia de modelo al llegar al límite. Afirma "hasta 1.600 millones de tokens gratis por mes".
- [00:00] **Claude Mem**: memoria entre sesiones; deja de repetir contexto de proyectos y archivos.
- [00:33] **Headroom**: se interpone entre el agente y el modelo, comprime y descarta lo que no importa. "Mismo resultado con muchísimos menos tokens".
- [00:33] **Claude Code Setup**: "el plugin oficial de Anthropic"; escanea el código y recomienda hooks, skills, subagentes y servidores MCP, y elimina ruido.
- [00:33] **Task Observer**: observa cómo trabajás, aprende tu estilo y "va mejorando tus Skills por sí solo de forma totalmente automática".
- [01:03] El video no explica ninguno: el paso a paso se entrega a cambio de comentar "CLAUDE". No hay procedimiento verificable en la pieza.

## Procedimiento que propone

1. Instalar los cinco antes de empezar a usar Claude Code [00:00].
2. Dejar que OmniRoute cambie de proveedor cuando se agota la cuota [00:00].
3. Dejar que la memoria y la compresión reduzcan el contexto repetido [00:00–00:33].
4. Correr el setup oficial para que recomiende automatizaciones y borre lo que sobra [00:33].
5. Activar Task Observer para que mejore las skills solo [00:33].

**No es un procedimiento**: es una lista de compras. No dice versión, orden, requisitos, costo, permisos ni cómo verificar que algo funcionó.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| OmniRoute | Gateway multi-proveedor con fallback al agotar cuota | Proveedores de OpenCode + Ollama local |
| Claude Mem | Memoria persistente entre sesiones | `AGENTS.md`, `docs/`, `videos/`, `preguntas` en cada sesión (memoria curada a mano) |
| Headroom | Comprimir tool output antes del modelo | `grep`/`read` con límites, salida truncada del shell |
| Claude Code Setup (`claude-code-setup`) | Auditar el proyecto y recomendar hooks/skills/MCP | **No tenemos**: auditoría manual del stack |
| Task Observer | Convertir correcciones repetidas en mejoras de skills | **No tenemos**: correcciones se pierden en el chat |
| Zep/CMEM (implícito) | Servicios que algunas de estas tools usan por detrás | — |

## Verificación de las afirmaciones (2026-10-27)

| Afirmación del video | Estado | Evidencia |
|---|---|---|
| "Cinco plugins" | **Falso** | Solo `claude-mem` y `claude-code-setup` son plugins. OmniRoute es gateway, Headroom es CLI/proxy, Task Observer es una skill. |
| "1.600 millones de tokens gratis al mes" | **Engañoso** | Es un techo teórico: suma de límites gratuitos de todo el catálogo usados sin parar. No es saldo ni garantía. |
| "Más de 200 proveedores" | **Aproximado** | El catálogo declara entre 290 y 350+ según la fuente; el número cambia. |
| "Plugin oficial de Anthropic" (Setup) | **Correcto** | `claude-code-setup` existe en `anthropics/claude-plugins-official`. Instalación: `/plugin install claude-code-setup@claude-plugins-official`. |
| "Task Observer te mejora las skills solo" | **Matizado** | Observa y **propone** cambios; el usuario aprueba. No escribe reglas sin revisión. |
| "Nunca más explicás nada" (memoria) | **Engañoso** | Requiere worker, base SQLite, embeddings y servicio; tiene planes pagos y proveedor alojado. No reemplaza documentación del proyecto. |

### Riesgos que el video omite

- **OmniRoute**: el proyecto pide definir `JWT_SECRET`, `API_KEY_SECRET` y `STORAGE_ENCRYPTION_KEY` antes de arrancar. El predecesor tuvo un secreto por defecto que permitía saltar el login y leer API keys; en 2026 un escáner marcó el paquete npm por scripts de instalación (parcheado después). Es un proyecto de un solo mantenedor que guarda tus claves.
- **Claude Mem**: captura actividad de herramientas y la manda a un proveedor; hay que revisar qué guarda y dónde. El repo además promociona un token (CMEM) ajeno.
- **Headroom**: no hace local al modelo; el contenido sigue viajando al proveedor. El ahorro real en trabajo de código es bastante menor que el 60–95 % de los logs.

## Ideas aprovechables para mí

- **Auditar el stack antes de sumar tools.** El valor real del video no son las cinco piezas: es la práctica de inventariar qué tiene el agente, qué está duplicado y qué no se usa. Hoy no tenemos ese paso.
- **Convertir correcciones en parches de skills.** Task Observer formaliza algo que hoy hacemos a mano y mal: cuando el usuario corrige dos veces lo mismo, debería salir un cambio en `SKILL.md`.
- **Distinguir plugin / gateway / skill / servicio.** El video mezcla categorías; nuestro `docs/herramientas-y-skills.md` ya las separa (Nivel 1–5). Ese criterio es el que hay que aplicar al evaluar cualquier "top 5".
- **La memoria curada gana a la memoria automática** para este repo: `AGENTS.md` + fichas + decisiones son auditables; una memoria automática no.

## Humo / a verificar

- [x] ¿Los cinco son plugins? **No** (ver tabla).
- [x] ¿"1.600 millones" es saldo? **No**, es techo teórico.
- [x] ¿`claude-code-setup` es oficial? **Sí**, en el directorio de Anthropic.
- [ ] ¿OmniRoute sigue siendo seguro con secretos propios y última versión? Requiere revisar advisories y el paquete npm antes de instalar. **No instalar sin esa revisión.**
- [ ] ¿Claude Mem tiene plan gratuito suficiente y borrado real de datos? Ver docs de privacidad y precios antes de usarlo con proyectos reales.
- [ ] ¿Task Observer funciona en OpenCode o solo en Claude Code/Cowork? El video no lo dice; su instalación documentada es para Claude Code.
- [ ] ¿Cuánto ahorra Headroom en *este* repo? Solo se responde midiendo `headroom perf` en una tarea real con logs largos.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `agent-stack-audit` (propuesta) | Inventario + poda del stack (skills, MCP, permisos, espejos, memoria) con criterios de seguridad y costo |
| plan | ninguno | No hace falta instalar nada de la lista para capturar la práctica |
| nota | `docs/decisiones.md` | Dejar asentado por qué no adoptamos los cinco de golpe |

## Citas textuales

> "No uses Cloud Code sin antes instalarte estos cinco plugins." [00:00]

> "Te da un uso prácticamente ilimitado conectando Cloud Code a más de 200 proveedores de API para usar gratis." [00:00]

> "Se pone entre tú y el modelo y solamente deja pasar lo que realmente importa." [00:33]

> "El plugin oficial de Anthropic, que escanea toda tu base de código y te recomienda los mejores Yuks, Skills, subagentes y hasta servidores MCP." [00:33]

> "Observa cómo trabajas, aprende tu estilo y va mejorando tus Skills por sí solo de forma totalmente automática." [00:33]

> "Comenta CLOD aquí abajo y te mando el paso a paso completo." [01:03]
