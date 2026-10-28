# Draft pack — Prueba Tu Lanzamiento Con Clientes Falsos: MiroFish En Claude

> Generado por `tools/draft_pack.py` el 2026-10-27. No es una ficha ni un skill: es material para verificar y completar.

## Metadatos

- **ID:** -1t8wdk8O14
- **Título:** Prueba Tu Lanzamiento Con Clientes Falsos: MiroFish En Claude
- **Canal:** revolutia
- **Duración:** 44s (corta: usar ficha corta)
- **Publicado:** 20261023
- **URL:** https://www.youtube.com/watch?v=-1t8wdk8O14
- **Archivos:** `metadata.json`, `transcript.txt`

## Gate

- **Veredicto preliminar:** `revisar`
- **Señales:** `duracion_corta=True`, `cta=True`, `cifras=True`, `pasos=False`, `fuentes=False`, `nombres_raros=2`
- **Razones:**
  - CTA sin procedimiento
  - cifras sin fuente en el video
  - sin URL ni repo en el video: verificar por fuera
  - nombres en CamelCase: confirmar contra la fuente (el ASR puede deformarlos)
  - sin pasos reproducibles

## Gancho

> "Alguien acaba de liberar una forma de probar tu lanzamiento con miles de usuarios falsos y ya lleva 75.000 estrellas en GitHub." [00:00]

## Nombres a confirmar

| Detectado | Nombre real | Fuente que lo confirma |
|---|---|---|
| GitHub |  |  |
| MiroFish |  |  |
| Miro Fish |  |  |
| Prueba Tu |  |  |
| Lanzamiento Con |  |  |
| Clientes Falsos |  |  |
| En Claude |  |  |

Regla: dos candidatos por nombre y confirmación en repo, registro de paquetes o docs oficiales.

## Afirmaciones candidatas

| Hora | Texto | Tipo | Estado | Fuente |
|---|---|---|---|---|
| 00:00 | Alguien acaba de liberar una forma de probar tu lanzamiento con miles de usuarios falsos y ya lleva 75.000 estrellas en GitHub. | cifra | pendiente |  |
| 00:00 | Entonces Claude se pone a interpretar una multitud de clientes con edades, trabajos y presupuestos distintos. | cifra | pendiente |  |
| 00:31 | Y después puedes preguntarle a cualquiera de esos clientes por qué no te ha comprado. | cifra | pendiente |  |
| 00:31 | Menos mal que lo puedes probar dentro de Claude de manera gratuita. | integración | pendiente |  |

Tipos: `cifra`, `capacidad`, `precio`, `integración`, `licencia`, `procedimiento`.
Estados: `verificado`, `falso`, `engañoso`, `no verificable`, `pendiente`.

## Fuentes en la descripción

- ninguna

## Próximos pasos

- [ ] Confirmar cada nombre de la tabla contra la fuente primaria.
- [ ] Verificar cada afirmación y completar estado + fuente.
- [ ] Decidir el veredicto final del gate (`skill-directo`, `skill-derivado`, `solo-ficha`, `descartar`).
- [ ] Completar la ficha desde `templates/ficha-short.md` (≤180 s) o `templates/ficha-video.md`.
- [ ] Proponer en el chat y **esperar aprobación** antes de escribir `SKILL.md`.

## Propuesta (borrador, no enviar sin verificar)

```
veredicto: <completar>
skill: <nombre> — <una línea>
plan:  <nombre> — <una línea>
no:    <qué se descarta y por qué>
```
