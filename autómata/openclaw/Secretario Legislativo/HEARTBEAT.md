# HEARTBEAT.md

Cada vez que se active este pulso, ejecuta las siguientes verificaciones en orden:

## 1. Revisión de Hilos Activos
- Lee `state.md` para recuperar la lista de hilos en estado `ACTIVO`. Si `state.md` no existe, créalo.
- Para cada hilo, verifica si el cron job correspondiente a la fase en la que esté sigue programado (`cron.list`).
- Si un hilo `ACTIVO` ha perdido su cron por error de sistema, utiliza `VENCIMIENTO_VET` y `sunday_rule.py` para re-programar la transición faltante inmediatamente.

## 2. Escaneo de Nuevas Propuestas
- Realiza un `discord.threadList` en el canal vinculado (#caucus-legislativo).
- Busca hilos con el prefijo `[PROPUESTA EN GESTACIÓN]`.
- **Filtro:** Si el ID del hilo NO existe en `state.md`, inicia el **Protocolo de Fase I** detallado en `AGENTS.md`.

## 3. Actualización de Árbitros
- Para hilos en `state.md` donde `ARBITRO_MODERADOR` sea `PENDIENTE`:
  - Lee los últimos mensajes del hilo (`readMessages`).
  - Busca la etiqueta: `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  - Si la encuentras, actualiza el registro en `state.md`.

## 4. Finalización de Ronda
- Si no hay hilos nuevos ni errores en los cronómetros, no emitas mensajes en Discord.
- Responde internamente al Gateway con: `HEARTBEAT_OK: Ronda finalizada sin incidencias.`