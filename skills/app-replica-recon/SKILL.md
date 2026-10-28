---
name: app-replica-recon
description: >
  Reverse-engineer an app's behaviour into a build-ready recon map: screen
  inventory, user flows, components, inferred data model with evidence, and a
  must/should/could feature matrix. Clean-room only: public sources and the
  user's own account; never source code, assets or private APIs.
  Use when the user says "clone this app", "I want my own version of X",
  "map out how X works", "what screens does X have", "reverse engineer this
  app", or pastes an app URL/store listing before rebuilding it.
  Triggers: "clonar app", "replica de", "mapeá las pantallas", "cómo funciona X",
  "recon map", "app clone recon".
---

# Recon clean-room de una app

## Qué hace

Convierte una app en un mapa verificable que otro agente o developer puede reconstruir sin volver a abrir la original: inventario de pantallas, flujos, componentes, modelo de datos inferido y matriz de features. No copia código ni assets: estudia **qué hace** y **cómo se recorre**.

Es la fase 1 del pipeline `replica-app-mejorada` (plan en [`plans/replica-app-mejorada.md`](../../plans/replica-app-mejorada.md) de este repo; si copiás la skill sola a otro proyecto, el procedimiento no depende de él). El método está adaptado de `Jakeschincariol/replica-skill` (MIT), skill `replica-recon`; el video de origen solo publicita el pack y no enseña el procedimiento.

## Cuándo usarlo

- El usuario quiere una versión propia de una app existente (para venderla o para uso interno).
- Hay que estimar si una app es clonable y cuánto cuesta antes de comprometerse.
- Se necesita un contrato de alcance para que el build no improvise pantallas ni estados.
- Después de elegir el nicho y antes de escribir la primera línea de código.

## Cuándo NO usarlo

- **Ingeniería inversa de binarios**: decompilar un APK, un `.exe` o un `.dll` no es esta skill. Acá se mapea comportamiento observable, no se desensambla nada.
- Copiar el código, el contenido, el catálogo, los logos o el copy de la app.
- Entrar a la cuenta de otra persona, saltear un paywall o un login.
- Apps cuya propuesta sea puramente un catálogo licenciado o una red de usuarios: no es clonable aunque la UI lo sea.
- Cuando el usuario solo quiere una comparación de features para decidir, sin intención de construir.

## Reglas no negociables

1. **Clean-room.** Se reconstruye funcionalidad y patrones de UX. Nunca código fuente, bundles, APIs privadas, logos, tipografías propietarias, copy ni contenido.
2. **Fuentes permitidas:** páginas públicas y la cuenta propia del usuario. Nunca la cuenta de un tercero, nunca un paywall o login sorteado.
3. **Leer no es scrapear.** Navegación a velocidad humana, sin crawlers ni descargas masivas. Respetar los términos del sitio. Las APIs públicas y oficiales se usan dentro de sus términos.
4. **Capturas como referencia.** Viven en `replica/screens/`, sirven para comparar layout y nunca se publican ni se meten en el clon.
5. **Evidencia y confianza.** Cada dato inferido lleva su fuente y un nivel (`alta`, `media`, `baja`). Lo adivinado se marca como adivinado.
6. **Alcance honesto.** "Clonar cualquier app" significa features y flujos. No significa catálogos licenciados, datos propios, red de usuarios, integraciones de terceros ni hardware.
7. **Checkpoint legal.** Antes de un uso comercial: revisar términos del servicio, marca registrada y consultar abogado. Si los términos de la cuenta prohíben construir un competidor, trabajar solo con fuentes públicas y decirlo.

## Procedimiento

1. **Acotar.** Confirmar cuatro cosas (proponer respuestas y pedir un sí):
   - app y plataforma (web, iOS, Android, desktop);
   - **slice**: el loop por el que la gente paga, no "toda la app";
   - para quién es (uso interno/aprendizaje o producto a vender);
   - qué queda explícitamente afuera.

2. **Tabla de fuentes.** Una fila por fuente y una URL en cada fila. Orden de valor:
   | Fuente | Qué aporta |
   |---|---|
   | Centro de ayuda / docs | lista más completa de features y ajustes |
   | Página de precios | qué consideran valioso (lo que cobran aparte) |
   | Changelog | qué agregaron último y qué les importa |
   | Ficha en App Store / Play | capturas de pantallas clave y pitch |
   | Walkthroughs públicos | flujos reales, clic por clic |
   | Sitio de marketing | el loop contado en sus palabras |
   | Cuenta propia del usuario | estados reales, con el usuario presente |
   | Docs de API pública | modelo de datos casi gratis |

3. **Inventario de pantallas.** Una fila por pantalla, IDs estables `S01`, `S02`…:
   `ID | pantalla | ruta o cómo se llega | propósito | componentes clave | estados vistos`.
   Estados obligatorios: vacío, cargando, lleno, error, sin permiso, mobile. Un estado vacío no registrado es un estado que no se va a construir.

4. **Flujos.** `F01`, `F02`… Cada uno con objetivo, secuencia de pantallas y casos borde:
   ```
   F01 Invitado reserva una reunión
       S07 página de reserva -> S08 elegir horario -> S09 datos -> S10 confirmado
       borde: sin horarios esta semana, zona horaria distinta, turno tomado mientras completa
   ```
   Contar clics del camino feliz: ese número es el objetivo a superar.

5. **Componentes.** Cada pieza repetida: botón, input, date picker, modal, tabla, toast, navegación. Nombre, variantes, estados y en qué pantallas aparece.

6. **Modelo de datos inferido.** Entidades, campos, relaciones, **evidencia** y **confianza**:
   ```
   Reserva  id, event_type_id, inicio, fin, nombre, email,
            estado (confirmada | cancelada | reprogramada)
            evidencia: campos de S09, confirmación S10, artículo "Cancelar una reserva"
            confianza: alta
   ```
   No inventar campos que ninguna fuente muestre.

7. **Matriz de features.** Escribir `replica/features.csv`:
   ```csv
   feature,area,priority,original,clone,notes
   Reserva por link,agenda,must,yes,no,
   Recordatorio por SMS,notificaciones,should,no,no,pedido en reseñas
   ```
   `priority`: `must` / `should` / `could`. `clone` arranca en `no` y lo completa la fase de build. Las filas `skip` van con motivo.

8. **Lo que no se puede clonar.** Lista honesta de filas `skip` con razón: contenido licenciado, red de usuarios, datos que la app posee, acuerdos con partners, hardware, licencias reguladas (banca, salud).

9. **Dimensionar.** Pantallas, flujos, entidades y las partes difíciles (tiempo real, sync, pagos, calendario, email, offline). Tamaño: `S` (un fin de semana), `M` (semanas), `L` (un trimestre), `XL` (reacotar). Sin promesas de clon perfecto.

10. **Cerrar con resumen de cinco líneas:** loop central, cantidad de pantallas y flujos, tres partes más difíciles, qué queda afuera y próximo paso.

## Salida esperada

- `replica/recon.md` — alcance, fuentes, pantallas, flujos, componentes, modelo inferido, skips y tamaño.
- `replica/features.csv` — matriz con `must/should/could`, `original` y `clone`.
- `replica/screens/` — capturas de referencia (no se publican; agregar a `.gitignore`).
- Resumen de cinco líneas en el chat.

**Criterio de éxito:** otro developer puede construir el loop central leyendo `recon.md` sin reabrir la app, cada feature se rastrea a una fuente y cada exclusión tiene motivo escrito.

## Portabilidad

La skill no depende de `agent-lab`:

- Todo se escribe en `replica/`, relativo a la raíz del proyecto donde se corre.
- No requiere scripts, Python ni MCP: solo un agente con acceso a navegador/lectura y al usuario para la cuenta propia.
- Para llevarla a otro proyecto: copiar la carpeta `app-replica-recon/` a `.opencode/skills/`, `.claude/skills/` o `.agents/skills/` del proyecto destino, o instalarla global. El `SKILL.md` es autosuficiente.
- Si el proyecto ya tiene `docs/`, igual conviene `replica/` para separar el material de referencia del clon.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Clonar "toda la app" | plan de meses, nada terminado | Bajar a un slice: el loop que se paga |
| Saltear estados vacío/error | UI que se rompe en producción | Inventariar los seis estados en cada pantalla |
| Mezclar referencia y producto | capturas o copy del original en el clon | `replica/screens/` fuera del build; barrido antes de publicar |
| Inferir el modelo sin evidencia | tablas y campos inventados | Marcar confianza y volver a la fuente |
| Prometer paridad total | el usuario espera un clon exacto | Entregar tamaño `S/M/L/XL` y lista de `skip` |
| Scrapear o usar la cuenta de otro | bloqueo, problema legal | Leer a mano, solo fuentes públicas y cuenta propia |

## Origen

- Video: `videos/-PItFh9VLa4-clona-cualquier-app-con-claude-y-vendela-mejorada-replica-sk/` [00:00], [00:30].
- Método: adaptado de `Jakeschincariol/replica-skill` (MIT), `replica-recon/SKILL.md`; verificado el 2026-10-22. Atribución en el plan.
