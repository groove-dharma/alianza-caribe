# HEARTBEAT.md

# 🛑 SYSTEM OVERRIDE: CEGUERA SELECTIVA
**INSTRUCCIÓN CRÍTICA:**
El sistema adjunta mensajes recientes automáticamente. **IGNÓRALOS**.
1. No leas el chat para entender el contexto.
2. Tu ÚNICA fuente de verdad es `./state.md` (ruta obligatoria) y la lista de hilos activos de Discord.
3. Actúa como un **Procesador por Lotes**. No te detengas en el primer ítem; procésalos TODOS.

---

## 🔄 PROCEDIMIENTO DE EJECUCIÓN MASIVA

### 1. EL GUARDIÁN (Mantenimiento y Rescate)
*Tu trabajo es asegurar que el plan siga vivo.*
- Lee el archivo `./state.md` completo.
- **PARA CADA** fila/propuesta en estado `ACTIVO`:

  1.  **Determina la fase actual** leyendo la columna FASE de `state.md`. Esto define qué crones son relevantes:
      - Si FASE = `FASE 1` → crones pendientes: `FASE2_[ID]`, `FASE3_[ID]`, `CIERRE_[ID]`
      - Si FASE = `FASE 2` → crones pendientes: `FASE3_[ID]`, `CIERRE_[ID]` (FASE2 ya se ejecutó, NO lo busques)
      - Si FASE = `FASE 3` → crones pendientes: `CIERRE_[ID]` (FASE2 y FASE3 ya se ejecutaron, NO los busques)

  2.  **Auditoría de Crones (solo fases futuras):** Verifica en `cron.list` si existen ÚNICAMENTE los crones pendientes determinados en el paso anterior.
      - **🚫 PROHIBIDO:** Buscar o re-crear crones de fases ya completadas. Si `state.md` dice `FASE 2`, el cron `FASE2_[ID]` ya cumplió su misión y fue consumido. Re-crearlo causaría duplicación de mensajes.

  3.  **Reparación:** Si falta algún cron de una fase FUTURA, **vuélvelo a crear** inmediatamente usando los tiempos de `sunday_rule.py` calculados desde la fecha actual.

  4.  **Rescate de Emergencia:** Usa la columna `VENCIMIENTO_VET` de `state.md` para determinar si la fase actual ya venció comparando con la hora actual.
       - Si venció y el estado en `state.md` no ha cambiado a la siguiente fase: **EJECUTA LA TRANSICIÓN TÚ MISMO AHORA**.
         - **Acción:** Publica: "⚠️ Debido a un fallo técnico el anuncio de inicio para la FASE X no fue publicado. Confirmo que la FASE X ha iniciado hace X hora(s) y le quedan X hora(s)."
         - **Persistencia:** Actualiza inmediatamente `state.md` a la nueva fase para que no se repita este error en la siguiente vuelta.

  5.  *Si una fila da error, regístralo en logs internos y CONTINÚA con la siguiente.*

### 2. EL ARQUITECTO (Escaneo y Big Bang)
*Aquí es donde nacen las propuestas y su destino.*
- Ejecuta `discord.list_threads` en el canal padre `#caucus-legislativo` (`placeholder`).
- Filtra la lista para obtener **TODOS** los hilos con prefijo `[PROPUESTA EN GESTACIÓN]`.
- Compara contra `./state.md`.
- **PARA CADA** hilo nuevo que **NO** esté en `./state.md`:

  1.  **Captura:** Obtén el ID y el Título.
  2.  **Alta:** Registra en `./state.md` como `FASE 1`.
  3.  **Ejecución Inmediata:** Publica en el hilo el mensaje de **Inicio de FASE I** (ver AGENTS.md Punto 3).

  4.  **💥 PLANIFICACIÓN TOTAL (BIG BANG):**
      - Calcula **T1** (Fin Fase 1), **T2** (Fin Fase 2) y **T3** (Cierre) usando `sunday_rule.py`.
      - **Calcula POLL_DURATION_HOURS** (horas reales del poll): Ejecuta vía `exec`:
        `python3 -c "from datetime import datetime; t2=datetime.fromisoformat('[T2]'); t3=datetime.fromisoformat('[T3]'); print(max(1, int((t3-t2).total_seconds()//3600)))"`
        El resultado es el número de horas que el poll de Discord debe permanecer abierto (mínimo 1 hora, requisito de Discord). Inyéctalo en el payload del Cron B.
      - **Crea AHORA MISMO los 3 crones futuros (Isolated) con payloads autocontenidos.**
        Cada payload DEBE ser una receta completa paso-a-paso. No uses referencias indirectas como "sigue AGENTS.md Punto X". El cron aislado nace ciego; su payload es su única instrucción operativa.
        - **Cron A (Para T1):** Payload: "CRON AISLADO — TRANSICIÓN A FASE II. DATOS: threadId=[ID_HILO], guildId=[ID_GUILD], channelId=[ID_HILO]. PASO 0 (GUARDA): Lee ./state.md y localiza la fila con ID_HILO [ID_HILO]. Si la columna FASE ya dice 'FASE 2' o superior (FASE 3, DONE), ejecuta cron.delete con nombre 'FASE2_[ID_HILO]' para auto-eliminarte, luego responde con el texto 'GUARDA ACTIVADA: FASE2_[ID_HILO] ya procesado. Cron eliminado.' y termina inmediatamente — NO ejecutes ningún otro paso. PASO 1: Usa discord.sendMessage con guildId=[ID_GUILD] y threadId=[ID_HILO] para publicar: '📢 **FASE II: FALSACIÓN (48h)**. Inicia ejercicio de acero (steel man).' PASO 2: Usa discord.readMessages en threadId=[ID_HILO] para buscar el patrón [STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]. Si lo encuentras, extrae la mención. PASO 3: Actualiza ./state.md — columna FASE a 'FASE 2 [ID del mensaje enviado en Paso 1]'. Si encontraste Árbitro en Paso 2, actualiza columna ARBITRO_MODERADOR. PASO 4: Termina."
        - **Cron B (Para T2):** Payload: "CRON AISLADO — TRANSICIÓN A FASE III. DATOS: threadId=[ID_HILO], guildId=[ID_GUILD], channelId=[ID_HILO], pollDurationHours=[POLL_DURATION_HOURS]. PASO 0 (GUARDA): Lee ./state.md y localiza la fila con ID_HILO [ID_HILO]. Si la columna FASE ya dice 'FASE 3' o 'DONE', ejecuta cron.delete con nombre 'FASE3_[ID_HILO]' para auto-eliminarte, luego responde con el texto 'GUARDA ACTIVADA: FASE3_[ID_HILO] ya procesado. Cron eliminado.' y termina inmediatamente — NO ejecutes ningún otro paso. PASO 1: Usa discord.poll en guildId=[ID_GUILD] y threadId=[ID_HILO] con pregunta '¿Elevar propuesta al Cuerpo de Árbitros?', opciones '👍 Elevar', '👎 No elevar' y --poll-duration-hours [POLL_DURATION_HOURS]. PASO 2: Usa discord.sendMessage con guildId=[ID_GUILD] y threadId=[ID_HILO] para publicar: '🗳️ **FASE III: VOTACIÓN (24h)**. Inicia voto para proceso de elevación.' PASO 3: Actualiza ./state.md — columna FASE a 'FASE 3 [ID del mensaje enviado en Paso 2]'. PASO 4: Termina."
        - **Cron C (Para T3):** Payload: "CRON AISLADO — CIERRE Y HANDOFF. DATOS: threadId=[ID_HILO], guildId=[ID_GUILD], channelId=[ID_HILO]. PASO 0 (GUARDA): Lee ./state.md y localiza la fila con ID_HILO [ID_HILO]. Si la columna ESTADO ya dice 'DONE', ejecuta cron.delete con nombre 'CIERRE_[ID_HILO]' para auto-eliminarte, luego responde con el texto 'GUARDA ACTIVADA: CIERRE_[ID_HILO] ya procesado. Cron eliminado.' y termina inmediatamente — NO ejecutes ningún otro paso. PASO 1: Obtén el ARBITRO_MODERADOR registrado en ./state.md para esta fila. PASO 2: Usa discord.readMessages en guildId=[ID_GUILD] y threadId=[ID_HILO] para leer el resultado del poll (ya cerrado por Discord automáticamente). PASO 3: Usa discord.sendMessage con guildId=[ID_GUILD] y threadId=[ID_HILO] para publicar: '📊 **RESULTADO FINAL:** [Aprobado/Rechazado] - [Conteo de Votos].' PASO 4: Usa discord.sendMessage con guildId=[ID_GUILD] y threadId=[ID_HILO] para publicar: '[STATUS: PROCESO FINALIZADO - ESPERANDO ACCIÓN DEL ÁRBITRO-MODERADOR @...]' (usa el árbitro de ./state.md). PASO 5: Actualiza ./state.md — columna ESTADO a 'DONE'. PASO 6: Termina."

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
    "name": "FASE2_[ID]",
    "agentId": "legislativo",
    "wakeMode": "now",
    "payload": { ... }
  }
}
```

**Notas:**
- La propiedad `wakeMode: "now"` DEBE estar dentro del objeto `job`, nunca como flag externo.
- La propiedad `agentId: "legislativo"` es OBLIGATORIA. Sin ella, el cron aislado usará el workspace del agente `main` y no encontrará `./state.md`.

### 3. ACTUALIZACIÓN DE ÁRBITROS
- Filtra las filas de `./state.md` donde `ARBITRO` == `PENDIENTE`.
- **PARA CADA** uno de estos hilos:
  1.  Apuntando a SU `threadId`, busca: `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  2.  Si existe -> Actualiza `./state.md`.
  3.  Si no existe -> Ignora y pasa al siguiente.
---

## 🧭 PROTOCOLO DE ENRUTAMIENTO

**CASO A: NUEVA PROPUESTA (Arquitecto)**
- **Origen:** Detectado en Paso 2.
- **Destino:** El `threadId` del hilo nuevo.
- **Acción:** Ejecuta Punto 3 de AGENTS.md.

**CASO B: RESCATE DE EMERGENCIA (Guardián)**
- **Origen:** Disparado por el Paso 1 (Item 3) al detectar vencimiento no procesado.
- **Destino:** El ID registrado en la **Columna 1** de `state.md`.
- **Acción:** Ejecuta el punto de AGENTS.md correspondiente a la fase que toca.

**🚫 REGLA DE ORO:**
1. **EL HILO ES EL CANAL:** `channelId` SIEMPRE debe ser el ID numérico de la propuesta (Hilo).
2. **ZONA PROHIBIDA:** Bajo ninguna circunstancia uses el ID del canal raíz para publicar actualizaciones. Si no tienes un ID de hilo válido en `./state.md` o en el escaneo, **ABORTA** la operación.
3. **TARGET PROHIBIDO:** NUNCA uses `"heartbeat"` como target de Discord. `"heartbeat"` es un canal interno del sistema OpenClaw, NO un canal de Discord. Si lo usas, fallará con `Unknown target`.

---

## 🔇 PROTOCOLO DE SILENCIO
- Si tras recorrer todas las listas no hubo cambios: **SILENCIO ABSOLUTO**.
- No reportes "0 cambios". Solo reporta errores críticos o acciones exitosas en los logs internos.