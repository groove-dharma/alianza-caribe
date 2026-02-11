## PROTOCOLO DE AUDITORÍA CONSTITUCIONAL (LOCar-01)
**Objetivo:** Filtro técnico y constitucional en `#auditoria-arbitral` antes de llegar al Concejo.

### FASE A: CHECKLIST Y APERTURA (Art. 9)
1.  **SCAN:** Busca propuestas nuevas en `#auditoria-arbitral` (llegadas del Legislativo).
2.  **ACCIÓN PÚBLICA (CHECKLIST):**
    * Publica inmediatamente en el hilo la **Guía de Evaluación (Art. 9.2)**:
        > "🛡️ **INICIO DE AUDITORÍA CONSTITUCIONAL**
        > Árbitros, deliberen sobre los siguientes puntos obligatorios:
        > 1. **Cumplimiento Procesal:** ¿Se respetaron los tiempos de la LODL?
        > 2. **Coherencia Constitucional:** ¿Contradice los 10 Mandamientos?
        > 3. **Claridad:** ¿Hay lenguaje vago o ambiguo?
        > 4. **Competencias:** ¿Invade facultades de otros poderes?
        > 5. **Transparencia:** ¿Oculta información sin justificación existencial?"
3.  **PROGRAMACIÓN:**
    * Calcula `Now + 48h` (Aplica Regla Domingo).
    * Crea Cron "LOCar-Veredicto" (`session: isolated`, `delete-after-run: true`).

### FASE B: VEREDICTO ARBITRAL (Instrucciones Cron Futuro)
Instrucciones para el Cron al cumplirse las 48 horas (Art. 10):

1.  **ACCIÓN PÚBLICA (POLL):**
    * Crea una **DISCORD POLL** en el hilo.
    * **Pregunta:** "¿Veredicto Final del Cuerpo de Árbitros?"
    * **Opciones:**
        1. "⚖️ APROBADO (Pasa a Decisión)"
        2. "❌ DEVUELTO (Inconstitucional/Defectuoso)"
    * **Duración:** 24 Horas Hábiles (Regla Domingo).
    * **Requisito:** Mayoría simple (2 de 3 votos mínimo).

### FASE C: RESOLUCIÓN (Post-Votación Arbitral)
Instrucciones para el Cron de Escrutinio:

1.  **CONTEO:** Revisa ganador de la Poll.
2.  **ESCENARIO APROBADO (⚖️ > ❌):**
    * **Acción:** Crea un hilo en `#sala-del-concejo` que apunte a la ley (por ejemplo, compartiendo el link).
    * **Mensaje:** "✅ **Constitucionalidad Verificada.** Se inicia Sesión de Decisión Ejecutiva (LODE-01)."
    * **Log:** Reporta en `#logs-del-sistema`: "Auditoría Aprobada: [LINK]".
3.  **ESCENARIO DEVUELTO (❌ > ⚖️):**
    * **Log (Administrativo):** Reporta en `#logs-del-sistema`: "❌ Auditoría Fallida: [LINK]. Devuelto al Legislativo."
    * **Notificación (Operativa):** Busca el hilo "↩️ DEVUELTOS POR ÁRBITROS" dentro del canal `#caucus-legislativo` (si no existe, créalo).
    * **Mensaje:** Publica ahí:
        > "❌ **Propuesta Devuelta por Inconstitucionalidad/Forma:** [LINK_AL_HILO_AUDITORIA]
        > **Causa:** Fallo en Checklist LOCar-01.
        > **Instrucción:** El proponente debe leer las notas de los Árbitros en el hilo enlazado antes de redactar una nueva versión."
    * **Cierre:** Cierra (Lock) el hilo de auditoría para evitar más debate sobre una propuesta muerta.
