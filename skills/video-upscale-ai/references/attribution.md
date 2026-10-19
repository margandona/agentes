# Procedencia y licencias

Esta es una adaptación local para Codex y OpenCode, no una publicación oficial de los autores siguientes. Se reescribe el pipeline Bash como Python/PowerShell y se añaden preset Shorts, mezcla conservadora, conservación de tiempos/color, logs, respaldos, previews, lotes y pruebas. No se ejecuta el instalador upstream que elimina instalaciones previas ni se adopta su mirror/proxy.

| Fuente inspeccionada | Versión | Licencia y uso en esta adaptación |
|---|---|---|
| [pangpang778/real-esrgan-skill](https://github.com/pangpang778/real-esrgan-skill) | `13e681c67743810cc3b7f9a717290f6d812e2aa1` | MIT; origen del flujo y de la skill. [Licencia íntegra](../LICENSE), copyright 2026 pangpang778. |
| [Gladgithub/esrgan-4k-upscale](https://github.com/Gladgithub/esrgan-4k-upscale) | `8be27e5283ab413e5ad5cfea25a6c98948bf0a21` | MIT; referencia para mezclar original Lanczos y salida IA. [Licencia íntegra](LICENSE-Gladgithub.txt), copyright 2026 Gladwin Mathew Prabhu Rajkumar. No se incorpora su grano automático ni modelo anime predeterminado. |
| [k4yt3x/video2x](https://github.com/k4yt3x/video2x) | `7db9c18d6278bbad9c3eda0e4e4ae210f9a688eb` | AGPL-3.0; alternativa evaluada. No se incorpora código ni se instala este framework. |
| [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | motor publicado en release v0.2.5.0, archivo 20220424 | Modelo/proyecto BSD-3-Clause, copyright 2021 Xintao Wang. [Aviso completo](LICENSE-Real-ESRGAN.txt). |
| [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) | ejecutable oficial 20220424 | MIT, con atribuciones de Xintao Wang y nihui; motor de inferencia externo. [Aviso completo](LICENSE-ncnn-vulkan.txt). |
| [Tencent/ncnn](https://github.com/Tencent/ncnn) | dependencia del paquete oficial | BSD-3-Clause y avisos de sus componentes. [Aviso completo de upstream](LICENSE-ncnn.txt). |

Los ejecutables y pesos permanecen en la caché ignorada por Git. Las licencias de cada componente son independientes de MIT de esta adaptación; consultar los avisos completos antes de redistribuir el paquete de runtime. FFmpeg y Pillow conservan sus licencias propias. El material audiovisual del usuario no se incluye en la distribución de la skill.
