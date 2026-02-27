# TOOLS.md - Notas Técnicas de Operación

Este archivo contiene las especificaciones exactas para el uso de herramientas por parte del Asignador Arbitral.

## 1. Regla del Domingo (Cálculo del Failsafe)

Para calcular la fecha de vencimiento de la ventana de 2 horas del mercado de tareas, usa `sunday_rule.py`:

`python3 sunday_rule.py --hours 2`

**Uso Crítico:** Inserta el resultado exacto en el parámetro `schedule.at` del objeto `job` del cron failsafe.

## 2. Acciones de Discord

### 2.1. Lectura de reacciones (discord.reactions)
- **Propósito:** Detectar si un Árbitro reclamó una tarea con una reacción de mano en #tareas-arbitrales (✋ es el principal; cualquier emoji de mano — 👍, 👋, 🤚, 🖐️, etc. — cuenta como voluntario).
- **Parámetros obligatorios:**
  - `message-id`: ID numérico del mensaje de tarea (columna MSG_TAREAS_ID de `./state.md`).
  - `target`: `placeholder` (#tareas-arbitrales).
- **Parámetros opcionales:** `limit` (número de reacciones a devolver).
- **Salida:** Lista de reacciones con emoji y usuario(s) que reaccionaron.
- **Filtro:** Considera voluntario a quien reaccione con cualquier emoji que represente una mano (✋, 👍, 👋, 🤚, 🖐️, etc.). ✋ es el principal; el resto cuenta igual.

### 2.2. Edición de mensajes (discord.edit)
- **Propósito:** Actualizar el mensaje de tarea en #tareas-arbitrales tras la asignación (PAAH-01 Art. 3.3).
- **Parámetros obligatorios:**
  - `message-id`: ID numérico del mensaje de tarea.
  - `message`: Nuevo contenido del mensaje.
  - `target`: `placeholder` (#tareas-arbitrales).
- **Uso:** Tras asignar un Árbitro, editar el mensaje original al siguiente bloque completo (no reemplazar solo por una línea; conservar el enlace al hilo para contexto administrativo):
  - Pull: `📋 TAREA LEGISLATIVA` + nueva línea + `Hilo: https://discord.com/channels/placeholder/[ID_HILO]` + nueva línea + `✅ ASIGNADO a <@ID> (Voluntario)`
  - Push: mismo encabezado y Hilo, última línea: `⚠️ ASIGNADO a <@ID> (Automático - PAAH-01 §4)`
- **🚫 PROHIBIDO:** Usar `discord.edit` para editar mensajes en hilos legislativos. Los anuncios de asignación en hilos son mensajes nuevos, no ediciones.

### 2.3. Envío de mensajes (discord.sendMessage)
- **Destinos autorizados:**
  - Hilos legislativos: `threadId=[ID_HILO]` con `guildId=placeholder` — para anuncios de asignación `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  - #tareas-arbitrales: `channelId=placeholder` — para publicar nuevas ofertas de tarea.
  - #logs-del-sistema: `channelId=placeholder` — para registros de auditoría.
- **OBLIGATORIO:** Siempre especifica `guildId` al publicar en hilos.

### 2.4. Lectura de mensajes (discord.readMessages)
- **Uso 1:** Buscar `[STATUS: NECESITA ÁRBITRO-MODERADOR]` en hilos de #caucus-legislativo.
  - `threadId=[ID_HILO]`
- **Uso 2:** Buscar `[STATUS: PROCESO FINALIZADO` en hilos para detectar cierre.
  - `threadId=[ID_HILO]`
- **OBLIGATORIO:** Siempre especifica el target (threadId) al leer mensajes.
- **🚫 PROHIBIDO:** Usar la herramienta `message` con `action: "read"`. Eso NO existe. Solo usa `discord.readMessages`.

### 2.5. Listado de hilos (discord.threadList)
- **Uso:** Escanear #caucus-legislativo para detectar hilos con `[PROPUESTA EN GESTACIÓN]`.
- **Parámetros obligatorios:**
  - `guildId=placeholder`
  - `channel-id=placeholder` (#caucus-legislativo) — OBLIGATORIO para filtrar solo hilos de este canal.

## 3. Registro de Estado

### 3.1. state.md
- **Ruta:** `./state.md`
- **Formato:** Tabla delimitada por pipes (`|`).
- **Cabecera:** `ID_HILO | MSG_TAREAS_ID | FECHA_LIMITE_FAILSAFE | ARBITRO | MODO | ESTADO`
- **FECHA_LIMITE_FAILSAFE:** ISO 8601, deadline precalculado por `sunday_rule.py --hours 2`. Se escribe una sola vez al crear la entrada. El Guardián compara este valor con la hora actual para determinar si la ventana expiró.

### 3.2. roster.md
- **Ruta:** `./roster.md`
- **Formato:** Tabla delimitada por pipes (`|`).
- **Cabecera:** `ARBITRO_ID | MENCION | CARGA_ACTIVA | ULTIMA_ASIGNACION_AUTO`

## 4. Cron Jobs (Failsafe - JSON SCHEMA)

Configuración MANDATORIA para el objeto `job` dentro de `cron.add`. NO USES FLAGS DE TERMINAL (`--`). Usa esta estructura de datos:

- **agentId:** `"asignador"` (OBLIGATORIO — garantiza que el cron use el workspace correcto `/home/ubuntu/.openclaw/workspace-asignador`)
- **sessionTarget:** `"isolated"`
- **wakeMode:** `"now"` (OBLIGATORIO)
- **delivery:** `{ "mode": "announce" }`
- **payload:**
  - **kind:** `"agentTurn"`
  - **model:** `"anthropic/claude-sonnet-4-5"`
  - **message:** Payload AUTOCONTENIDO. DEBE contener explícitamente:
    1. El **ID numérico del hilo** (`threadId`).
    2. El **ID numérico del mensaje de tarea** (`msgTareasId`).
    3. El **ID numérico del GUILD** (`guildId`): `placeholder`.
    4. El **ID numérico de #tareas-arbitrales** (`tareasChannelId`): `placeholder`.
    5. El **ID numérico de #logs-del-sistema** (`logsChannelId`): `placeholder`.
    6. Pasos numerados (PASO 0, PASO 1, PASO 2A/2B...) con la secuencia exacta de herramientas a invocar y acciones a ejecutar.
    7. Un paso final explícito: "Termina. No hagas nada más."

**Prohibido:** Usar variables abstractas como "hilo actual" o referencias indirectas como "sigue AGENTS.md Sección X". El cron aislado nace ciego; su payload es su única instrucción operativa.

---

### 🚫 Targets Prohibidos de Discord
- **Regla absoluta:** El target DEBE ser siempre un **ID numérico** (channelId o threadId). Si la herramienta pide un target, usa solo números.
- **NUNCA** pongas la palabra `"heartbeat"` como target. No es un canal de Discord; es interno de OpenClaw. Usarlo produce `Unknown target "heartbeat"`.
- Los únicos targets válidos son:
  - IDs numéricos de hilos (`threadId`) obtenidos de `./state.md` o del escaneo de `discord.threadList`.
  - `placeholder` (#tareas-arbitrales).
  - `placeholder` (#logs-del-sistema).
- Si no tienes un ID numérico válido, **NO publiques nada**.

---
*Cualquier error en la ejecución de estas herramientas será registrado como una falla en el protocolo de asignación.*
