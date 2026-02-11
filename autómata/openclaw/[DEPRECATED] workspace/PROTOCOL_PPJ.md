## PROTOCOLO DE PROCESO JUDICIAL (PPJ-01)
**Objetivo:** Gestión de plazos y fases del juicio en los canales `#tribunal-caso-[N]`.

### FASE A: INICIO Y DEFENSA (Fase I - Art. 3)
Este bloque se ejecuta inmediatamente después de que el PAJ-01 crea el canal del tribunal.

1.  **ACCIÓN PÚBLICA (APERTURA):**
    * Publica en el nuevo canal `#tribunal-caso-[N]`:
        > "🏛️ **INICIO DE JUICIO (PPJ-01)**
        > **Fase I:** Notificación y Contestación.
        > **Instrucción:** El Demandado tiene la palabra para presentar su Escrito de Defensa.
        > **Plazo:** 72 Horas Hábiles."
2.  **PROGRAMACIÓN:**
    * Calcula `Now + 72h` (Aplica Regla Domingo).
    * Crea Cron "PPJ-FinDefensa-[ID]" (`session: isolated`, `delete-after-run: true`).

### FASE B: TRANSICIÓN DE ALEGATOS (Fase II - Art. 4)
Instrucciones para el Cron al terminar la Fase I:

1.  **VERIFICACIÓN (REBELDÍA):**
    * Escanea el canal. ¿El Demandado publicó algo?
    * **NO:** Publica "⚠️ **DECLARACIÓN DE REBELDÍA (Art. 3.3).** Se asume la no contradicción de los hechos."
    * **SÍ:** Publica "✅ Escrito de Defensa recibido."
2.  **INICIO TURNO QUERELLANTE (Fase II-A):**
    * Publica: "🗣️ **FASE II: ALEGATOS Y PRUEBAS - TURNO QUERELLANTE.** Tiene 48h hábiles para exponer su caso completo."
    * Calcula `Now + 48h` (Regla Domingo).
    * Crea Cron "PPJ-TurnoDemandado-[ID]" (`session: isolated`, `delete-after-run: true`).

Instrucciones para el Cron al terminar Turno Querellante:
1.  **INICIO TURNO DEMANDADO (Fase II-B):**
    * Publica: "🛡️ **FASE II: ALEGATOS Y PRUEBAS - TURNO DEMANDADO.** Tiene 72h hábiles para refutar y presentar pruebas."
    * Calcula `Now + 72h` (Regla Domingo).
    * Crea Cron "PPJ-InicioConclusiones-[ID]" (`session: isolated`, `delete-after-run: true`).

### FASE C: CONCLUSIONES FINALES (Fase III - Art. 5)
Instrucciones para el Cron al terminar Fase II:

1.  **TURNO QUERELLANTE (Fase III-A):**
    * Publica: "📝 **FASE III: CONCLUSIONES - QUERELLANTE.** Resumen final. Prohibido introducir nuevas pruebas. Plazo: 24h hábiles."
    * Calcula `Now + 24h` (Regla Domingo).
    * Crea Cron "PPJ-ConclusionDemandado-[ID]" (`session: isolated`, `delete-after-run: true`).

Instrucciones para el Cron al terminar III-A:
1.  **TURNO DEMANDADO (Fase III-B):**
    * Publica: "📝 **FASE III: CONCLUSIONES - DEMANDADO.** Resumen final. Plazo: 24h hábiles."
    * Calcula `Now + 24h` (Regla Domingo).
    * Crea Cron "PPJ-VistoSentencia-[ID]" (`session: isolated`, `delete-after-run: true`).

### FASE D: DELIBERACIÓN Y SENTENCIA (Fase IV - Art. 6, 7, 8)
Instrucciones para el Cron al terminar Fase III:

1.  **CIERRE DE DEBATE:**
    * Publica: "🔒 **VISTO PARA SENTENCIA.** El debate queda cerrado. El Tribunal entra en deliberación privada (72h hábiles)."
    * Ajusta permisos del canal (si es técnicamente posible) a solo lectura para las partes.
2.  **PROGRAMACIÓN ALERTA:**
    * Calcula `Now + 72h` (Regla Domingo).
    * Crea Cron "PPJ-AlertaSentencia-[ID]" (`session: isolated`, `delete-after-run: true`).

Instrucciones para el Cron de Alerta (Recordatorio al Juez):
1.  **NOTIFICACIÓN:**
    * Menciona al Rol Juez en el canal: "⏰ **TIEMPO CUMPLIDO.** Se requiere la publicación de la SENTENCIA siguiendo el Art. 7 del PPJ-01."
2.  **PUBLICACIÓN AUTOMÁTICA (Scan de Sentencia):**
    * (Este paso es reactivo): Cuando el Autómata detecte un post del Juez conteniendo la palabra clave "FALLO:" o "SENTENCIA":
        * **Copia:** Duplica el texto en `#gaceta-oficial`.
        * **Archivo:** Publica en `#logs-del-sistema`: "Juicio [ID] Finalizado."
        * **Apertura:** Publica en `#pleno-judicial`: "⚠️ **ACCIÓN REQUERIDA:** Juez, por favor haga PÚBLICO el canal `#tribunal-caso-[N]` conforme al Art. 8.2."