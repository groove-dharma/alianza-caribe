## LEY ORGÁNICA DEL ACTO CIUDADANO (LOAC-01)
**Objetivo:** Auditoría de méritos para el ascenso a Ciudadano Activo y Mantenimiento de Ciclos.

### FASE A: AUDITORÍA INCREMENTAL (Cron Diario Recurrente)
**Frecuencia:** Cada 24h a las 00:00 UTC (`0 0 * * *`).
**Archivo de Estado:** `STATE_CANDIDATES.md` y `STATE_CYCLE.md`.

1.  **CONTROL DE CICLO:**
    * Lee `STATE_CYCLE.md`. Si hoy es domingo, NO sumes día hábil al contador de ciclo.
    * Si no es domingo, suma +1 a `dias_habiles`.
2.  **AUDITORÍA DE ACTIVIDAD (Consistencia):**
    * **Si es Domingo:** Salta este paso.
    * **Si es Lunes-Sábado:** Escanea los logs de mensajes de las últimas 24h.
    * Para cada Residente que haya hablado: Suma +1 a su contador `dias_activos` en `STATE_CANDIDATES.md`.
3.  **AUDITORÍA DE INICIATIVA (Mérito):**
    * Escanea `#aspirante-a-ciudadano`.
    * Busca hilos creados por Residentes.
    * Verifica si tienen ≥ 3 reacciones de validación (👀, ✅, 🔥) de usuarios con rol `Ciudadano` o superior.
    * Si cumple, marca `iniciativa_cumplida: true` en el MD.
4.  **AUDITORÍA DE DELIBERACIÓN (Cruce):**
    * Escanea menciones o hilos movidos en `#caucus-legislativo` o `#propuestas-ciudadanas`.
    * Si un Residente tiene actividad cruzada verificada, marca `deliberacion_cruce: true`.

### FASE B: PROTOCOLO DE RENOVACIÓN (T-7 Días)
**Trigger:** Cuando `STATE_CYCLE.md` indique que faltan 7 días para el fin del ciclo (90 días).

1.  **ACCIÓN PÚBLICA (APERTURA):**
    * Publica en `#sala-del-concejo`:
        > "🏛️ **INICIO DE PROTOCOLO DE ASCENSO (LOAC-01)**
        > **Ciclo:** [N]
        > **Estado:** Evaluación de Méritos.
        > **Instrucción:** Se abrirá un hilo con los expedientes de los candidatos aptos."
    * Crea un Hilo asociado a ese mensaje: "Expedientes de Aspirantes - Ciclo [N]".
2.  **REPORTE INDIVIDUAL (En el Hilo):**
    * Lee `STATE_CANDIDATES.md`. Filtra usuarios con al menos 2 méritos potenciales.
    * Por cada candidato, publica un mensaje en el hilo:
        > "👤 **CANDIDATO:** @Usuario
        > 1. **Iniciativa:** [CUMPLIDO/NO] (Link a propuesta)
        > 2. **Consistencia:** [X/90 Días] ([PORCENTAJE]%)
        > 3. **Deliberación:** [ESTADO] (Requiere validación manual de calidad).
        >
        > **VOTACIÓN DEL CONCEJO:**"
    * Adjunta una **DISCORD POLL** (SÍ/NO) a cada expediente.