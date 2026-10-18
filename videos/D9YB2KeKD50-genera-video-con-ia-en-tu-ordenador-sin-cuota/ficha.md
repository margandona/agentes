# Ficha de video — LTX Desktop (video local sin cuota)

## Metadatos

- **Título:** Genera vídeo con IA en tu ordenador, sin cuota
- **Canal:** Lluís Jiménez IA | Creador UGC Tech
- **URL:** https://youtube.com/shorts/D9YB2KeKD50
- **Duración:** 1:03
- **Fecha:** 2026-10-17
- **Relevancia para el lab (1-5):** 3 (tema interesante, no aplicable al hardware actual)

## Tesis en una frase

> LTX Desktop permite generar y editar video con IA en la propia máquina, sin cuota mensual, si tenés una GPU NVIDIA de 15 GB o un Mac con 32 GB.

## Qué enseña

- [00:10] LTX Desktop es de Lightricks (el video dice "Lightrix") y es de código abierto.
- [00:17] El video se genera en tu máquina: no hay cuota mensual ni créditos.
- [00:20] Acepta texto, imagen o audio como entrada, y devuelve video.
- [00:26] Permite rehacer solo un fragmento ("retake") y montar todo en un editor con línea de tiempo.
- [00:33] Sin límite de uso: "lo usás las veces que quieras".
- [00:47] Requiere NVIDIA con 15 GB de VRAM o Mac Apple Silicon con 32 GB de RAM.

## Procedimiento que propone

1. Instalar LTX Desktop (aplicación de escritorio).
2. Escribir la escena, o dar una foto o un audio.
3. Generar el video localmente.
4. Rehacer los fragmentos que no gusten.
5. Montar en el editor con línea de tiempo.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| LTX Desktop (Lightricks) | Generación y edición de video local | ninguna (no hago video) |
| LTX 2.5 Fast / 2.3 Fast | Modelos locales | — |

## Ideas aprovechables para mí

- El patrón "generar → rehacer solo el fragmento malo → montar" es el mismo loop de verificación que quiero para agentes: no regenerar todo, corregir la parte fallada.
- Sirve como ejemplo de herramienta local con requisito de hardware explícito: el video lo dice, y el repo lo confirma.

## Humo / a verificar

- [x] **"Código abierto"** — Verificado: `Lightricks/LTX-Desktop`, licencia Apache-2.0, ~2.1k estrellas, estado **beta**. El código de la app es abierto; los pesos de los modelos se descargan aparte y tienen licencias propias.
- [x] **"15 GB de VRAM"** — Verificado en el README: Windows/Linux con CUDA y **≥15 GiB** de VRAM, o Apple Silicon con ≥32 GiB de RAM. Coincide con el video.
- [x] **"72 GB de disco"** — Verificado en el README: ~72 GB para el paquete base 2.5 Fast.
- [ ] **"No pagás nada"** — Matiz: la generación local es gratis, pero el *text encoding* por API es gratuito y el local requiere una descarga extra; la generación por API (2.5 Pro, Retake en la nube) es paga. El video no menciona estos matices.
- [ ] **Conflicto de interés** — El video cierra con `lalmarketing.com` [01:00], posible enlace de afiliado. No invalida el dato técnico, pero explica el tono.

## Veredicto para esta máquina

**No corre local.** La RTX 4050 Laptop tiene **6 GB de VRAM**; el mínimo son 15 GiB. La app se puede instalar, pero caería en modo API (nube, pago). No vale la pena para el lab hoy.

Detalle completo en `local-ai/herramientas/ltx-desktop.md`.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| nota | `local-ai/herramientas/ltx-desktop.md` | Evaluación de herramienta + veredicto de hardware |
| skill | — | No hay procedimiento repetible que valga la pena con 6 GB de VRAM |
| plan | — | Sin hardware compatible, un plan sería teatro |

## Citas textuales

> "Necesitas una gráfica Nvidia de 15 GB o un Mac con 32 de memoria." [00:47]
>
> "El vídeo se genera en tu máquina, sin cuota que pagar cada mes." [00:17]
