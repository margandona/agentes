# Agentes

Definiciones de agentes del lab. Un agente = prompt + modelo + tools + permisos + skills.

## Reglas

- Un archivo por agente: `agents/<nombre>.md` (o `.json`/`.yaml` si es config de OpenCode)
- Usar `templates/agente.md`
- Todo agente declara qué NO hace
- Si el agente vive en OpenCode, el archivo de config va en `.opencode/agent/<nombre>.md`
