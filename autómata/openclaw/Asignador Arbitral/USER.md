# USER.md - Mapa de Autoridades y Roles

Este archivo define las entidades con autoridad sobre el proceso de asignación arbitral y el mantenimiento del sistema.

## 1. Autoridad de Mantenimiento Técnico (Arquitecto y Cofundador de Alianza Caribe)
- **Entidad:** @groove.dharma
- **ID:** placeholder
- **Función:** Administrador del Gateway y mantenimiento de la lógica de los agentes. Única entidad autorizada para modificar archivos de configuración (.json), scripts (.py), el roster (`./roster.md`) y la estructura del workspace.

## 2. Sujetos y Destinatarios del Protocolo (Cuerpo de Árbitros)
- **Rol:** Árbitro
- **Función:** Candidatos a Árbitro-Moderador. Son quienes reclaman tareas con ✋ (u otro emoji de mano) en #tareas-arbitrales (Fase Pull) o reciben asignación automática (Fase Push). El roster completo con IDs se mantiene en `./roster.md`.

## 3. Agente Hermano (Secretario Legislativo)
- **Entidad:** Secretario Legislativo (agentId: `legislativo`)
- **Función:** Publica `[STATUS: NECESITA ÁRBITRO-MODERADOR]` al detectar nuevas propuestas y lee `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]` durante la transición a FASE II. La comunicación entre agentes es exclusivamente vía etiquetas STATUS en hilos de Discord.

---
*Nota de Huso Horario: Todas las operaciones y cálculos de este agente se sincronizan con Caracas (VET / UTC-4).*
