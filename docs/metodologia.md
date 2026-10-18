# Metodología: de un video a un agente

## El problema

Un video de YouTube sobre agentes dura 40 minutos, tiene 6 ideas buenas y 40 minutos de relleno. Copiar el proyecto del video produce agentes que funcionan en el video y en ningún otro lado.

## La solución: cuatro capas

```
VIDEO  →  FICHA  →  SKILL  →  PLAN  →  AGENTE
```

### 1. Video (crudo)
Se guarda la evidencia: `metadata.json` (título, canal, fecha, duración, descripción) y `transcript.txt`. Nada se interpreta todavía.

### 2. Ficha (interpretación)
Una página. Qué enseña, cuál es la tesis, qué pasos propone, qué herramientas usa, qué afirma sin probar, qué me sirve a mí.

Criterio de calidad: alguien que no vio el video puede decidir si le sirve leyendo la ficha.

### 3. Skill (procedimiento)
La parte **repetible** del video, convertida en instrucciones que un agente puede seguir. Un skill no explica teoría: dice qué hacer, en qué orden, con qué criterio de éxito.

Señales de que algo merece ser skill:
- Lo vas a hacer más de una vez.
- Tiene pasos estables.
- Se puede verificar el resultado.

### 4. Plan (implementación)
El "cómo" específico para este repo: archivos, dependencias, orden de commits, criterios de aceptación. Un plan se puede ejecutar en una sesión.

### 5. Agente (producto)
La combinación de un prompt + tools + permisos + skills. Recién acá aparece un agente nuevo, y solo si el plan lo justifica.

## Regla del 20%

Si de un video de 60 minutos salen más de 3 skills, estás transcribiendo, no sintetizando. Elegí.

## Anti-patrones

| Anti-patrón | Por qué duele |
|---|---|
| Skill que es un resumen del video | No es ejecutable |
| Plan sin criterio de aceptación | No se sabe cuándo terminó |
| Agente que hace todo | No se puede debuggear |
| Copiar el stack del video sin medir | Dependencias que no vas a usar |
| "Según el video, X es mejor" | Falta el benchmark propio |

## Checklist de cierre

- [ ] La ficha tiene timestamps
- [ ] El skill se puede seguir sin ver el video
- [ ] El plan tiene pasos numerados y verificables
- [ ] Hay un "cómo saber si falló"
