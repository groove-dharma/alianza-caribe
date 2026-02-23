# TOOLS.md - Notas Técnicas de Operación

Este archivo contiene las especificaciones exactas para el uso de herramientas por parte del Secretario Legislativo.

## 1. Regla del Domingo (Cálculo Procesal en Cadena)

Para la **Planificación Total (Big Bang)**, DEBES usar el script `sunday_rule.py` con tu herramienta `exec` en cadena para calcular T1, T2 y T3:

1.  **T1 (Fin Fase I):** Ejecuta `python3 sunday_rule.py --hours 24`. El resultado es T1.
2.  **T2 (Fin Fase II):** Ejecuta `python3 sunday_rule.py --hours 48 --start "T1"`. El resultado es T2.
3.  **T3 (Cierre):** Ejecuta `python3 sunday_rule.py --hours 24 --start "T2"`. El resultado es T3.

**Uso Crítico:** Inserta estos resultados exactos en el parámetro `schedule.at` de cada objeto `job`.

## 2. Acciones de Discord (Gobernanza)

Instrucciones específicas para la interacción con el servidor de Alianza Caribe:

- **Envío de mensajes en Hilo:** Utilizar `discord.sendMessage`
- **Lectura de mensajes en Hilo:** Utilizar `discord.readMessages` con el `threadId` como target.
  - **OBLIGATORIO:** Siempre especifica el target (threadId) al leer mensajes. Ejemplo: `discord.readMessages` con `threadId=[ID_HILO]`.
  - **🚫 PROHIBIDO:** Usar la herramienta `message` con `action: "read"`. Eso NO existe. Solo usa `discord.readMessages`.
- **Fase III (Votación):** Invoca `discord.poll`.
  - **Pregunta:** "¿Elevar propuesta al Cuerpo de Árbitros?"
  - **Opciones:** `👍 Elevar`, `👎 No elevar`.
  - **Duración:** `--poll-duration-hours [POLL_DURATION_HOURS]`. Este valor se calcula durante el Big Bang como la diferencia en horas reales entre T3 y T2. Discord cerrará el poll automáticamente al vencerse, sincronizándose con el Cron de Cierre.
- **Detección de Árbitro:** Usa `discord.readMessages` con `threadId=[ID_HILO]`.
  - **Patrón de búsqueda:** `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  - **Extracción:** Captura el ID o mención para el registro en `./state.md`.

## 3. Registro de Estado (state.md)

Estructura obligatoria para la persistencia de datos en el workspace:

- **Ruta:** `./state.md`
- **Formato:** Tabla delimitada por pipes (`|`).
- **Cabecera:** `ID_HILO | FASE | VENCIMIENTO_VET | ARBITRO_MODERADOR | ESTADO`

## 4. Cron Jobs (Transiciones - JSON SCHEMA)

Configuración MANDATORIA para los objetos `job` dentro de `cron.add`. NO USES FLAGS DE TERMINAL (`--`). Usa esta estructura de datos:

- **agentId:** `"legislativo"` (OBLIGATORIO — garantiza que el cron use el workspace correcto `/home/ubuntu/.openclaw/workspace-legislativo`)
- **sessionTarget:** `"isolated"`
- **wakeMode:** `"now"` (OBLIGATORIO)
- **delivery:** `{ "mode": "announce" }`
- **payload:**
  - **kind:** `"agentTurn"`
  - **model:** `"anthropic/claude-sonnet-4-5"`
  - **message:** Payload AUTOCONTENIDO. DEBE contener explícitamente:
    1. El **ID numérico del hilo** (`threadId`).
    2. El **ID numérico del GUILD** (`guildId`).
    3. El **ID numérico del canal padre `#caucus-legislativo`** (`channelId`).
    4. Pasos numerados (PASO 1, PASO 2...) con la secuencia exacta de herramientas a invocar, mensajes a publicar y actualizaciones a `state.md`.
    5. Un paso final explícito: "Termina. No hagas nada más."
  
**Prohibido:** Usar variables abstractas como "hilo actual" o referencias indirectas como "sigue AGENTS.md Punto X". El cron aislado nace ciego; su payload es su única instrucción operativa. Si no le pasas los IDs y los pasos completos en el `message`, fallará.

---

### Uso de discord.sendMessage
- Cuando respondas a una propuesta existente:
  `guildId`: [ID del Servidor]
  `channelId`: [ID del Hilo Específico]
  `threadId`: [ID del Hilo Específico]
- **Nota:** Nunca omitas el `threadId`. Las respuestas deben ser quirúrgicas dentro del contenedor de la propuesta.

### 🚫 Targets Prohibidos de Discord
- **NUNCA** uses `"heartbeat"` como target de `discord.sendMessage` o `discord.readMessages`. `"heartbeat"` es un canal interno del sistema, NO es un canal de Discord. Si intentas enviar un mensaje a `"heartbeat"`, obtendrás `Unknown target "heartbeat"`.
- Los únicos targets válidos son IDs numéricos de hilos (`threadId`) obtenidos de `./state.md` o del escaneo de `discord.threadList`.
- Si no tienes un ID numérico de hilo válido, **NO publiques nada**.

---
*Cualquier error en la ejecución de estas herramientas será registrado como una falla en el protocolo notarial.*