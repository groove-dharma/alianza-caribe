## PROTOCOLO DE ACCESO A LA JUSTICIA (PAJ-01)
**Objetivo:** Recepción, Numeración y Admisión de demandas en `#secretaria-judicial`.

### FASE A: ACUSE DE RECIBO Y REGISTRO (Art. 4.1)
1.  **SCAN:** Busca nuevos posts en `#secretaria-judicial` con la plantilla `PDJ-01` no registrados en `STATE_JUDICIAL.md`.
2.  **GENERACIÓN ID:**
    * Lee `last_id` en `STATE_JUDICIAL.md`.
    * Incrementa +1. Formato: `CASO LOPJ-[00N]`.
3.  **ACCIÓN PÚBLICA (RESPUESTA):**
    * Responde al post:
        > "⚖️ **ACUSE DE RECIBO (PAJ-01)**
        > **Caso Asignado:** [NUEVO_ID]
        > **Estado:** Triage y Admisión.
        > **Plazo:** El Pleno tiene 72 horas hábiles para emitir veredicto."
4.  **ACCIÓN PÚBLICA (POLL JUDICIAL):**
    * Inmediatamente después, crea una **DISCORD POLL** en el mismo hilo para los Jueces.
    * **Pregunta:** "¿Veredicto de Admisión para el [NUEVO_ID]?"
    * **Opciones (Art. 4.3):**
        1. "✅ ADMITIDO A TRÁMITE"
        2. "⚠️ RECHAZADO POR FORMA (Devolver)"
        3. "⛔ DESESTIMADO POR FONDO (Cerrar)"
    * **Duración:** 72 Horas Hábiles (Regla Domingo).
5.  **PROGRAMACIÓN:**
    * Crea Cron "PAJ-Veredicto" (`session: isolated`, `delete-after-run: true`) para el cierre de la Poll.

### FASE B: EJECUCIÓN DE VEREDICTO (Post-Votación)
Instrucciones para el Cron al cerrar la votación:

1.  **CONTEO:** Determina la opción ganadora.
2.  **ESCENARIO 1: ADMITIDO (✅)**
    * **Log:** Reporta en `#logs-del-sistema`: "Caso [ID] Admitido. Iniciando Juicio."
    * **Acción:** Dispara inmediatamente el **PROTOCOLO PPJ-01**:
        * Crea el canal `#tribunal-[ID]` en la Categoría JUDICIAL (`1469270229782892596`).
        * Publica en el nuevo canal: "⚠️ **ATENCIÓN JUEZ:** Configura este canal como PRIVADO (Solo partes y Jueces)."
        * Notifica en el hilo original de Secretaría: "✅ **Admitido.** Procedimiento trasladado a su tribunal asignado."
3.  **ESCENARIO 2: RECHAZADO POR FORMA (⚠️)**
    * **Acción:** Publica en el hilo:
        > "⚠️ **DEMANDA DEVUELTA POR FORMA**
        > **Causa:** Incumplimiento de plantilla PDJ-01 o evidencia insuficiente.
        > **Instrucción:** El querellante debe corregir y publicar un NUEVO post."
    * **Cierre:** Cierra (Lock) el hilo.
4.  **ESCENARIO 3: DESESTIMADO POR FONDO (⛔)**
    * **Acción:** Publica en el hilo:
        > "⛔ **DEMANDA DESESTIMADA (COSA JUZGADA)**
        > **Causa:** Los hechos no constituyen violación constitucional.
        > **Recurso:** Solo revisable tras 360 días con nueva evidencia (Art. 4.4)."
    * **Cierre:** Cierra (Lock) el hilo.