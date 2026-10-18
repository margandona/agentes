# Generar video con IA — las 3 rutas, con valores

> Precios verificados el **2026-10-18** en las fuentes oficiales (al final). Cambian seguido: antes de pagar, revisá el link.

## Resumen

| | Ruta 1 — ComfyUI local | Ruta 2 — LTX Desktop + API | Ruta 3 — GPU alquilada |
|---|---|---|---|
| **Dónde corre** | Tu laptop (6 GB VRAM) | Nube de Lightricks | Servidor con GPU de 24 GB+ |
| **Calidad** | Baja-media (modelos 2B) | Alta (LTX 2.5) | Alta (LTX 2.5 local) |
| **Costo** | $0 + luz (~$0,03/h) | **$0,09-0,13 por segundo** de video | **$0,22-0,89 por hora** |
| **Clip de 5s** | $0, pero 5-15 min de espera | $0,15 a $0,65 | ~$0,03-0,07 de cómputo |
| **Esfuerzo** | Alto (instalar, modelos, nodos) | Bajo (instalar y usar) | Medio (pod, volumen, modelos) |
| **Ideal para** | Aprender, experimentar, no pagar | Publicar ya, volumen bajo | Volumen medio, control total |

**Regla corta:** si tu tiempo vale más que $5, andá a la Ruta 2. Si querés aprender y no pagar nada, Ruta 1. Si vas a generar seguido, Ruta 3.

---

## Tu punto de partida

| Ítem | Valor | Alcanza para |
|---|---|---|
| GPU | RTX 4050 Laptop, **6 GB VRAM** | Ruta 1 (justo) |
| RAM | 24 GB | Ruta 1 ✓ |
| Disco libre | ~469 GB | todas ✓ |
| LTX Desktop local | pide **15 GiB VRAM** | ✗ |

Los modelos grandes de video (LTX 2.5 son 22B) no entran en 6 GB. Los chicos (2B) sí, con paciencia.

---

## Ruta 1 — ComfyUI local (gratis)

### Qué obtenés

Clips de **3-5 segundos a 480-512p**, con movimiento aceptable y detalles flojos (manos, texto, caras de cerca). Sirve para b-roll, fondos, experimentos. No sirve para UGC realista ni para clientes exigentes.

### Qué necesitás

- ComfyUI portable para Windows (~1,5 GB).
- Un checkpoint chico:
  - **LTXV 0.9.5 2B** (~4-5 GB): texto/imagen → video, el más directo.
  - **Wan 2.1 1.3B** (~2,5 GB): alternativa, buena para animar fotos.
- Text encoder T5 (~5-9 GB según precisión) y VAE (~1 GB).
- Total en disco: **~15-20 GB**.

### Costo real

- Software: **$0**.
- Luz: la laptop consume ~150-200 W al mango. A ~$0,15/kWh son **~$0,03 por hora** de generación.
- Si un clip tarda 10 minutos, el costo energético es **menos de un centavo**.
- Lo que sí pagás: **tiempo**. 10 minutos de espera por 5 segundos de video.

### Pasos

1. Bajar **ComfyUI Windows Portable** desde los releases de GitHub y descomprimir en `C:\AI\ComfyUI` (fuera de OneDrive).
2. Abrir `run_nvidia_gpu.bat`. Si se queda sin VRAM, usar `run_nvidia_gpu_lowvram.bat`.
3. En la UI: **Workflow → Browse Templates → Video → LTX-Video** (o Wan 2.1). El template descarga los modelos que faltan.
4. Empezar con lo mínimo: **480p, 3-5 segundos, 24 fps, 20-30 pasos**.
5. Medir: anotar tiempo por clip y VRAM usada en `local-ai/benchmarks.md`.
6. Recién ahí subir resolución o duración.

### Cuánto tarda (estimado, a medir)

| Clip | En esta laptop | En una 4090 |
|---|---|---|
| 3s @ 480p | ~5-10 min | ~30-60 s |
| 5s @ 480p | ~8-15 min | ~1-2 min |
| 5s @ 720p | probablemente no entra | ~2-3 min |

### Cuándo sirve

- Querés aprender cómo funciona la generación por dentro.
- El video es un experimento, no una entrega.
- No querés darle una tarjeta a nadie.

### Cuándo NO

- Necesitás algo publicable esta semana.
- El video lleva personas hablando a cámara.
- No tolerás 10 minutos de espera por 5 segundos.

---

## Ruta 2 — LTX Desktop + API (pago por segundo)

### Cómo funciona

Instalás la app oficial (Windows/Mac). Como tu GPU no llega a 15 GiB, la app usa el **modo API**: la generación ocurre en los servidores de Lightricks y vos pagás por segundo de video producido. El **text encoding es gratis**; la generación no.

### Precios oficiales (por segundo de video)

| Modelo | 720p | 1080p | 1440p | 4K |
|---|---|---|---|---|
| **LTX 2.5 Fast** | $0,09 | $0,13 | $0,19 | $0,30 |
| **LTX 2.5 Pro** | $0,12 | $0,17 | $0,25 | $0,39 |
| **LTX 2.3 Fast** | $0,03 | $0,06 | $0,12 | $0,24 |
| **LTX 2.3 Pro** | $0,04 | $0,08 | $0,16 | $0,32 |

Extras:

| Función | Precio |
|---|---|
| Retake (rehacer un fragmento) 1080p | $0,10/s |
| Extend (alargar) 1080p | $0,10/s |
| Audio-to-video | igual que texto-a-video |
| Text encoding | **gratis** |

### Ejemplos de costo

| Lo que querés | Modelo | Costo |
|---|---|---|
| Clip de 5s para Reel, 720p | 2.5 Fast | **$0,45** |
| Clip de 5s, 1080p | 2.5 Fast | **$0,65** |
| Clip de 10s, 720p | 2.5 Fast | **$0,90** |
| Clip de 5s, 720p, barato | 2.3 Fast | **$0,15** |
| Rehacer 3s de un video 1080p | Retake 2.3 Pro | **$0,30** |
| **20 clips de 5s al mes, 720p** | 2.5 Fast | **~$9** |
| **20 clips de 5s al mes, 720p** | 2.3 Fast | **~$3** |

Para contenido semanal, 20 clips al mes es un número realista: **$3 a $9 por mes**, sin GPU nueva.

### Pasos

1. Bajar el instalador desde **github.com/Lightricks/LTX-Desktop/releases**.
2. Instalar y abrir. Aceptar el modo API cuando avise que el hardware local no alcanza.
3. Crear una API key gratis en **console.ltx.video** (el text encoding no se cobra).
4. Cargar la key en la app.
5. Generar un clip de prueba de 3s a 720p con 2.3 Fast (~$0,09) antes de ir por algo más caro.
6. Si te gusta, recién ahí usar 2.5 Fast/Pro.

### Cuándo sirve

- Querés calidad alta **hoy**.
- Hacés pocos clips por mes.
- No querés mantener infraestructura.

### Cuándo NO

- Necesitás cientos de clips: el costo por segundo se nota.
- No querés depender de una cuenta y una key.

---

## Ruta 3 — GPU alquilada por hora

### La idea

Alquilás una máquina con RTX 4090 (24 GB) o A40 (48 GB) por hora, corrés **LTX o ComfyUI ahí**, y apagás cuando terminás. Es "local" en el sentido de que el modelo corre en tu instancia, pero el hardware es de otro.

### Precios (Runpod, 8 de octubre de 2026)

| GPU | VRAM | Community | Secure |
|---|---|---|---|
| RTX 3090 | 24 GB | **$0,22/h** | $0,50/h |
| RTX 4090 | 24 GB | **$0,34/h** | $0,89/h |
| L4 | 24 GB | $0,44/h | $0,59/h |
| A40 | 48 GB | $0,35/h | $0,59/h |
| RTX A6000 | 48 GB | $0,33/h | $0,59/h |
| RTX 5090 | 32 GB | $0,69/h | $1,19/h |
| L40S | 48 GB | $0,79/h | $1,09/h |

Almacenamiento: **$0,07/GB/mes** (network storage) o $0,10/GB/mes (volumen).

Vast.ai suele tener precios parecidos o menores, con más variabilidad de calidad.

### La trampa de los 72 GB

LTX 2.5 necesita ~72 GB de pesos. Si bajás los modelos en cada sesión, perdés 1-2 horas de GPU solo descargando. La cuenta real:

| Concepto | Costo mensual |
|---|---|
| 72 GB de modelos en network storage | ~$5,04 |
| 8 horas de RTX 4090 Community | ~$2,72 |
| **Total** | **~$7,76/mes** |

Eso te da generación local ilimitada durante 8 horas. Si hacés 20 clips de 5s, es **~$0,39 por clip**, comparable a la Ruta 2 pero con más control y más fricción.

### Pasos

1. Crear cuenta en Runpod y cargar crédito (mínimo típico: $10).
2. Crear un **network volume** de ~100 GB en la región donde vas a desplegar.
3. Desplegar un pod con template **ComfyUI** (o una imagen con LTX ya instalado) y el volumen montado.
4. Conectar por el proxy HTTP del pod (te da una URL de ComfyUI en el navegador).
5. Instalar/descargar modelos **una sola vez**, al volumen.
6. Generar, descargar los videos, y **apagar el pod**. El storage sigue cobrando centavos; el GPU no.

### Cuándo sirve

- Vas a generar varias veces por semana.
- Querés LTX 2.5 completo sin comprar una GPU de $1.500+.
- Te bancás configurar un pod una vez.

### Cuándo NO

- Sos alérgico a la terminal y a las cuentas cloud.
- Necesitás algo en 10 minutos.
- Generás una vez cada dos meses (ahí Ruta 2 gana).

---

## Comparación por tipo de video

| Tipo | Mejor ruta | Costo por pieza | Nota |
|---|---|---|---|
| **Clips para redes (5-10s)** | Ruta 2 (2.3 Fast) o Ruta 3 | $0,15-0,45 | La más simple: LTX Desktop + API |
| **Animar una foto** | Ruta 2 (image-to-video) | $0,15-0,65 | Mismo precio que texto; la foto manda el encuadre |
| **Avatares / UGC hablando** | Ruta 3 + lipsync | ~$0,25-0,50 por clip | LTX no hace talking heads: necesitás lipsync aparte (ej. InfiniteTalk, $0,25 por request 720p en Runpod) |
| **Editar / rehacer un fragmento** | Ruta 2 (Retake) | $0,10/s | 3 segundos = $0,30; en local es gratis pero mucho más trabajo |
| **Extender un video** | Ruta 2 (Extend) | $0,10/s | Igual lógica que Retake |
| **Música → video** | Ruta 2 (audio-to-video) | igual que texto | Bueno para visuales de audio |

---

## Cómo decidir en 30 segundos

```
¿Necesitás el video esta semana?
├─ Sí → ¿Cuántos clips?
│        ├─ 1-30 al mes → Ruta 2 (API). $3-9/mes.
│        └─ 30+ al mes   → Ruta 3 (GPU alquilada).
└─ No → ¿Querés aprender y no pagar?
         ├─ Sí → Ruta 1 (ComfyUI local). Gratis, lento, calidad baja.
         └─ No → esperá a tener una GPU de 16 GB+.
```

---

## Mi recomendación concreta

1. **Hoy:** Ruta 2 con **2.3 Fast a 720p**. Un clip de prueba de 3s cuesta **$0,09**. Si el resultado te sirve, escalás a 2.5 Fast solo para el clip final.
2. **Este mes:** si generás más de 30 clips, pasá a **Ruta 3** con 3090/4090 y volumen de 100 GB (~$8/mes).
3. **Ruta 1:** solo si el objetivo es aprender. No la elijas para producir: en 6 GB vas a esperar 10 minutos por un clip de 480p que no se ve como el del video.

## Letra chica

- Los precios de LTX son **por segundo de video generado**, no por intento. Si no te gusta el resultado, pagaste igual.
- La app está en **beta**: puede cambiar la UI y romper workflows.
- Los pesos 2.5 están *gated* en Hugging Face: hay que aceptar la licencia.
- "Sin cuota" del video aplica solo si tenés 15 GiB de VRAM. Con 6 GB, esa promesa no se cumple.
- Las estimaciones de tiempo en local son eso: estimaciones. Se miden y se anotan.

## Fuentes

- Precios LTX API: https://docs.ltx.io/pricing (consultado 2026-10-18)
- Requisitos LTX Desktop: https://github.com/Lightricks/LTX-Desktop (consultado 2026-10-18)
- Precios GPU Runpod: https://www.runpod.io/pricing (actualizado 2026-10-08)
- Endpoints de video Runpod (Wan, Kling, InfiniteTalk): https://www.runpod.io/pricing#public-endpoints

## Pendientes

- [ ] Medir en esta laptop: LTXV 2B a 480p, tiempo real por clip
- [ ] Probar un clip de 3s con 2.3 Fast y comparar contra el Short de referencia
- [ ] Decidir si el objetivo es publicar o aprender (define la ruta)
