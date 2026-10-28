---
name: synthetic-audience-test
description: >
  Rehearse a launch before launching: run a landing page, price or ad against
  6-12 synthetic personas, interview the ones who did not buy, and turn the
  output into ranked hypotheses plus a real interview script. Always labeled
  as simulation, never as demand evidence. Use before publishing a landing,
  changing price, or writing launch copy.
  Triggers: "probar el lanzamiento", "clientes falsos", "audiencia sintética",
  "cómo reaccionaría la gente", "testear el precio antes de lanzar",
  "synthetic audience", "pre-launch test".
---

# Ensayo de lanzamiento con audiencia sintética

## Qué hace

Pone tu landing, precio o anuncio frente a un grupo de personas simuladas con contexto distinto, y devuelve lo único que una simulación puede dar: **hipótesis y objeciones** para entrevistas reales. No predice conversión.

La idea viene del Short de MiroFish ("probá tu lanzamiento con clientes falsos"), pero acá se corre con subagentes aislados y se corrige el sesgo más grave de esos motores: si los agentes se ven entre sí, se copian.

## Cuándo usarlo

- Tenés el copy de una landing, un precio o un anuncio y todavía no lo publicaste.
- Querés descubrir objeciones antes de gastar en tráfico.
- Querés un guion de entrevistas con hipótesis concretas, no preguntas genéricas.
- Después de `app-gap-analysis`, para probar el ángulo de posicionamiento.

## Cuándo NO usarlo

- Como evidencia de demanda, TAM, conversión o ingresos. **No lo es.**
- Para precios regulados, salud, finanzas o cualquier afirmación legal.
- Cuando podés hablar con 5 usuarios reales esta semana: hablá con ellos.
- Para generar testimonios, reseñas o prueba social: es fabricación.
- Si no tenés el material real (copy, precio, público): sin eso, la simulación inventa el input y el output no sirve.

## Reglas no negociables

1. **Etiqueta visible.** Todo archivo generado empieza con `> SIMULACIÓN — no es evidencia de demanda.`
2. **Aislamiento en la primera ronda.** Cada persona ve solo el material y su ficha. Si ve a las demás, el resultado se contagia.
3. **Personas ancladas.** Edad, trabajo y presupuesto se apoyan en datos públicos o reseñas reales; no se inventan "para que quede variado".
4. **Nada de citas presentadas como reales.** Las respuestas son texto sintético; no van a la landing ni a anuncios.
5. **Cada hipótesis tiene una prueba de falsación.** Si no se puede refutar con una entrevista o un test, no es hipótesis: es opinión.
6. **Declarar la muestra.** Cuántas personas, cuántos modelos, cuántas rondas y qué se dejó afuera.

## Procedimiento

### 1. Fijar la decisión

Una sola decisión por corrida:

```
decisión: publicar esta landing / subir el precio de $X a $Y / usar este anuncio
material: <copy exacto, precio, captura o URL>
público: <a quién le habla>
```

Si hay dos decisiones, se corren dos veces.

### 2. Segmentar (6–12 personas)

Cubrir roles, no demographics decorativos:

| Rol | Para qué |
|---|---|
| Comprador ideal | ¿entiende la propuesta en 5 segundos? |
| Escéptico | ¿qué no le cierra? |
| No comprador por precio | ¿el precio lo saca o no entiende el valor? |
| Usuario de la alternativa | ¿con qué lo compara? |
| Mal encaje | ¿para quién NO es? (evita marketing genérico) |
| Adyacente | ¿ve un uso que no previste? |

`lanzamiento/personas.csv`:

```csv
id,rol,edad,trabajo,presupuesto_mensual,contexto,objecion_probable,fuente_de_anclaje
p01,comprador ideal,34,dueña de estudio contable,80 USD,"factura a 40 clientes, usa Excel","miedo a migrar datos","reseñas App Store 2026-08 / entrevista propia"
```

La columna `fuente_de_anclaje` es obligatoria. Si dice "inventado", la persona no entra.

### 3. Ronda 1 — aislada

Un subagente por persona (`subagent`), sin acceso a las otras respuestas. Prompt base:

```
Sos {id}. {ficha completa}.
No sos un asistente: sos esta persona evaluando algo que vio en su feed.
Material: {copy / precio / anuncio exacto}

Respondé:
1. Primer reacción en una frase (amor / indiferencia / rechazo).
2. ¿Qué creés que hace y para quién es?
3. ¿Qué precio le pondrías? ¿Por qué?
4. ¿Con qué lo comparás?
5. ¿Qué te frena? Sé específico.
6. ¿Pagarías? sí / no / no sé — y qué te falta para decidir.
7. Confianza en tu respuesta (baja/media/alta) y por qué.
```

Guardar `lanzamiento/ronda-1/<id>.md`. No editar las respuestas.

### 4. Ronda 2 — opcional, con prueba social

Mostrar a cada persona 2–3 reacciones agregadas (no todas) y volver a preguntar 1, 5 y 6. Medir el **delta**: cuánto cambió el "no" al ver que otros dicen "sí".

Ese delta es el dato más útil y el más peligroso: los LLM son más gregarios que los humanos, así que la ronda 2 **sobreestima** el entusiasmo. Anotarlo.

### 5. Entrevista de salida

Solo a quienes dijeron "no" o "no sé". Cinco preguntas, sin defender el producto:

1. ¿Qué te hizo decir que no?
2. ¿Qué tendría que ser verdad para que cambies de opinión?
3. ¿Qué solución usás hoy y qué te molesta de ella?
4. ¿A quién se lo recomendarías y a quién no?
5. ¿Qué palabra del copy te generó más desconfianza?

### 6. Síntesis

`lanzamiento/sintesis.md`:

- **Clusters**: objeción → cuántas personas → cita textual sintética → si se repite entre modelos.
- **Contradicciones**: dónde el mensaje se interpretó distinto de lo que quisiste decir.
- **Lo que la simulación no puede ver**: confianza, marca, logística, soporte, precio real, competencia.
- **Hipótesis** en `lanzamiento/hipotesis.md`, ordenadas por `impacto en la decisión × incertidumbre`:

```
H1: el precio se lee como "para equipos", no para independientes.
Evidencia simulada: 7/10 lo compararon con herramienta de equipo.
Prueba de falsación: 5 entrevistas reales; si 3+ lo ven individual, se cae.
Test barato: dos variantes de copy en la landing, 200 visitas cada una.
```

### 7. Convertir en validación real

`lanzamiento/guion-entrevistas.md` con 5 preguntas y el criterio de "qué respuesta confirma y qué respuesta refuta". Después: landing A/B, lista de espera o 5 llamadas. El output de la simulación es el input de eso, no el reemplazo.

### 8. Etiquetar y archivar

`lanzamiento/README.md` con: fecha, material evaluado, cantidad de personas, modelos usados, rondas, limitaciones y la etiqueta de simulación.

## Límites conocidos (declararlos siempre)

| Límite | Efecto |
|---|---|
| **Colapso de persona** | El modelo conserva sus sesgos; la diversidad es menor que la real |
| **Gregarismo** | Los agentes siguen la mayoría más que los humanos; subestiman el rechazo |
| **Complacencia** | Tienden a halagar al creador; hay que pedir explícitamente la objeción más dura |
| **Una sola familia de modelos** | Comparte sesgos; si se puede, correr con dos proveedores y comparar |
| **Muestra chica** | 8 personas no son 8.000; no hay intervalos de confianza |
| **Sin costo real** | Nadie pierde dinero al responder, así que el "sí" es barato |

## MiroFish: cuándo sí y cuándo no

**No instalar por defecto.** Es una app self-hosted (Node 18+, Python 3.11–3.12, `uv`), licencia AGPL-3.0, y requiere `LLM_API_KEY` + `ZEP_API_KEY`. El propio README recomienda menos de 40 rondas por costo. No es un plugin de Claude ni es gratis.

Considerarlo solo si **la dinámica social emergente es el objeto de estudio** (cascadas, polarización, difusión), no para probar un copy. Aun así, el output sigue siendo hipótesis.

## Salida esperada

```
lanzamiento/
  README.md            # etiqueta, muestra, modelos, límites
  personas.csv         # fichas con fuente_de_anclaje
  ronda-1/<id>.md      # respuestas aisladas
  ronda-2/delta.md     # opcional: efecto de la prueba social
  sintesis.md          # clusters, contradicciones, lo no simulable
  hipotesis.md         # H1..Hn con falsación y test barato
  guion-entrevistas.md # validación real
```

**Criterio de éxito:** cada hipótesis tiene una prueba de falsación y una pregunta de entrevista; ningún archivo afirma demanda ni conversión; la etiqueta de simulación está en todos.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Presentar la simulación como predicción | "el 70 % compraría" | Prohibido: hablar de hipótesis, no de tasas |
| Dejar que las personas se vean en la ronda 1 | todos opinan parecido | Aislar por subagente |
| Personas clonadas | 8 variantes del mismo comprador | Cubrir roles y anclar con evidencia |
| Preguntar "¿te gusta?" | respuestas complacientes | Preguntar "¿qué te frena?" y "¿qué te falta?" |
| Ignorar el delta de la ronda 2 | se lee como validación | Reportarlo como sesgo de gregarismo |
| Citas sintéticas en la landing | problema ético y legal | Nunca; solo investigación interna |
| Saltar a entrevistas reales | se decide con ficción | El guion es obligatorio |

## Origen

- Video: `videos/-1t8wdk8O14-prueba-tu-lanzamiento-con-clientes-falsos-mirofish-en-claude/` [00:00]–[00:31].
- Límites: README de `666ghj/MiroFish` (AGPL-3.0, requisitos y costo) y literatura sobre colapso de persona y gregarismo en OASIS/CAMEL-AI, consultada el 2026-10-27.
- Relacionado: `app-gap-analysis` (evidencia real de reseñas) y `six-docs-before-build` (documentar antes de construir).
