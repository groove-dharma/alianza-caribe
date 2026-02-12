# HEARTBEAT.md

# 🛑 SYSTEM OVERRIDE: CEGUERA SELECTIVA
**INSTRUCCIÓN CRÍTICA:**
El sistema adjunta mensajes recientes automáticamente. **IGNÓRALOS**.
1. No leas el chat para entender el contexto.
2. Tu ÚNICA fuente de verdad es `state.md` y la lista de hilos activos de Discord.
3. Actúa como un **Procesador por Lotes**. No te detengas en el primer ítem; procésalos TODOS.

---

## 🔄 PROCEDIMIENTO DE EJECUCIÓN MASIVA

### 1. MANTENIMIENTO DE CARTERA (Iterar `state.md`)
- Lee el archivo `state.md` completo.
- **PARA CADA** fila/propuesta en estado `ACTIVO`:
  1.  **Check de Cron:** ¿Existe su job en `cron.list`?
  2.  **Check de Tiempo:** Calcula si ya pasó el tiempo estipulado en su columna de fecha (usando `sunday_rule.py`).
  3.  **Acción:** Si falta el cron o el tiempo venció, ejecuta la transición de fase (Fase I -> Fase II, etc.) **INMEDIATAMENTE**.
  4.  *Si una fila da error, regístralo en el canal #logs-del sistema ID: placeholder y CONTINÚA con la siguiente fila.*

### 2. ESCANEO DE NUEVOS INGRESOS (Iterar Discord)
- Ejecuta `discord.list_threads` en el canal padre `#caucus-legislativo` (`placeholder`).
- Filtra la lista para obtener **TODOS** los hilos con prefijo `[PROPUESTA EN GESTACIÓN]`.
- Compara contra `state.md`.
- **PARA CADA** hilo que **NO** esté en `state.md`:
  1.  **Captura:** Obtén el ID y el Título.
  2.  **Alta:** Inicia el **Protocolo de Fase I** (ver abajo).
  3.  **Registro:** Escribe la nueva entrada en `state.md`.
  4.  *Continúa con el siguiente hilo nuevo, si existe.*

### 3. ACTUALIZACIÓN DE ÁRBITROS (Iterar Pendientes)
- Filtra las filas de `state.md` donde `ARBITRO` == `PENDIENTE`.
- **PARA CADA** uno de estos hilos:
  1.  Apuntando a SU `threadId`, busca: `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  2.  Si existe -> Actualiza `state.md`.
  3.  Si no existe -> Ignora y pasa al siguiente.

---

## 🧭 PROTOCOLO DE ENRUTAMIENTO Y EJECUCIÓN (CRÍTICO)

Tu comportamiento se rige por la **Ley de `AGENTS.md`**. No improvises.

**CASO A: NUEVA PROPUESTA (Detectada en Escaneo)**
- **Origen:** Detectado por `discord.list_threads` (Paso 2).
- **Destino (`channelId`):** El `threadId` del hilo detectado.
- **Acción:** Ejecuta textualmente el **Punto 3 de AGENTS.md** ("FASE I: CLARIFICACIÓN").
- **Persistencia:** Crea el registro en `state.md`.

**CASO B: TRANSICIONES DE FASE (Crones Aislados o Rescate)**
- **Origen:** Disparado por un Cron programado o por el Heartbeat al detectar vencimiento en `state.md`.
- **Destino (`channelId`):** El ID registrado en la **Columna 1** de `state.md`.
- **Acción:**
  - Si toca Fase II: Ejecuta textualmente el **Punto 4 (Fase II) de AGENTS.md**.
  - Si toca Fase III: Ejecuta textualmente el **Punto 4 (Fase III) de AGENTS.md**.
  - Si toca Cierre: Ejecuta textualmente el **Punto 5 de AGENTS.md**.

**🚫 REGLA DE ORO DE INFRAESTRUCTURA:**
1. **EL HILO ES EL CANAL:** Para la herramienta `discord`, el parámetro `channelId` SIEMPRE debe ser el ID de la propuesta (Hilo).
2. **ZONA PROHIBIDA:** Bajo ninguna circunstancia uses el ID del canal raíz (`placeholder...`) para publicar actualizaciones. Si no tienes un ID de hilo válido en `state.md` o en el escaneo, **ABORTA** la operación.

---

## 🔇 PROTOCOLO DE SILENCIO
- Si tras recorrer todas las listas no hubo cambios: **SILENCIO ABSOLUTO**.
- No reportes "0 cambios". Solo reporta errores críticos o acciones exitosas en los logs internos.