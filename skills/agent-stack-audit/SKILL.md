---
name: agent-stack-audit
description: >
  Audit and prune the stack that powers an agent project: skills and their
  mirrors, MCP servers, tools, permissions, memory/docs and third-party
  dependencies. Finds drift, duplicates, orphans, security and context-cost
  problems, then proposes keep/merge/archive decisions with evidence.
  Use when the user asks "what do we actually have installed", "audit our
  skills", "why is the agent ignoring a skill", "clean up the stack", or
  before adopting a new plugin or tool.
  Triggers: "auditar el stack", "inventario de skills", "limpiar plugins",
  "por qué no carga la skill", "qué tenemos instalado", "stack audit".
---

# Auditoría del stack del agente

## Qué hace

Convierte "creo que tenemos X" en un inventario verificable: qué skills existen, cuáles están realmente cargadas, qué MCP y permisos hay, qué depende de servicios externos y qué se puede podar. Termina en decisiones priorizadas, no en una lista.

La práctica viene del Short de los "5 plugins", donde el valor no era instalar cinco cosas sino revisar qué necesita el proyecto y eliminar el ruido. Acá se aplica al stack completo, con evidencia.

## Cuándo usarlo

- Antes de adoptar un plugin, MCP o herramienta nueva.
- Cuando una skill "existe" pero el agente no la usa.
- Cuando el repo lleva meses sumando piezas y nadie sabe cuáles siguen vivas.
- Antes de una entrega o de abrir el repo a otra persona.
- Después de una sesión con muchas correcciones repetidas.

## Cuándo NO usarlo

- Para decidir si una app es clonable: eso es `app-replica-recon`.
- Para evaluar la calidad de una skill concreta: se lee su `SKILL.md` y se prueba.
- Para instalar y configurar herramientas: este skill audita y decide; la instalación es otro paso.
- Como reemplazo de un análisis de seguridad formal de dependencias.

## Reglas no negociables

1. **No borrar: archivar.** Todo cambio destructivo va por git (`git mv` a `_archivo/`), nunca `rm` directo.
2. **Sin evidencia no hay veredicto.** "No lo usamos" necesita prueba: sin referencias en índices, docs, scripts ni historial reciente.
3. **Medir antes de recomendar.** Contexto cargado, cantidad de skills, servicios con clave: números, no impresiones.
4. **Declarar qué sale de la máquina.** Para cada herramienta externa: datos que envía, a dónde y con qué licencia.
5. **No autoaplicar cambios de skills.** Se propone el parche; el usuario aprueba.

## Procedimiento

### 1. Inventario

Relevar, sin interpretar todavía:

| Capa | Qué mirar |
|---|---|
| Skills canónicas | `skills/*/SKILL.md` |
| Espejos | `.opencode/skills/`, `.agents/skills/`, `.claude/skills/` según el cliente |
| Config MCP | `opencode.jsonc`, `.mcp.json`, `.claude/settings.json` |
| Tools propias | `tools/` |
| Contratos | `templates/`, `AGENTS.md`, `CLAUDE.md` |
| Docs de referencia | `docs/`, índices |
| Dependencias | scripts, `package.json`, `pyproject.toml`, binarios en `tmp/` |

Comando base en PowerShell:

```powershell
Get-ChildItem skills -Directory | ForEach-Object {
  $f = Join-Path $_.FullName "SKILL.md"
  [pscustomobject]@{
    Carpeta = $_.Name
    Frontmatter = if (Test-Path $f) { (Select-String -Path $f -Pattern '^name:' | Select-Object -First 1).Line } else { "FALTA" }
    Bytes = if (Test-Path $f) { (Get-Item $f).Length } else { 0 }
  }
}
```

### 2. Drift de espejos

Comparar conjuntos, no cantidades:

```powershell
$canon = (Get-ChildItem skills -Directory).Name
$oc    = (Get-ChildItem .opencode/skills -Directory -ErrorAction SilentlyContinue).Name
$ag    = (Get-ChildItem .agents/skills  -Directory -ErrorAction SilentlyContinue).Name

"Faltan en .opencode: " + (Compare-Object $canon $oc | Where-Object SideIndicator -eq '<=' | ForEach-Object InputObject)
"Sobran en .opencode: " + (Compare-Object $canon $oc | Where-Object SideIndicator -eq '=>' | ForEach-Object InputObject)
"Faltan en .agents:   " + (Compare-Object $canon $ag | Where-Object SideIndicator -eq '<=' | ForEach-Object InputObject)
```

Además: el `name` del frontmatter debe coincidir con la carpeta y ser `[a-z0-9-]`. Un desajuste hace que el cliente no la encuentre aunque el archivo exista.

### 3. Solapamiento y duplicados

- Agrupar por verbo de la `description` ("convierte", "audita", "analiza").
- Dos skills que se activan con los mismos triggers compiten: una gana o se fusionan.
- Revisar tambores duplicados: misma herramienta documentada en dos docs con versiones distintas.

### 4. Huérfanos y links rotos

- Skill en disco que no figura en `skills/INDEX.md`.
- Fila del índice que apunta a una carpeta inexistente.
- Doc que menciona una herramienta ya retirada (por ejemplo, un servicio que ya no está en uso).
- Plan en estado "en curso" sin fecha de actualización.

### 5. Riesgo de terceros

Para cada plugin, MCP, skill externa o binario:

| Pregunta | Por qué |
|---|---|
| ¿Quién lo mantiene? ¿Cuántos mantenedores? | Un proyecto de una persona que guarda claves es un riesgo distinto |
| ¿Licencia? | AGPL en un servicio de red obliga a liberar código; "no comercial" bloquea productos |
| ¿Qué secretos pide? | Claves propias, JWT, tokens de terceros |
| ¿Tiene secretos por defecto? | Un default conocido es una puerta abierta |
| ¿Qué datos salen y a dónde? | Memoria, prompts, logs, archivos |
| ¿Scripts de instalación? | Revisar `postinstall`, `preinstall`, `curl \| bash` |
| ¿Advisories o incidentes previos? | Historial del proyecto y del paquete npm/PyPI |
| ¿Cómo se desinstala? | Si no hay rollback, no entra |

Si alguna respuesta es "no se sabe", la herramienta no se adopta todavía.

### 6. Costo de contexto y de dinero

- Contar skills cargadas y sumar el largo de las `description`: se inyectan en cada sesión.
- Listar servicios con API key y su facturación (por request, por token, por mes).
- Marcar tools que duplican algo nativo (por ejemplo, un compresor de contexto cuando el agente ya trunca salidas).
- Medir, no estimar de memoria: si hay comando de diagnóstico (`doctor`, `perf`, `status`), correrlo.

### 7. Decisiones

Tabla final, una fila por pieza:

| Pieza | Veredicto | Evidencia | Acción | Prioridad |
|---|---|---|---|---|
| `ejemplo` | mantener / fusionar / archivar / adoptar / rechazar | link o comando | quién y qué archivo | P0/P1/P2 |

Cada acción con rollback: ruta de archivo, comando de git y cómo revertir.

### 8. Bucle corrección → parche

Si durante la auditoría aparecen correcciones repetidas del usuario ("siempre te olvidás de X"), no se arregla en el chat: se propone un diff al `SKILL.md` que corresponda.

```
observación: el usuario corrigió 2+ veces el mismo paso
skill afectada:
línea a cambiar:
diff propuesto:
cómo se verifica que quedó:
```

Se aplica solo con aprobación y se anota en `docs/decisiones.md`.

## Salida esperada

- `docs/stack-audit-YYYY-MM-DD.md` con inventario, drift, riesgos, costos y tabla de decisiones.
- Parches propuestos (no aplicados) para skills e índices.
- Resumen en el chat: qué está roto, qué sobra, qué falta y qué no se toca.

**Criterio de éxito:** cada veredicto se puede rastrear a un comando o a un archivo; después de aplicar los P0, el inventario y los espejos coinciden.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Contar carpetas en vez de comparar nombres | "tenemos 8" pero el cliente carga 5 | `Compare-Object` por conjunto |
| Confiar en el índice | índice dice 8, disco tiene 7 | Verificar ambos sentidos |
| Borrar lo que "no se usa" | se pierde trabajo previo | Archivar con git y documentar |
| Adoptar por popularidad | estrellas sin licencia ni mantenimiento | Checklist de terceros |
| Auditar sin medir contexto | se suman skills "chicas" que inflan cada sesión | Sumar descripciones y contar |
| Parchear skills en caliente | el agente cambia sus reglas sin revisión | Diff propuesto + aprobación |

## Origen

- Video: `videos/hVlnCKQXYkk-comenta-claude-y-recibe-los-5-plugins-para-claude-code-claud/` [00:00]–[00:33] — práctica de inventariar y podar antes de sumar.
- Hallazgo propio del 2026-10-27: `skills/` 8, `.opencode/skills/` 7, `.agents/skills/` 5; faltaban `agent-with-memory-and-tools` y `six-docs-before-build` en OpenCode, y además `media-metadata-sanitizer` en `.agents/`.
- Idea del bucle corrección → parche: Task Observer (`rebelytics/one-skill-to-rule-them-all`, CC BY 4.0), reformulada como revisión manual.
