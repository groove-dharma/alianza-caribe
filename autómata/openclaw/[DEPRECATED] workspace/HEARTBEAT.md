# ORQUESTADOR DEL SISTEMA (HEARTBEAT)

## 1. AXIOMAS TRANSVERSALES (Reglas Globales)
Estas reglas aplican a TODOS los protocolos satélites.

* **AXIOMA DE TIEMPO (LODL-01 Art. 4.2):**
    * El Autómata NO adivina el tiempo. Lo mide.
    * **Herramienta:** Usa SIEMPRE `exec` para calcular fechas ISO 8601.
    * **La Ley del Domingo:** El intervalo `Domingo 00:00 - 23:59` es tiempo muerto. Si un plazo de horas cae o atraviesa un domingo, esas 24h se suman al final.
* **AXIOMA DE ESTADO:**
    * No confíes en tu memoria. Lee y escribe el estado en archivos Markdown en el workspace (`STATE_LODL.md`, `STATE_ARBITROS.md`, etc.).
* **AXIOMA DE VOTACIÓN:**
    * Nunca uses reacciones para votos vinculantes. Usa **Encuestas Nativas de Discord (Polls)** para garantizar "1 Persona = 1 Voto".
* **AXIOMA DE SILENCIO:**
    * Si no ejecutas ninguna acción, responde SOLO: `HEARTBEAT_OK`. No publiques en Discord si no hay novedades.

## 2. MAPA DE PROTOCOLOS (Router)
El Agente debe consultar los siguientes archivos para ejecutar sus tareas específicas:

| Proceso | Archivo de Protocolo | Objetivo |
| :--- | :--- | :--- |
| **Legislativo** | `PROTOCOL_LODL.md` | Gestión de Propuestas y Votación Popular. |
| **Árbitros (Asignación)** | `PROTOCOL_PAAH.md` | Asignación de moderadores a hilos. |
| **Árbitros (Auditoría)** | `PROTOCOL_LOCAR.md` | Filtro de Constitucionalidad (Checklist). |
| **Ejecutivo** | `PROTOCOL_LODE.md` | Sanción o Veto del Concejo. |
| **Justicia (Entrada)** | `PROTOCOL_PAJ.md` | Admisión de Demandas. |
| **Justicia (Juicio)** | `PROTOCOL_PPJ.md` | Fases del Juicio (Defensa, Pruebas, Sentencia). |
| **Ciudadanía** | `PROTOCOL_LOAC.md` | Auditoría de Méritos y Ciclos (Solo Cron Diario). |