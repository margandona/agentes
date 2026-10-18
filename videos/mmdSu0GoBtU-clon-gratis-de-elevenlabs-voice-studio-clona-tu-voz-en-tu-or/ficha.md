# Ficha de video — VoiceStudio (clonar la voz en local)

## Metadatos

- **Título:** Clon Gratis De ElevenLabs: Voice Studio Clona Tu Voz En Tu Ordenador
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/mmdSu0GoBtU
- **Duración:** 0:48
- **Fecha:** 2026-10-12
- **Relevancia para el lab (1-5):** 5 (corre en esta máquina y se conecta con agentes por MCP)

## Tesis en una frase

> VoiceStudio es una alternativa local y open source a ElevenLabs: clona tu voz con un clip corto, genera audio, transcribe, hace audiolibros y dobla videos, sin cuota y sin subir tu voz a la nube.

## Qué enseña

- [00:04] El proyecto supera las 36.000 estrellas en GitHub (dato del momento del video).
- [00:09] Reemplaza la cuota mensual de ElevenLabs: corre en tu propio ordenador.
- [00:13] Según el video, funciona incluso en un portátil viejo de 10 años.
- [00:18] Se llama **Voice Studio**: le das un clip corto hablando y lee cualquier texto con tu voz.
- [00:24] También convierte libros en audiolibros, dicta y transcribe grabaciones.
- [00:35] Dobla videos a **más de 600 idiomas**.
- [00:39] Al correr local, "tu voz no se sube a ningún sitio" y no hay facturas.

## Procedimiento que propone

1. Descargar e instalar Voice Studio.
2. Grabar un clip corto de referencia con tu voz.
3. Generar cualquier texto con esa voz.
4. Usar los extras: audiolibro, dictado, transcripción, doblaje.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| VoiceStudio | Clonación, TTS, doblaje, transcripción local | ninguna |
| OmniVoice (motor por defecto) | TTS multilingüe con clonación | — |

## Ideas aprovechables para mí

- Es la primera herramienta de la pista local que **sí corre** en esta laptop (CPU o GPU de 6 GB).
- Expone una **API local en el puerto 3900 y un servidor MCP**: un agente puede hablar, clonar y transcribir. Eso la vuelve parte de la pista de agentes, no solo de la de IA local.
- Permite cerrar el circuito video + voz: LTX genera imagen, VoiceStudio genera la locución.

## Humo / a verificar

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| "36.000 estrellas" | Cierto al momento, **desactualizado** | Hoy `debpalash/VoiceStudio` tiene **74.963** estrellas |
| "Versión gratuita de ElevenLabs" | Matiz | No es un fork: es una alternativa open source (**AGPL-3.0**). Gratis para uso local; los pesos de los modelos tienen licencias propias |
| "Portátil viejo de 10 años" | **Exagerado** | Corre en CPU, pero el propio proyecto avisa que es 10-50x más lento que en GPU. Un portátil de 2016 puede tardar minutos por párrafo |
| "Clip corto y lee cualquier cosa" | Cierto | Clonación zero-shot con clip de referencia + su transcripción |
| "600 idiomas" | Cierto | **646 idiomas** según el README y el motor OmniVoice |
| "Audiolibros, dictado, transcripción" | Cierto | Están en la app y en el MCP |
| "Tu voz no se sube a ningún sitio" | **Cierto con matices** | El flujo local no sube audio. La app tiene servicios remotos opcionales y telemetría con consentimiento. El doblaje puede traducir con NLLB local o con un proveedor LLM en la nube si lo configurás |
| "Gratis para siempre" | Matiz | La app es AGPL-3.0; uso comercial permitido bajo sus condiciones. Modelos y voces tienen términos aparte |
| Sin conflicto de interés | **No** | El video cierra con "la bóveda" y "el link del avío": es captación de tráfico, no una review neutral |

## Veredicto para esta máquina

**GO.** A diferencia de LTX Desktop, VoiceStudio está pensado para correr también sin GPU:

| Ítem | Máquina | Requisito | |
|---|---|---|---|
| OS | Windows 11 x64 | Windows 10/11 x64 | ✓ |
| GPU | RTX 4050 6 GB | opcional (CUDA acelera) | ✓ con límites |
| RAM | 24 GB | — | ✓ |
| Disco | ~469 GB libres | ~10 GB (5 GB en CPU) | ✓ |

Con 6 GB de VRAM la app **serializa** las generaciones (no paraleliza), pero funciona. Si el motor por defecto no entra, hay motores livianos para CPU (KittenTTS, Supertonic-3, PocketTTS).

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| nota | `local-ai/herramientas/voicestudio.md` | Evaluación completa + integración MCP |
| plan | `plans/instalar-voicestudio.md` | Instalación, clonación con consentimiento y prueba MCP (propuesto) |
| doc | `docs/consentimiento-voz.md` | Reglas de uso: consentimiento, divulgación, no suplantación (propuesto) |

## Citas textuales

> "Le das un clip corto tuyo hablando y a partir de ahí puede leerte cualquier cosa con tu voz." [00:18]

> "Como corre en tu ordenador, dejas de pagar facturas y tu voz no se sube a ningún sitio." [00:39]
