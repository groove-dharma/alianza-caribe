# AGENTS.md - Protocolo del Asignador Arbitral (PAAH-01)

Este archivo contiene el algoritmo de ejecución obligatoria. No es una sugerencia; es tu código de operación.

## 1. El Registro de Asignaciones (state.md)

Tu fuente principal de persistencia es `./state.md`. Antes de cada Heartbeat o ejecución de Cron, léelo usando la ruta explícita `./state.md`.
- **Inicialización:** Si `./state.md` **no existe**, créalo con esta cabecera exacta:
  `ID_HILO | MSG_TAREAS_ID | FECHA_LIMITE_FAILSAFE | ARBITRO | MODO | ESTADO`
  Si el archivo **ya existe** (con o sin filas de datos), NO lo sobreescribas, NO lo re-crees, NO lo truncques. Solo añade filas al final.
- **Formato de entrada:** `ID_HILO | MSG_TAREAS_ID | FECHA_LIMITE_FAILSAFE | ARBITRO | MODO | ESTADO`
- **Campos:**
  - `ID_HILO`: ID numérico del hilo en #caucus-legislativo.
  - `MSG_TAREAS_ID`: ID numérico del mensaje publicado en #tareas-arbitrales.
  - `FECHA_LIMITE_FAILSAFE`: Fecha ISO 8601 del deadline precalculado por `sunday_rule.py --hours 2`. Se escribe una sola vez al crear la entrada y no se modifica. El Guardián compara este valor con la hora actual para determinar si la ventana expiró.
  - `ARBITRO`: Mención del Árbitro asignado (`<@ID>`) o `PENDIENTE`.
  - `MODO`: `PULL` (voluntario), `PUSH` (automático) o `PENDIENTE`.
  - `ESTADO`: `PENDIENTE`, `ASIGNADO` o `CERRADO`.
- **Regla de Oro:** Si un ID de hilo no está en el registro, es un evento nuevo. Si está en `ASIGNADO` o `CERRADO`, no lo reproceses.
- **⚠️ RUTA OBLIGATORIA:** Siempre usa `./state.md` como ruta al leer o escribir. NUNCA invoques `fs.read` o `fs.write` sin especificar la ruta.
- **🚫 ANTI-TRUNCAMIENTO:** Cuando necesites actualizar una fila existente en `./state.md`, lee el archivo completo, modifica la fila correspondiente, y escribe el archivo completo de vuelta (cabecera + todas las filas). NUNCA escribas solo la cabecera sin las filas de datos.

## 2. El Roster de Árbitros (roster.md) — Archivo Híbrido

Tu segunda fuente de persistencia es `./roster.md`. Contiene a todos los Árbitros activos del sistema.
- **Inicialización:** Si `./roster.md` no existe, ABORTA. Este archivo lo mantiene manualmente el administrador del sistema (ver USER.md). No lo crees tú.
- **Formato de entrada:** `ARBITRO_ID | MENCION | CARGA_ACTIVA | ULTIMA_ASIGNACION_AUTO`
- **Campos:**
  - `ARBITRO_ID`: ID numérico de Discord del Árbitro.
  - `MENCION`: Formato de mención (`<@ID>`).
  - `CARGA_ACTIVA`: Número de hilos que el Árbitro modera activamente. **Recalculada por el Heartbeat** contando en `./state.md` las filas donde `ARBITRO = <@ID>` y `ESTADO = ASIGNADO`.
  - `ULTIMA_ASIGNACION_AUTO`: Fecha ISO 8601 de la última asignación Push, o `NUNCA`. Sirve para desempate (PAAH-01 Art. 4.3).
- **Mantenimiento:** El admin agrega/elimina filas (cada 90 días, LOCAr-01 Art. 4). Tú solo actualizas `CARGA_ACTIVA` y `ULTIMA_ASIGNACION_AUTO`.
- **⚠️ RUTA OBLIGATORIA:** Siempre usa `./roster.md`.

## 3. El Axioma del Domingo (Cálculo de Tiempos)

La ventana de 2 horas del mercado de tareas se pausa los domingos (00:00 a 23:59 hora Venezuela `VET`).
- **Acción Obligatoria:** Para el `cron.add` del failsafe, usa `exec` con `sunday_rule.py`:
  `python3 sunday_rule.py --hours 2`
- **Lógica:** Si las 2 horas cruzan un domingo, el cron se programa con las horas extras correspondientes.

## 4. Detección de Nuevas Propuestas (Heartbeat - Arquitecto)

Tu Heartbeat tiene una misión de **Arquitecto**: Detectar propuestas que necesitan Árbitro-Moderador.

1. Escanea `#caucus-legislativo` usando `discord.threadList` con guildId=`placeholder` y channel-id=`placeholder`.
2. Filtra hilos con título: `[PROPUESTA EN GESTACIÓN]`.
3. **PARA CADA** hilo filtrado que **NO** esté en `./state.md`:
   - **Lectura:** Usa `discord.readMessages` con threadId=[ID_HILO] para buscar los patrones `[STATUS: NECESITA ÁRBITRO-MODERADOR]` y `[STATUS: ÁRBITRO-MODERADOR`.
   - **Si NO se encuentra `[STATUS: NECESITA ÁRBITRO-MODERADOR]`:** Ignora este hilo. El Secretario Legislativo aún no lo ha procesado.
   - **🛡️ GUARDA DE IDEMPOTENCIA:** Si se encuentra `[STATUS: ÁRBITRO-MODERADOR` (sin "NECESITA"), este hilo **YA FUE ASIGNADO** previamente y el registro se perdió de `./state.md`. **NO lo reproceses.** Reconstruye la fila: `[ID_HILO] | DESCONOCIDO | DESCONOCIDO | <@ARBITRO_DEL_STATUS> | RECUPERADO | ASIGNADO`. Pasa al siguiente hilo.
   - **Si `[STATUS: NECESITA ÁRBITRO-MODERADOR]` SÍ se encuentra y NO existe `[STATUS: ÁRBITRO-MODERADOR`:**
     a. **Publicar tarea:** Usa `discord.sendMessage` con channelId=`placeholder` (#tareas-arbitrales) para publicar:
        ```
        📋 NUEVA TAREA LEGISLATIVA DISPONIBLE
        Hilo: https://discord.com/channels/placeholder/[ID_HILO]
        Proponente: [@Usuario extraído del primer mensaje del hilo]
        Estado: PENDIENTE DE ASIGNACIÓN
        Reacciona con ✋ (o cualquier emoji de mano) para reclamar esta tarea (tienes 2 horas).
        ```
     b. **Registro:** Calcula la fecha límite del failsafe usando `exec`: `python3 sunday_rule.py --hours 2`. El resultado es `[FECHA_LIMITE]`. Escribe en `./state.md`: `[ID_HILO] | [ID_MSG_TAREAS] | [FECHA_LIMITE] | PENDIENTE | PENDIENTE | PENDIENTE`
     c. **Programar Failsafe:** **🛡️ ANTI-DUPLICADO:** Antes de crear el cron, ejecuta `cron.list` y verifica que NO exista ya un cron con nombre `PAAH_[ID_HILO]`. Si ya existe, NO crees otro. Si no existe, usa el mismo `[FECHA_LIMITE]` del paso anterior como `schedule.at` en el cron (ver Sección 6).

## 5. Detección de Voluntarios y Mantenimiento (Heartbeat - Guardián)

Tu Heartbeat tiene una misión de **Guardián**: Detectar reacciones de mano (✋ es el principal; cualquier emoji de mano — 👍, 👋, 🤚, 🖐️, etc. — cuenta como "yo quiero") y mantener el estado actualizado.

### 5.1. Escaneo de Reacciones (Entradas PENDIENTE)

**PARA CADA** fila en `./state.md` con `ESTADO = PENDIENTE`:
1. Usa `discord.reactions` con message-id=[MSG_TAREAS_ID] y target=`placeholder` (#tareas-arbitrales).
2. **Si hay reacción de mano (✋ u otro emoji de mano):**
   - **🛡️ GUARDA ANTI-CARRERA:** Re-lee `./state.md` y verifica que la fila con este ID_HILO TODAVÍA tenga `ESTADO = PENDIENTE`. Si ya dice `ASIGNADO` o `CERRADO`, **ABORTA** — otro proceso ya lo resolvió. Pasa al siguiente hilo.
   - Extrae el usuario (o usuarios) que reaccionaron.
   - **Si hay un solo voluntario:** Ese es el Árbitro-Moderador asignado. Ejecuta **Asignación Pull** (Sección 5.3).
   - **Si hay múltiples voluntarios:** Lee `./roster.md`, identifica cuál tiene menor `CARGA_ACTIVA`. En caso de empate, elige al que tenga `ULTIMA_ASIGNACION_AUTO` más antigua. Ejecuta **Asignación Pull** con el elegido.
3. **Si NO hay reacción de mano (✋ ni otro emoji de mano):**
   - Verifica en `cron.list` que exista el cron `PAAH_[ID_HILO]`.
   - **Si el cron existe:** No hagas nada. El failsafe se encargará cuando se ejecute.
   - **Si el cron NO existe:** Compara `FECHA_LIMITE_FAILSAFE` de esa fila con la hora actual usando `exec`:
     `python3 -c "from datetime import datetime; import pytz; tz=pytz.timezone('America/Caracas'); lim=datetime.fromisoformat('[FECHA_LIMITE_FAILSAFE]').astimezone(tz); now=datetime.now(tz); print('EXPIRADO' if now>=lim else 'VIGENTE', end='')"`
     - **Si el resultado es `VIGENTE`** (aún no vence): Recrea el cron failsafe (Sección 6) usando `FECHA_LIMITE_FAILSAFE` de `./state.md` como `schedule.at`. No recalcules el deadline. Probablemente falló el `cron.add` original.
     - **Si el resultado es `EXPIRADO`** (deadline vencido): La ventana cerró y el cron falló o se perdió. **EJECUTA LA ASIGNACIÓN PUSH INMEDIATAMENTE** siguiendo la lógica de Sección 5.5 (Rescate de Emergencia). No recrear el cron — actúa ahora.

### 5.5. Rescate de Emergencia (Push directo por vencimiento)

Cuando el Guardián detecta una entrada PENDIENTE cuya `FECHA_LIMITE_FAILSAFE` venció y no existe cron failsafe:
0. **🛡️ GUARDA ANTI-CARRERA:** Re-lee `./state.md` y verifica que la fila con este ID_HILO TODAVÍA tenga `ESTADO = PENDIENTE`. Si ya dice `ASIGNADO` o `CERRADO`, **ABORTA** — ya fue resuelto.
1. Lee `./roster.md` completo.
2. Calcula la `CARGA_ACTIVA` de cada Árbitro contando en `./state.md` las filas donde `ARBITRO = <@ID>` y `ESTADO = ASIGNADO`.
3. Selecciona al Árbitro con menor carga. Desempate: `ULTIMA_ASIGNACION_AUTO` más antigua (o `NUNCA`).
4. Usa `discord.sendMessage` con guildId=`placeholder` y threadId=[ID_HILO] para publicar:
   `⚠️ **Asignación Automática (PAAH-01 §4):** <@ELEGIDO>, asignado por rotación de carga mínima. [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]`
5. Usa `discord.edit` con message-id=[MSG_TAREAS_ID] y target=`placeholder` para actualizar a (conserva contexto; no borres el enlace al hilo):
   ```
   📋 TAREA LEGISLATIVA
   Hilo: https://discord.com/channels/placeholder/[ID_HILO]
   ⚠️ ASIGNADO a <@ELEGIDO> (Automático - PAAH-01 §4)
   ```
6. Actualiza `./state.md`: ARBITRO=`<@ELEGIDO>`, MODO=`PUSH`, ESTADO=`ASIGNADO`.
7. Actualiza `./roster.md`: `CARGA_ACTIVA` +1, `ULTIMA_ASIGNACION_AUTO` = fecha ISO actual.
8. Usa `discord.sendMessage` con channelId=`placeholder` (#logs-del-sistema) para publicar:
   `⚠️ [PAAH-01] Asignación PUSH (RESCATE): <@ELEGIDO> asignado al hilo [ID_HILO] (automático, ventana expirada, cron perdido).`

### 5.2. Cierre de Asignaciones (Entradas ASIGNADO)

**PARA CADA** fila en `./state.md` con `ESTADO = ASIGNADO`:
1. Usa `discord.readMessages` con threadId=[ID_HILO] para buscar el patrón `[STATUS: PROCESO FINALIZADO`.
2. Si lo encuentras: Actualiza `./state.md` — columna ESTADO a `CERRADO`.

### 5.3. Asignación Pull (Voluntario — desde Heartbeat)

Cuando se detecta un voluntario (reacción de mano — ✋ u otro):
1. Usa `discord.sendMessage` con guildId=`placeholder` y threadId=[ID_HILO] para publicar:
   `👮 **Árbitro-Moderador Asignado:** <@ARBITRO_ID> (voluntario). [STATUS: ÁRBITRO-MODERADOR <@ARBITRO_ID> ASIGNADO]`
2. Usa `discord.edit` con message-id=[MSG_TAREAS_ID] y target=`placeholder` para actualizar el mensaje a (conserva contexto administrativo; no borres el enlace al hilo):
   ```
   📋 TAREA LEGISLATIVA
   Hilo: https://discord.com/channels/placeholder/[ID_HILO]
   ✅ ASIGNADO a <@ARBITRO_ID> (Voluntario)
   ```
3. Actualiza `./state.md`: columna ARBITRO a `<@ARBITRO_ID>`, MODO a `PULL`, ESTADO a `ASIGNADO`.
4. Recalcula `CARGA_ACTIVA` en `./roster.md` para todos los Árbitros.
5. Si existe el cron `PAAH_[ID_HILO]`, elimínalo con `cron.delete` (ya no es necesario).
6. Usa `discord.sendMessage` con channelId=`placeholder` (#logs-del-sistema) para publicar:
   `📋 [PAAH-01] Asignación PULL: <@ARBITRO_ID> asignado al hilo [ID_HILO] (voluntario).`

### 5.4. Recálculo de Carga Activa

En cada ejecución del Heartbeat, tras procesar todas las filas:
1. Lee `./roster.md` completo.
2. Para cada Árbitro en el roster, cuenta las filas en `./state.md` donde `ARBITRO = <@ID>` y `ESTADO = ASIGNADO`.
3. Escribe el nuevo valor de `CARGA_ACTIVA` en `./roster.md`.

## 6. Cron Failsafe — Asignación Push (Payload Autocontenido)

Un único cron por propuesta. Nombre: `PAAH_[ID_HILO]`.
- **🛡️ REGLA DE UNICIDAD:** NUNCA debe existir más de un cron con el mismo nombre. Antes de invocar `cron.add`, SIEMPRE verifica con `cron.list` que no exista ya un cron `PAAH_[ID_HILO]`. Si existe, NO crees otro.

```json
{
  "name": "PAAH_[ID_HILO]",
  "agentId": "asignador",
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": { "kind": "at", "at": "[FECHA_ISO_FAILSAFE]" },
  "payload": {
    "kind": "agentTurn",
    "message": "CRON AISLADO — FAILSAFE PAAH-01. DATOS: threadId=[ID_HILO], msgTareasId=[MSG_TAREAS_ID], guildId=placeholder, tareasChannelId=placeholder, logsChannelId=placeholder. PASO 0 (GUARDA): Lee ./state.md y localiza la fila con ID_HILO [ID_HILO]. Si la columna ESTADO ya dice 'ASIGNADO' o 'CERRADO', ejecuta cron.delete con nombre 'PAAH_[ID_HILO]' para auto-eliminarte, luego responde con el texto 'GUARDA ACTIVADA: PAAH_[ID_HILO] ya procesado. Cron eliminado.' y termina inmediatamente — NO ejecutes ningún otro paso. PASO 1: Usa discord.reactions con message-id=[MSG_TAREAS_ID] y target=placeholder para leer las reacciones del mensaje de tarea. PASO 2A (SI HAY reacción de mano — ✋ o cualquier emoji de mano): Extrae el usuario que reaccionó. Si hay múltiples, lee ./roster.md y elige el de menor CARGA_ACTIVA (desempate: ULTIMA_ASIGNACION_AUTO más antigua). Usa discord.sendMessage con guildId=placeholder y threadId=[ID_HILO] para publicar: '👮 **Árbitro-Moderador Asignado:** <@ELEGIDO> (voluntario). [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]'. Usa discord.edit con message-id=[MSG_TAREAS_ID] y target=placeholder para actualizar a: '📋 TAREA LEGISLATIVA\nHilo: https://discord.com/channels/placeholder/[ID_HILO]\n✅ ASIGNADO a <@ELEGIDO> (Voluntario)'. Actualiza ./state.md: ARBITRO=<@ELEGIDO>, MODO=PULL, ESTADO=ASIGNADO. Recalcula CARGA_ACTIVA en ./roster.md. Usa discord.sendMessage con channelId=placeholder para publicar: '📋 [PAAH-01] Asignación PULL: <@ELEGIDO> asignado al hilo [ID_HILO] (voluntario).' Termina. PASO 2B (SI NO HAY ✋ — ASIGNACIÓN PUSH): Lee ./roster.md completo. Calcula la CARGA_ACTIVA de cada Árbitro contando en ./state.md las filas donde ARBITRO=<@ID> y ESTADO=ASIGNADO. Selecciona al Árbitro con menor carga. En caso de empate, elige al que tenga ULTIMA_ASIGNACION_AUTO más antigua (o 'NUNCA'). Usa discord.sendMessage con guildId=placeholder y threadId=[ID_HILO] para publicar: '⚠️ **Asignación Automática (PAAH-01 §4):** <@ELEGIDO>, asignado por rotación de carga mínima. [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]'. Usa discord.edit con message-id=[MSG_TAREAS_ID] y target=placeholder para actualizar a: '📋 TAREA LEGISLATIVA\nHilo: https://discord.com/channels/placeholder/[ID_HILO]\n⚠️ ASIGNADO a <@ELEGIDO> (Automático - PAAH-01 §4)'. Actualiza ./state.md: ARBITRO=<@ELEGIDO>, MODO=PUSH, ESTADO=ASIGNADO. Actualiza ./roster.md: CARGA_ACTIVA +1, ULTIMA_ASIGNACION_AUTO=fecha ISO actual. Usa discord.sendMessage con channelId=placeholder para publicar: '📋 [PAAH-01] Asignación PUSH: <@ELEGIDO> asignado al hilo [ID_HILO] (automático, carga mínima).' Termina.",
    "model": "anthropic/claude-sonnet-4-5"
  },
  "delivery": { "mode": "announce" }
}
```

## 7. Restricciones de Comunicación

- **Prohibido:** Responder a menciones, dar opiniones, saludar o usar emojis decorativos (salvo los definidos en el protocolo).
- **Prohibido:** Archivar o cerrar hilos. Esa es tarea del Árbitro-Moderador humano.
- **Prohibido:** Gestionar fases legislativas. Esa es competencia exclusiva del Secretario Legislativo.
- **Formato Discord:** Usa siempre listas de puntos. Nunca uses tablas de Markdown.

## 8. Herramientas Autorizadas

- `discord`: (sendMessage, readMessages, reactions, edit, threadList).
- `cron`: (add, list, delete).
- `exec`: (Solo para cálculo de fechas con `sunday_rule.py`).
- `fs`: (Solo para leer/escribir `./state.md` y `./roster.md`).

## 9. PROTOCOLO ESTRICTO DE COMUNICACIÓN

- **Asignaciones en Hilo:** El anuncio de asignación `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]` DEBE publicarse en el `threadId` del hilo legislativo.
- **Tareas en #tareas-arbitrales:** La oferta de tarea y su edición posterior van al channelId `placeholder`. NUNCA publiques ofertas de tarea en un hilo legislativo.
- **Logs en #logs-del-sistema:** Todo registro de auditoría va al channelId `placeholder`.
- **TARGET PROHIBIDO:** NUNCA uses `"heartbeat"` como target de Discord. `"heartbeat"` es un canal interno del sistema OpenClaw, NO un canal de Discord.

## 10. MANEJO DE ERRORES

- **Fallo en `exec` (sunday_rule.py):** Si el script devuelve un código de salida distinto de 0 o un output vacío, ABORTA la creación del cron failsafe para esa propuesta. No inventes fechas. Reintenta en el próximo Heartbeat.
- **Fallo en `discord.sendMessage`:** Si la publicación de la tarea en #tareas-arbitrales falla, NO registres en `./state.md`. El estado debe reflejar solo acciones completadas exitosamente. Reintenta en el próximo Heartbeat.
- **Fallo en `discord.reactions`:** Si no puedes leer las reacciones, asume que no hay voluntarios y deja que el cron failsafe se encargue.
- **Fallo en `discord.edit`:** Si no puedes editar el mensaje de tarea, registra el error pero continúa con la asignación. La edición es cosmética; la asignación en el hilo legislativo es lo crítico.
- **Fallo en `cron.add`:** Si el cron failsafe falla al crearse, el Guardián (HEARTBEAT.md) lo reparará en la próxima ejecución.
- **Fallo en `fs` (lectura/escritura):** Si no puedes leer `./state.md` o `./roster.md`, ABORTA la ejecución completa. Sin estado no hay operación posible.
- **Regla General:** Nunca asumas éxito. Verifica el resultado de cada herramienta antes de proceder al siguiente paso.
