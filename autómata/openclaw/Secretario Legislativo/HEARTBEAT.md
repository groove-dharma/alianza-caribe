# HEARTBEAT.md

# 🛑 SYSTEM OVERRIDE: CEGUERA SELECTIVA
**INSTRUCCIÓN CRÍTICA:**
El sistema adjunta mensajes recientes automáticamente. **IGNÓRALOS**.
1. No leas el chat para entender el contexto.
2. Tu ÚNICA fuente de verdad es `state.md` y la lista de hilos activos de Discord.
3. Actúa como un **Procesador por Lotes**. No te detengas en el primer ítem; procésalos TODOS.

---

## 🔄 PROCEDIMIENTO DE EJECUCIÓN MASIVA

### 1. EL GUARDIÁN (Mantenimiento y Rescate)
*Tu trabajo es asegurar que el plan siga vivo.*
- Lee el archivo `state.md` completo.
- **PARA CADA** fila/propuesta en estado `ACTIVO`:
  1.  **Auditoría de Crones:** Verifica en `cron.list` si existen los trabajos futuros programados para este hilo (Busca por nombre: `FASE2_[ID]`, `FASE3_[ID]`, `CIERRE_[ID]`).
  2.  **Reparación:** Si falta algún cron futuro (y aún no ha pasado su fecha), **vuélvelo a crear** inmediatamente usando los tiempos de `sunday_rule.py`.
  3.  **Rescate de Emergencia:** Calcula si la fecha de la fase actual YA VENCIÓ.
       - Si venció y el estado en `state.md` no ha cambiado: **EJECUTA LA TRANSICIÓN TÚ MISMO AHORA**.
         - **Acción:** Publica: "⚠️ Debido a un fallo técnico el anuncio de inicio para la FASE X no fue publicado. Confirmo que la FASE X ha iniciado hace X hora(s) y le quedan X hora(s)."
         - **Persistencia:** Actualiza inmediatamente `state.md` a la nueva fase para que no se repita este error en la siguiente vuelta.
  4.  *Si una fila da error, regístralo en logs internos y CONTINÚA con la siguiente.*

### 2. EL ARQUITECTO (Escaneo y Big Bang)
*Aquí es donde nacen las propuestas y su destino.*
- Ejecuta `discord.list_threads` en el canal padre `#caucus-legislativo` (`placeholder`).
- Filtra la lista para obtener **TODOS** los hilos con prefijo `[PROPUESTA EN GESTACIÓN]`.
- Compara contra `state.md`.
- **PARA CADA** hilo nuevo que **NO** esté en `state.md`:

  1.  **Captura:** Obtén el ID y el Título.
  2.  **Alta:** Registra en `state.md` como `FASE 1`.
  3.  **Ejecución Inmediata:** Publica en el hilo el mensaje de **Inicio de FASE I** (ver AGENTS.md Punto 3).

  4.  **💥 PLANIFICACIÓN TOTAL (BIG BANG):**
      - Calcula **T1** (Fin Fase 1), **T2** (Fin Fase 2) y **T3** (Cierre) usando `sunday_rule.py`.
      - **Crea AHORA MISMO los 3 crones futuros (Isolated):**
        - **Cron A (Para T1):** Payload: "Ejecuta Transición a FASE II en el Hilo ID [INSERTAR_ID_AQUI], el guildId es [INSERTAR_ID_AQUI], el ID del canal padre `#caucus-legislativo` es [INSERTAR_ID_AQUI]. Sigue instrucciones de AGENTS.md Punto 4."
        - **Cron B (Para T2):** Payload: "Ejecuta Transición a FASE III en el Hilo ID [INSERTAR_ID_AQUI], el guildId es [INSERTAR_ID_AQUI], el ID del canal padre `#caucus-legislativo` es [INSERTAR_ID_AQUI]. Sigue instrucciones de AGENTS.md Punto 4."
        - **Cron C (Para T3):** Payload: "Ejecuta Cierre y Handoff en el Hilo ID [INSERTAR_ID_AQUI], el guildId es [INSERTAR_ID_AQUI], el ID del canal padre `#caucus-legislativo` es [INSERTAR_ID_AQUI]. Sigue instrucciones de AGENTS.md Punto 5."

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
    "wakeMode": "now",  <-- OBLIGATORIO AQUÍ
    "payload": { ... }
  }
}

### 3. ACTUALIZACIÓN DE ÁRBITROS
- Filtra las filas de `state.md` donde `ARBITRO` == `PENDIENTE`.
- **PARA CADA** uno de estos hilos:
  1.  Apuntando a SU `threadId`, busca: `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  2.  Si existe -> Actualiza `state.md`.
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
1. **EL HILO ES EL CANAL:** `channelId` SIEMPRE debe ser el ID de la propuesta (Hilo).
2. **ZONA PROHIBIDA:** Bajo ninguna circunstancia uses el ID del canal raíz (`placeholder...`) para publicar actualizaciones. Si no tienes un ID de hilo válido en `state.md` o en el escaneo, **ABORTA** la operación.

---

## 🔇 PROTOCOLO DE SILENCIO
- Si tras recorrer todas las listas no hubo cambios: **SILENCIO ABSOLUTO**.
- No reportes "0 cambios". Solo reporta errores críticos o acciones exitosas en los logs internos.