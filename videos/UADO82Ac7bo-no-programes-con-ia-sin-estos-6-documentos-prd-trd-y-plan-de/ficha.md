# Ficha de video — Los 6 documentos antes de programar con IA

## Metadatos

- **Título:** No Programes Con IA Sin Estos 6 Documentos: PRD, TRD Y Plan De Implementación
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/UADO82Ac7bo
- **Duración:** 1:14
- **Fecha:** 2026-10-13
- **Relevancia para el lab (1-5):** 5 (valida y refuerza la metodología del repo)

## Tesis en una frase

> El problema casi nunca es la IA, es la falta de contexto: si el agente tiene que adivinar, adivina mal. Con seis documentos deja de improvisar y empieza a construir. Primero los planos, después el código.

## Qué enseña

- [00:00] No construyas la app con IA hasta tener **seis documentos**.
- [00:00] **1. PRD** (requisitos de producto): todas las funcionalidades, qué estás construyendo exactamente y un resumen de la idea general.
- [00:10] **2. TRD** (requisitos técnicos): decisiones técnicas, stack de herramientas y APIs que vas a usar. Le da al agente un plano para decidir sin adivinar.
- [00:19] **3. Flujo de la app**: fases, navegación, recorrido del usuario y qué pasa cuando alguien pulsa un botón, incluida la pantalla siguiente.
- [00:31] **4. Brief de diseño**: aspecto y sensación (paleta, tipografía, componentes, estilo, cómo debe verse cada pantalla) para que no invente cualquier cosa.
- [00:40] **5. Esquema del backend**: cómo se guardan y organizan los datos del usuario, flujo de autenticación, cada tabla con columnas y relaciones.
- [00:50] **6. Plan de implementación**: la secuencia exacta de construcción paso a paso, para saber en qué orden montar las cosas.
- [01:03] Los seis se pueden crear con Claude en poco tiempo. Juntos hacen que el agente entienda la app de verdad.

## Procedimiento que propone

1. No escribir código hasta tener los seis documentos.
2. Redactar el PRD (funcionalidades + idea general).
3. Redactar el TRD (stack, herramientas, APIs).
4. Mapear el flujo de la app (pantallas, navegación, acciones).
5. Definir el brief de diseño (paleta, tipografía, componentes, estilo).
6. Diseñar el esquema del backend (tablas, columnas, relaciones, auth).
7. Escribir el plan de implementación (orden de construcción).
8. Recién entonces, programar.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Claude | Redactar los seis documentos | cualquier LLM local o en la nube |

## Ideas aprovechables para mí

- Los seis documentos son exactamente lo que este repo ya hace con `templates/`: ficha, plan, skill, agente. El video lo valida y le da un nombre.
- El TRD le da al agente un "plano para decidir sin adivinar": eso es lo que falta en `AGENTS.md` y en los planes. Conviene exigirlo antes de programar.
- La frase "primero los planos, después el código" puede ir en el README como regla.
- El esquema del backend (tablas, columnas, relaciones) es lo que `docs/` no tiene hoy: no hay un lugar para el modelo de datos de los proyectos del lab.

## Humo / a verificar

- [ ] "Los seis los puedes crear con Claude en un rato" — depende del tamaño del proyecto. En un lab chico sí; en una app real, el backend schema puede llevar horas.
- [ ] El video no dice qué tan detallado debe ser cada documento. Riesgo de pasarse o quedarse corto.
- [ ] No menciona revisión ni versionado de los documentos cuando el proyecto cambia.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `six-docs-before-build` | Checklist repetible antes de codear con un agente |
| template | `templates/spec.md` | Los 6 bloques en un solo documento de especificación |
| docs | `docs/decisiones.md` | Ya cubre decisiones; podría sumarse un modelo de datos por proyecto |

## Citas textuales

> "El problema casi nunca es la IA, es la falta de contexto. Si el agente tiene que adivinar, adivina mal." [00:00]

> "Con estos seis documentos deja de improvisar y empieza a construir. Primero los planos, después el código." [01:03]
