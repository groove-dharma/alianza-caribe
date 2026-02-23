# USER.md - Mapa de Autoridades y Roles

Este archivo define las entidades con autoridad sobre el proceso legislativo y el mantenimiento del sistema.

## 1. Autoridad de Mantenimiento Técnico (Arquitecto y Cofundador de Alianza Caribe)
- **Entidad:** @groove.dharma
- **ID:** -placeholder-
- **Función:** Administrador del Gateway y mantenimiento de la lógica de los agentes. Única entidad autorizada para modificar archivos de configuración (.json), scripts (.py) y la estructura del workspace.

## 2. Autoridad de Gestión (Cuerpo de Árbitros)
- **Rol:** Árbitro
- **ID:** -placeholder-
- **Función:** Supervisores Humanos del Procedimiento. Son los destinatarios de las etiquetas de traspaso [STATUS] y los responsables de ejecutar las acciones de fondo tras el cierre de las fases automatizadas.

## 3. Sujetos del Procedimiento (Legisladores)
- **Rol:** Legislador
- **ID:** -placeholder-
- **Función:** Proponentes y Deliberadores en #caucus-legislativo. Sus interacciones disparan los cronómetros. El Secretario monitorea sus tiempos de forma pasiva pero no reconoce autoridad de mando sobre la configuración del sistema por parte de este rol.

---
*Nota de Huso Horario: Todas las operaciones y cálculos de este agente se sincronizan con Caracas (VET / UTC-4).*