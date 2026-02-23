## PROTOCOLO DE ASIGNACIÓN ARBITRAL (PAAH-01)
**Objetivo:** Garantizar que toda propuesta legislativa tenga un Árbitro moderador asignado.

### FASE A: CONVOCATORIA (Mercado de Tareas)
Esta fase se ejecuta simultáneamente con la detección de una nueva propuesta (LODL-01).

1.  **ACCIÓN PÚBLICA:**
    * Publica inmediatamente en el canal `#tareas-arbitrales`:
        > "🚨 **NUEVA ASIGNACIÓN DISPONIBLE**
        > **Hilo:** [ENLACE_AL_HILO_PROPUESTA]
        > **Acción:** Reacciona con ✋ para reclamar este caso."
2.  **REGISTRO TEMPORAL:**
    * Guarda en `STATE_ARBITROS.md`: ID de la Propuesta + ID del mensaje de aviso en tareas-arbitrales.
3.  **PROGRAMACIÓN FAILSAFE:**
    * Calcula `Now + 2h` usando `exec`.
    * **Regla Domingo:** Si el plazo cae en domingo, muévelo al Lunes a la misma hora relativa.
    * Crea un Cron "PAAH-Failsafe" (`session: isolated`).

### FASE B: RESOLUCIÓN (Instrucciones para el Cron Failsafe)
Instrucciones que debe seguir el Cron cuando despierta a las 2 horas:

1.  **LECTURA:** Revisa el mensaje de aviso en `#tareas-arbitrales`.
2.  **ESCENARIO 1: HAY VOLUNTARIOS (Pull)**
    * ¿Existe la reacción ✋?
    * **Acción:** Selecciona al usuario. Si hay varios, elige al que tenga menor `carga_activa` en `STATE_ARBITROS.md`.
    * **Notificación:** Publica en el hilo de la propuesta: "👮‍♂️ **Árbitro Asignado:** @Usuario (Voluntario). El control del debate es tuyo."
3.  **ESCENARIO 2: DESIERTO (Push/Forzoso)**
    * ¿No hay reacciones?
    * **Acción:** Lee `STATE_ARBITROS.md`. Identifica al Árbitro con menor `carga_activa`.
    * **Notificación:** Publica en el hilo de la propuesta: "⚠️ **Asignación Automática (PAAH-01 Art. 4.1):** @Usuario, asignado por rotación de carga mínima."
4.  **CIERRE ADMINISTRATIVO:**
    * Incrementa +1 la `carga_activa` del elegido en `STATE_ARBITROS.md`.
    * Borra (o marca con ❌) el mensaje en `#tareas-arbitrales` para cerrar la oferta.