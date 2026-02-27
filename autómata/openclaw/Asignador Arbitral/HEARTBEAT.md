# HEARTBEAT.md

# 🛑 SYSTEM OVERRIDE: CEGUERA SELECTIVA
**INSTRUCCIÓN CRÍTICA:**
El sistema adjunta mensajes recientes automáticamente. **IGNÓRALOS**.
1. No leas el chat para entender el contexto.
2. Tu ÚNICA fuente de verdad es `./state.md` (ruta obligatoria), `./roster.md` (ruta obligatoria) y la lista de hilos activos de Discord.
3. Actúa como un **Procesador por Lotes**. No te detengas en el primer ítem; procésalos TODOS.

**⚠️ DISCORD — OBLIGATORIO:** Cuando uses la herramienta de envío/edición de mensajes a Discord, el parámetro `target` (o equivalente) DEBE ser SIEMPRE un **ID numérico** (channelId o threadId). NUNCA pongas la palabra `heartbeat` como target: no es un canal de Discord y la llamada fallará. Usa solo: `placeholder`, `placeholder`, o el threadId del hilo (columna ID_HILO de `./state.md`).

---

## 🔄 PROCEDIMIENTO DE EJECUCIÓN MASIVA

### 1. EL GUARDIÁN (Voluntarios, Crones y Cierre)
*Tu trabajo es detectar voluntarios a tiempo y asegurar que el failsafe siga vivo.*
- **Reacción voluntario:** Cualquier emoji que represente una mano (✋, 👍, 👋, 🤚, 🖐️, etc.) cuenta como "yo quiero esta tarea". ✋ es el principal; si ves cualquier otra mano, trátala igual.
- Lee el archivo `./state.md` completo.
- Lee el archivo `./roster.md` completo.

#### 1.1. Escaneo de Reacciones (Entradas PENDIENTE)
- **PARA CADA** fila en `./state.md` con `ESTADO = PENDIENTE`:

  1.  **Lectura de reacciones:** Usa `discord.reactions` con message-id=[MSG_TAREAS_ID] y target=`placeholder` (#tareas-arbitrales).

  2.  **SI HAY reacción de mano (✋ u otro emoji de mano) — Asignación Pull inmediata:**
      - **🛡️ GUARDA ANTI-CARRERA:** Antes de asignar, re-lee `./state.md` y verifica que la fila con este ID_HILO TODAVÍA tenga `ESTADO = PENDIENTE`. Si ya dice `ASIGNADO` o `CERRADO`, **ABORTA** — otro proceso (cron o heartbeat anterior) ya lo resolvió. Pasa al siguiente hilo.
      - Si hay un solo voluntario: ese es el elegido.
      - Si hay múltiples voluntarios: elige al de menor `CARGA_ACTIVA` en `./roster.md`. Desempate: `ULTIMA_ASIGNACION_AUTO` más antigua.
      - **Ejecuta la secuencia de Asignación Pull (AGENTS.md Sección 5.3):**
        a. Publica en el hilo legislativo (threadId=[ID_HILO]): `👮 **Árbitro-Moderador Asignado:** <@ELEGIDO> (voluntario). [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]`
        b. Edita el mensaje de tarea (discord.edit, message-id=[MSG_TAREAS_ID], target=`placeholder`) a este texto completo — no reemplaces solo por una línea; conserva el enlace al hilo:
         `📋 TAREA LEGISLATIVA\nHilo: https://discord.com/channels/placeholder/[ID_HILO]\n✅ ASIGNADO a <@ELEGIDO> (Voluntario)`
        c. Actualiza `./state.md`: ARBITRO=`<@ELEGIDO>`, MODO=`PULL`, ESTADO=`ASIGNADO`.
        d. Si existe el cron `PAAH_[ID_HILO]`, elimínalo con `cron.delete`.
        e. Log en #logs-del-sistema (channelId=`placeholder`): `📋 [PAAH-01] Asignación PULL: <@ELEGIDO> asignado al hilo [ID_HILO] (voluntario).`

  3.  **SI NO HAY reacción de mano (✋ ni otro emoji de mano):**
      - Verifica en `cron.list` que exista el cron `PAAH_[ID_HILO]`.
      - **Si el cron EXISTE:** No hagas nada. El failsafe se encargará.
      - **Si el cron NO EXISTE:** Compara la columna `FECHA_LIMITE_FAILSAFE` de esa fila con la hora actual usando `exec`:
        `python3 -c "from datetime import datetime; import pytz; tz=pytz.timezone('America/Caracas'); lim=datetime.fromisoformat('[FECHA_LIMITE_FAILSAFE]').astimezone(tz); now=datetime.now(tz); print('EXPIRADO' if now>=lim else 'VIGENTE', end='')"` 
        - **Si `VIGENTE`** (aún no vence): **🛡️ ANTI-DUPLICADO:** Ejecuta `cron.list` una vez más para confirmar que el cron `PAAH_[ID_HILO]` realmente no existe (pudo haberse creado entre checks). Si ahora existe, no hagas nada. Si confirmado que no existe, recréalo usando la columna `FECHA_LIMITE_FAILSAFE` de `./state.md` como `schedule.at`. No recalcules el deadline; ya está almacenado. Crea el cron con esta estructura:
          ```json
          {
            "name": "PAAH_[ID_HILO]",
            "agentId": "asignador",
            "sessionTarget": "isolated",
            "wakeMode": "now",
            "schedule": { "kind": "at", "at": "[FECHA_ISO_FAILSAFE]" },
            "payload": {
              "kind": "agentTurn",
              "message": "[PAYLOAD COMPLETO — ver bloque abajo]",
              "model": "anthropic/claude-sonnet-4-5"
            },
            "delivery": { "mode": "announce" }
          }
          ```
          **Payload del mensaje (COPIAR TAL CUAL, sustituyendo los valores entre corchetes):**
          `"CRON AISLADO — FAILSAFE PAAH-01. DATOS: threadId=[ID_HILO], msgTareasId=[MSG_TAREAS_ID], guildId=placeholder, tareasChannelId=placeholder, logsChannelId=placeholder. PASO 0 (GUARDA): Lee ./state.md y localiza la fila con ID_HILO [ID_HILO]. Si la columna ESTADO ya dice 'ASIGNADO' o 'CERRADO', ejecuta cron.delete con nombre 'PAAH_[ID_HILO]' para auto-eliminarte, luego responde con el texto 'GUARDA ACTIVADA: PAAH_[ID_HILO] ya procesado. Cron eliminado.' y termina inmediatamente — NO ejecutes ningún otro paso. PASO 1: Usa discord.reactions con message-id=[MSG_TAREAS_ID] y target=placeholder para leer las reacciones del mensaje de tarea. PASO 2A (SI HAY reacción de mano — ✋ o cualquier emoji de mano): Extrae el usuario que reaccionó. Si hay múltiples, lee ./roster.md y elige el de menor CARGA_ACTIVA (desempate: ULTIMA_ASIGNACION_AUTO más antigua). Usa discord.sendMessage con guildId=placeholder y threadId=[ID_HILO] para publicar: '👮 **Árbitro-Moderador Asignado:** <@ELEGIDO> (voluntario). [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]'. Usa discord.edit con message-id=[MSG_TAREAS_ID] y target=placeholder para actualizar a: '📋 TAREA LEGISLATIVA\nHilo: https://discord.com/channels/placeholder/[ID_HILO]\n✅ ASIGNADO a <@ELEGIDO> (Voluntario)'. Actualiza ./state.md: ARBITRO=<@ELEGIDO>, MODO=PULL, ESTADO=ASIGNADO. Recalcula CARGA_ACTIVA en ./roster.md. Usa discord.sendMessage con channelId=placeholder para publicar: '📋 [PAAH-01] Asignación PULL: <@ELEGIDO> asignado al hilo [ID_HILO] (voluntario).' Termina. PASO 2B (SI NO HAY ✋ — ASIGNACIÓN PUSH): Lee ./roster.md completo. Calcula la CARGA_ACTIVA de cada Árbitro contando en ./state.md las filas donde ARBITRO=<@ID> y ESTADO=ASIGNADO. Selecciona al Árbitro con menor carga. En caso de empate, elige al que tenga ULTIMA_ASIGNACION_AUTO más antigua (o 'NUNCA'). Usa discord.sendMessage con guildId=placeholder y threadId=[ID_HILO] para publicar: '⚠️ **Asignación Automática (PAAH-01 §4):** <@ELEGIDO>, asignado por rotación de carga mínima. [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]'. Usa discord.edit con message-id=[MSG_TAREAS_ID] y target=placeholder para actualizar a: '📋 TAREA LEGISLATIVA\nHilo: https://discord.com/channels/placeholder/[ID_HILO]\n⚠️ ASIGNADO a <@ELEGIDO> (Automático - PAAH-01 §4)'. Actualiza ./state.md: ARBITRO=<@ELEGIDO>, MODO=PUSH, ESTADO=ASIGNADO. Actualiza ./roster.md: CARGA_ACTIVA +1, ULTIMA_ASIGNACION_AUTO=fecha ISO actual. Usa discord.sendMessage con channelId=placeholder para publicar: '📋 [PAAH-01] Asignación PUSH: <@ELEGIDO> asignado al hilo [ID_HILO] (automático, carga mínima).' Termina."`
        - **Si `EXPIRADO`** (deadline vencido): La ventana cerró y el cron falló o se perdió. **EJECUTA ASIGNACIÓN PUSH INMEDIATAMENTE** (RESCATE DE EMERGENCIA):
          - **🛡️ GUARDA ANTI-CARRERA:** Re-lee `./state.md` y verifica que la fila TODAVÍA diga `ESTADO = PENDIENTE`. Si ya dice `ASIGNADO` o `CERRADO`, **ABORTA** — ya fue resuelto.
          a. Lee `./roster.md`. Calcula `CARGA_ACTIVA` contando en `./state.md` filas con `ESTADO = ASIGNADO` por Árbitro. Elige menor carga (desempate: `ULTIMA_ASIGNACION_AUTO` más antigua).
          b. Publica en hilo legislativo (threadId=[ID_HILO]): `⚠️ **Asignación Automática (PAAH-01 §4):** <@ELEGIDO>, asignado por rotación de carga mínima. [STATUS: ÁRBITRO-MODERADOR <@ELEGIDO> ASIGNADO]`
          c. Edita mensaje de tarea (discord.edit, message-id=[MSG_TAREAS_ID], target=`placeholder`) a este texto completo — conserva el enlace al hilo:
           `📋 TAREA LEGISLATIVA\nHilo: https://discord.com/channels/placeholder/[ID_HILO]\n⚠️ ASIGNADO a <@ELEGIDO> (Automático - PAAH-01 §4)`
          d. Actualiza `./state.md`: ARBITRO=`<@ELEGIDO>`, MODO=`PUSH`, ESTADO=`ASIGNADO`.
          e. Actualiza `./roster.md`: `CARGA_ACTIVA` +1, `ULTIMA_ASIGNACION_AUTO` = fecha ISO actual.
          f. Log en #logs-del-sistema (channelId=`placeholder`): `⚠️ [PAAH-01] Asignación PUSH (RESCATE): <@ELEGIDO> asignado al hilo [ID_HILO] (automático, ventana expirada, cron perdido).`

  4.  *Si una fila da error, regístralo en logs internos y CONTINÚA con la siguiente.*

#### 1.2. Cierre de Asignaciones (Entradas ASIGNADO)
- **PARA CADA** fila en `./state.md` con `ESTADO = ASIGNADO`:

  1.  Usa `discord.readMessages` con threadId=[ID_HILO] para buscar el patrón `[STATUS: PROCESO FINALIZADO`.
  2.  **Si lo encuentras:** Actualiza `./state.md` — columna ESTADO a `CERRADO`.
  3.  *Si una fila da error, CONTINÚA con la siguiente.*

#### 1.3. Recálculo de Carga Activa
- Tras procesar TODAS las filas de `./state.md`:
  1.  Para cada Árbitro en `./roster.md`, cuenta las filas en `./state.md` donde `ARBITRO = <@ID>` y `ESTADO = ASIGNADO`.
  2.  Escribe el nuevo valor de `CARGA_ACTIVA` en `./roster.md`.

### 2. EL ARQUITECTO (Detección de Nuevas Propuestas)
*Aquí es donde se detectan propuestas que necesitan Árbitro-Moderador.*
- Ejecuta `discord.threadList` con guildId=`placeholder` y channel-id=`placeholder` (#caucus-legislativo).
- Filtra la lista para obtener **TODOS** los hilos con prefijo `[PROPUESTA EN GESTACIÓN]`.
- Compara contra `./state.md`.
- **PARA CADA** hilo que **NO** esté en `./state.md`:

  1.  **Lectura:** Usa `discord.readMessages` con threadId=[ID_HILO] para buscar el patrón `[STATUS: NECESITA ÁRBITRO-MODERADOR]`.
  2.  **Si NO se encuentra:** Ignora. El Secretario Legislativo aún no ha procesado este hilo.
  3.  **🛡️ GUARDA DE IDEMPOTENCIA (OBLIGATORIA):** Busca también en los mensajes del hilo el patrón `[STATUS: ÁRBITRO-MODERADOR`. Si lo encuentras, este hilo **YA FUE ASIGNADO** (el dato se perdió de `./state.md`). **NO lo reproceses.** En su lugar, reconstruye la fila en `./state.md` con los datos disponibles: `[ID_HILO] | DESCONOCIDO | DESCONOCIDO | <@ARBITRO_DEL_STATUS> | RECUPERADO | ASIGNADO` y pasa al siguiente hilo.
  4.  **Si `[STATUS: NECESITA ÁRBITRO-MODERADOR]` SÍ se encuentra y NO existe `[STATUS: ÁRBITRO-MODERADOR`:**
      a. **Extrae el proponente** del primer mensaje del hilo (o del contexto del tag STATUS).
      b. **Publica tarea** en #tareas-arbitrales usando `discord.sendMessage` con channelId=`placeholder`:
         ```
         📋 NUEVA TAREA LEGISLATIVA DISPONIBLE
         Hilo: https://discord.com/channels/placeholder/[ID_HILO]
         Proponente: [@Usuario]
         Estado: PENDIENTE DE ASIGNACIÓN
         Reacciona con ✋ (o cualquier emoji de mano) para reclamar esta tarea (tienes 2 horas).
         ```
      c. **Registro:** Calcula la fecha límite del failsafe usando `exec`: `python3 sunday_rule.py --hours 2`. El resultado es `[FECHA_LIMITE]`. Escribe en `./state.md`: `[ID_HILO] | [ID_MSG_TAREAS] | [FECHA_LIMITE] | PENDIENTE | PENDIENTE | PENDIENTE`
      d. **Programa Failsafe:** **🛡️ ANTI-DUPLICADO:** Antes de crear el cron, ejecuta `cron.list` y verifica que NO exista ya un cron con nombre `PAAH_[ID_HILO]`. Si ya existe, NO crees otro — sáltate este paso. Si NO existe, créalo usando el mismo `[FECHA_LIMITE]` del paso anterior como `schedule.at`, con la misma estructura y payload definidos en la Sección 1.1 paso 3 de este documento (el bloque JSON + payload literal). **Usa `agentId: "asignador"`.** Sustituye [ID_HILO] y [MSG_TAREAS_ID] con los valores reales de esta propuesta.

  5.  *Si una fila da error, regístralo en logs internos y CONTINÚA con la siguiente.*

### ⚠️ PROTOCOLO DE INYECCIÓN DE PARÁMETROS (CRITICAL)

**INSTRUCCIÓN DE INTERFAZ:**
Al invocar la herramienta `cron.add`, el sistema IGNORARÁ cualquier parámetro externo tipo CLI (como `mode`, `flags`, o `--wake`).

Para garantizar la ejecución correcta requerida, debes inyectar la propiedad `wakeMode` **DENTRO** del objeto `job`.

**❌ INCORRECTO (Alucinación de CLI):**
`cron.add(mode="now", job={...})` -> ESTO FALLARÁ.

**✅ CORRECTO (Estructura de Datos):**
```json
{
  "tool": "cron",
  "action": "add",
  "job": {
    "name": "PAAH_[ID_HILO]",
    "agentId": "asignador",
    "wakeMode": "now",
    "payload": { ... }
  }
}
```

**Notas:**
- La propiedad `wakeMode: "now"` DEBE estar dentro del objeto `job`, nunca como flag externo.
- La propiedad `agentId: "asignador"` es OBLIGATORIA. Sin ella, el cron aislado usará el workspace del agente `main` y no encontrará `./state.md` ni `./roster.md`.

---

## 🧭 PROTOCOLO DE ENRUTAMIENTO

**CASO A: NUEVA PROPUESTA SIN ÁRBITRO (Arquitecto)**
- **Origen:** Detectado en Paso 2 al encontrar `[STATUS: NECESITA ÁRBITRO-MODERADOR]`.
- **Destino Tarea:** channelId `placeholder` (#tareas-arbitrales).
- **Destino Asignación (futuro):** threadId del hilo legislativo.

**CASO B: VOLUNTARIO DETECTADO (Guardián)**
- **Origen:** Reacción de mano (✋ u otro) detectada en Paso 1.1.
- **Destino Asignación:** threadId del hilo legislativo (columna ID_HILO de `./state.md`).
- **Destino Edición:** message-id del mensaje de tarea (columna MSG_TAREAS_ID de `./state.md`) en #tareas-arbitrales.

**🚫 REGLA DE ORO:**
1. **ASIGNACIONES EN HILO:** El `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]` SIEMPRE va en el threadId del hilo legislativo.
2. **TAREAS EN #tareas-arbitrales:** Las ofertas de tarea y ediciones van SOLO al channelId `placeholder`.
3. **LOGS EN #logs-del-sistema:** Los registros de auditoría van SOLO al channelId `placeholder`. Solo se loguean **asignaciones** (PULL/PUSH). NUNCA publiques en logs la detección de nuevas propuestas, escaneos vacíos, ni acciones intermedias.
4. **TARGET PROHIBIDO:** NUNCA uses `"heartbeat"` como target de Discord. `"heartbeat"` es un canal interno del sistema OpenClaw, NO un canal de Discord. Si lo usas, fallará con `Unknown target`.

---

## 🔇 PROTOCOLO DE SILENCIO
- Si tras recorrer todas las listas no hubo cambios: **SILENCIO ABSOLUTO**.
- No reportes "0 cambios". Solo reporta errores críticos o acciones exitosas en los logs internos.
