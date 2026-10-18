# LTX Desktop — evaluación

- **Qué es:** app de escritorio open source (Apache-2.0) para generar y editar video con modelos LTX, en local o vía API.
- **Origen:** video `videos/D9YB2KeKD50-genera-video-con-ia-en-tu-ordenador-sin-cuota/`
- **Repo:** https://github.com/Lightricks/LTX-Desktop
- **Estado:** beta (el README avisa de cambios incompatibles)
- **Fecha de evaluación:** 2026-10-18

## Requisitos (verificados en el README)

| Plataforma | Requisito | Modo |
|---|---|---|
| Windows/Linux + NVIDIA CUDA | **≥15 GiB de VRAM** | local |
| macOS Apple Silicon | **≥32 GiB de RAM** | local |
| Cualquier otra cosa | — | solo API (pago) |

- RAM: 16 GB mínimo, 32 GB recomendado.
- Disco: **~72 GB** para el paquete base 2.5 Fast (más si se agregan modelos de imagen, 2.3, etc.).
- Primer arranque: puede pedir login de Hugging Face para pesos con licencia gated.
- El *text encoding* se puede hacer por API (gratis) o con un encoder local (descarga extra).

## Veredicto para esta máquina

**No-go.**

| Ítem | Máquina | Requisito | |
|---|---|---|---|
| GPU | RTX 4050 Laptop, 6 GB | 15 GiB | ✗ |
| RAM | 24 GB | 16-32 GB | ✓ |
| Disco libre | ~469 GB | ~72 GB | ✓ |

La GPU es el cuello de botella. En modo API funcionaría, pero eso contradice el motivo del video (no pagar cuota).

## Alternativas si el objetivo es generar media local con 6 GB

Ninguna verificada todavía; candidatas a probar:

- **Imagen:** Stable Diffusion XL / Flux en cuantización agresiva — entra en 6 GB con offload, pero lento.
- **Video:** modelos chicos tipo Wan 1.3B o AnimateDiff con offload; calidad y duración muy por debajo de LTX.
- **Audio/voz:** Piper o Kokoro para TTS local; corre en CPU.

Regla del lab: no se instala nada sin antes medir si entra y a qué velocidad.

## Cuándo revisar de nuevo

- Si aparece una GPU con ≥16 GB de VRAM.
- Si LTX saca un modo local para 8 GB (poco probable: los pesos son 22B).
- Si el objetivo cambia a "video con IA" y se justifica pagar API por trabajo puntual.

## Notas

- El video dice "Lightrix"; el nombre correcto es **Lightricks**.
- El video promete "sin cuota" sin aclarar que el modo local exige hardware de gama alta y que varias funciones (2.5 Pro, Retake en la nube) son pagas.
- El proyecto es beta: no es una base estable para automatizar producción.
