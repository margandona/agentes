---
name: resume-optimization-prompts
description: >
  Optimize a resume/CV with four chained prompts: 6-second scan diagnosis,
  experience rewrite with Google XYZ formula, ATS compatibility score, and
  loss-aversion rewrite. Use when the user wants to improve a CV for a specific
  job posting, prepare for ATS filters, or tailor a resume. Triggers: "optimizar
  CV", "mejorar curriculum", "ATS", "resume", "CV", "postulacion", "entrevista".
---

# Resume optimization prompts

## Qué hace

Optimiza un CV con cuatro prompts encadenados en un mismo chat. Cada uno consume el resultado del anterior:

1. **Diagnóstico de 6 segundos**: simula un recruiter agotado y detecta dónde deja de leer y por qué.
2. **Reescritura de experiencia**: resultados primero, fórmula XYZ de Google, elimina lo genérico.
3. **Score ATS**: puntuación 0-100 y keywords exactas de rechazo.
4. **Perspectiva de la pérdida**: reescribe para que la empresa sienta que pierde algo si no contrata.

Origen: video `videos/s_xr--Zp5Fg-4-prompts-para-que-tu-cv-sobreviva-al-escaneo-de-6-segundos/` [00:05]-[00:45].

## Cuándo usarlo

- El usuario quiere mejorar su CV para una postulación específica.
- El CV no pasa filtros ATS.
- El usuario quiere saber por qué lo descartan.
- Quiere adaptar el CV a una oferta concreta.

## Cuándo NO usarlo

- El CV es para un contexto donde no hay ATS (contacto directo, referido).
- El usuario no tiene la descripción del puesto.
- El CV está en un idioma que el modelo no maneja bien (verificar).

## Procedimiento

### Precondición

Tener a mano:
- El CV actual (texto o PDF).
- La descripción del puesto al que se postula.

Todo se hace en **un mismo chat** para mantener el contexto.

### Paso 1 — Diagnóstico de 6 segundos

Subir el CV y la descripción del puesto. Ejecutar:

```
Actúa como el responsable de selección que ya lleva 300 currículums leídos hoy
y está agotado. Dale a mi currículum un escaneo de 6 segundos y dime con total
honestidad en qué momento exacto dejaste de leer y por qué.
```

**Salida esperada:** el punto exacto donde el recruiter deja de leer y la razón (título, primer bullet, formato, etc.).

### Paso 2 — Reescritura de experiencia

En el mismo chat:

```
Ahora reescribe mi sección de experiencia para que sobreviva a ese escaneo de
6 segundos. Cada línea tiene que empezar por un resultado, no por una
responsabilidad. Usa la fórmula XYZ de Google y quita todo lo que suene igual
que el resto.
```

**Fórmula XYZ de Google:** "Accomplished [X] as measured by [Y], by doing [Z]."

Ejemplo:
- Mal: "Responsable de gestionar el equipo de ventas."
- Bien: "Aumenté las ventas un 30% (X) en Q3 2025 (Y) implementando un CRM y
  capacitando al equipo (Z)."

**Salida esperada:** bullets reescritos con resultados medibles.

### Paso 3 — Score ATS

En el mismo chat:

```
Actúa como el filtro automático que descarta antes de que un humano llegue a
verlo. Dame una puntuación de compatibilidad sobre 100 y las palabras clave
exactas por las que me están rechazando.
```

**Salida esperada:** score 0-100 + lista de keywords faltantes.

### Paso 4 — Perspectiva de la pérdida

En el mismo chat:

```
Reescribe mi currículum desde la perspectiva de la pérdida para que la empresa
sienta que pierde algo si no me contrata.
```

**Salida esperada:** CV reescrito con framing de loss aversion (qué pierde la empresa si no te contrata).

## Salida esperada

- Diagnóstico del punto de fallo.
- Sección de experiencia reescrita con resultados (fórmula XYZ).
- Score ATS 0-100 con keywords de rechazo.
- CV reescrito desde la perspectiva de la pérdida.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Saltar el Prompt 1 | No se sabe por qué falla el CV | Siempre empezar por el diagnóstico |
| Usar chats separados | Se pierde el contexto acumulado | Todo en un mismo chat |
| Inflar resultados | El CV suena falso | Verificar que los números sean reales |
| No adaptar al puesto | Score ATS bajo | Incluir la descripción del puesto en el Prompt 1 |
| CV muy largo | El escaneo de 6 segundos no llega al final | Recortar a 1-2 páginas |

## Errores comunes del Prompt 2

- Bullets que empiezan con "Responsable de..." → cambiar por resultado.
- Resultados sin número → agregar métrica (%, tiempo, cantidad).
- Palabras genéricas ("liderazgo", "proactivo") → reemplazar por evidencia.

## Origen

- Video: `videos/s_xr--Zp5Fg-4-prompts-para-que-tu-cv-sobreviva-al-escaneo-de-6-segundos/` [00:05]-[00:45]
- Ficha: `videos/s_xr--Zp5Fg-.../ficha.md`
