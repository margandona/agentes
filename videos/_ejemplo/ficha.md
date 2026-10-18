# Ficha de video (ejemplo)

> Este folder es solo una muestra del formato. Se puede borrar.

## Metadatos

- **Título:** Cómo construí un agente de investigación
- **Canal:** Ejemplo
- **URL:** https://youtube.com/watch?v=XXXX
- **Duración:** 42:10
- **Fecha:** 2026-01-01
- **Relevancia para el lab (1-5):** 4

## Tesis en una frase

> Un agente útil no es el que tiene más tools, sino el que tiene un loop de verificación.

## Qué enseña

- [03:12] El loop mínimo: plan → actuar → verificar → corregir.
- [11:40] Las tools deben devolver errores accionables, no stack traces.
- [25:03] Memoria = archivos, no bases vectoriales, para proyectos chicos.

## Procedimiento que propone

1. Definir el criterio de éxito antes de escribir el prompt.
2. Darle 3 tools como máximo al arranque.
3. Loggear cada paso en un archivo.
4. Medir 10 corridas antes de cambiar el prompt.

## Herramientas mencionadas

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Ejemplo | logging | archivo JSONL |

## Ideas aprovechables para mí

- Aplicar el loop de verificación al pipeline de videos de este repo.

## Humo / a verificar

- [ ] ¿Realmente la memoria en archivos escala a 100 documentos? Probar con 50 fichas.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | agent-verification-loop | El loop es repetible |
| plan | memoria-en-archivos | Requiere cambios en el repo |

## Citas textuales

> "Si no podés describir cómo se ve el éxito, no tenés un agente, tenés una demo." [08:22]
