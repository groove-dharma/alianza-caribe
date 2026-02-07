## PROCESO LEGISLATIVO (LODL-01)
**Objetivo:** Gestionar el ciclo de vida de las propuestas en `#caucus-legislativo`.

### FASE A: DETECCIÓN (Heartbeat)
1.  **SCAN:** Busca hilos con título `[PROPUESTA EN GESTACIÓN]` que no estén registrados en `STATE_LODL.md`.
2.  **CÁLCULO:** Ejecuta `exec` para `Now + 24h` (Aplica Regla Domingo).
3.  **REGISTRO:** Añade el Hilo ID a `STATE_LODL.md`.
4.  **ACCIÓN PÚBLICA:**
    * Publica en el hilo: "📢 **Inicio de Fase I (Clarificación).** Cierre programado: [FECHA]. Solo preguntas de entendimiento."
    * Dispara el PAAH (Aviso en `#tareas-arbitrales`).
5.  **ACCIÓN CRON:** Programa el cierre (`session: isolated`, `delete-after-run: true`).

### FASE B: TRANSICIÓN AUTOMÁTICA (Instrucciones para Crones Futuros)
Cuando programes los crones de cierre, inyéctales estas instrucciones:

* **Al cerrar FASE I (Clarificación):**
    * Anuncia fin de fase.
    * Calcula `Now + 48h` (Regla Domingo).
    * Inicia **FASE II (Falsación)**: "Se abre debate crítico. Solo objeciones fundamentadas."
* **Al cerrar FASE II (Falsación):**
    * Anuncia fin de fase.
    * Calcula `Now + 24h` (Regla Domingo).
    * Inicia **FASE III (Síntesis)**: "El proponente debe integrar críticas y presentar versión final."
* **Al cerrar FASE III (Síntesis):**
    * Calcula `Now + 24h` (Regla Domingo).
    * Crea **DISCORD POLL** en el hilo: "¿Elevar al Cuerpo de Árbitros? [SÍ/NO]".

### FASE C: CIERRE Y ARCHIVO (Post-Votación)
Instrucción para el Cron de Conteo de Votos:

1.  **Leer Poll:** ¿Ganó SÍ o NO?
2.  **CASO APROBADO (SÍ > NO):**
    * **Acción:** Mueve el hilo (o publica el link y resumen) en `#auditoria-arbitral`.
    * **Mensaje:** "🚀 **Elevado para Revisión Constitucional.** Pendiente de Check-list Arbitral."
3.  **CASO RECHAZADO (NO > SÍ):**
    * Busca el hilo "RECHAZADO EN LEGISLATIVO" dentro del canal `#logs-del-sistema`. (Si no existe, créalo).
    * Publica ahí: "🗑️ **Propuesta Archivada:** [LINK_AL_HILO_PROPUESTA] - Rechazada por votación legislativa."
    * Cierra (Lock) el hilo de la propuesta original.