## PROCESO EJECUTIVO (LODE-01)

**Objetivo:** Gestionar la Sanción o Veto de leyes en `#sala-del-concejo`.



### FASE A: LECTURA Y REFLEXIÓN (Fase I)

1.  **SCAN:** Busca propuestas nuevas en `#sala-del-concejo` (movidas desde Auditoría Arbitral).

2.  **ACCIÓN PÚBLICA (INICIO):**

    * Publica en el hilo:

        > "🧐 **FASE I: EXPOSICIÓN FINAL (LODE-01 Art. 3.2)**

        > **Estado:** Lectura y Reflexión Silenciosa.

        > **Reglas:** Prohibido el debate entre Concejales. Solo se permiten preguntas directas al proponente.

        > **Duración:** 24 Horas Hábiles (Inicia la cuenta regresiva)."

3.  **PROGRAMACIÓN:**

    * Calcula `Now + 24h` (Aplica Regla Domingo).

    * Crea Cron "LODE-InicioVotacion" (`session: isolated`, `delete-after-run: true`).



### FASE B: ACTO DE VOTACIÓN (Fase II - Instrucciones Cron Futuro)

Instrucciones para el Cron al terminar la Fase de Lectura:



1.  **ACCIÓN PÚBLICA (POLL):**

    * Crea una **DISCORD POLL** en el hilo.

    * **Pregunta:** "¿Voto Soberano sobre esta Ley?"

    * **Opciones (Art. 4.2):**

        1. "✅ Sancionado (Aprobar)"

        2. "⛔ Vetado (Rechazar)"

        3. "🔇 Abstención (Neutro)"

    * **Duración:** 24 Horas Hábiles (Aplica Regla Domingo).

    * **Advertencia:** "El voto es un acto puro de juicio. No justificar."

2.  **PROGRAMACIÓN:**

    * Crea Cron "LODE-Escrutinio" (`session: isolated`,`delete-after-run: true` ) para el cierre de la Poll.



### FASE C: PROCLAMACIÓN Y ARCHIVO (Art. 5)

Instrucciones para el Cron de Escrutinio:



1.  **CONTEO:**

    * **SANCIONADO:** Si Votos ✅ > Votos ⛔.

    * **VETADO:** Si Votos ⛔ >= Votos ✅.

2.  **ESCENARIO SANCIONADO:**

    * **Log:** Reporta en `#logs-del-sistema`: "Ley Sancionada: [LINK]".

    * **Gaceta:** Copia el texto íntegro de la propuesta a `#gaceta-oficial` y taguea a @groove.dharma para que haga un commit manual al github de Alianza Caribe.

    * **Cierre:** Cierra (Lock) el hilo en Concejo, no lo elimines.

3.  **ESCENARIO VETADO:**

    * **Log:** Reporta en `#logs-del-sistema`: "Ley Vetada: [LINK]".

    * **Archivo:** Mueve el link al hilo "RECHAZADO EN CONCEJO" dentro de `#logs-del-sistema`, si el hilo no existe, créalo..

    * **Cierre:** Cierra (Lock) y etiqueta como [VETADO].