# TOOLS.md - Notas Técnicas de Operación

Este archivo contiene las especificaciones exactas para el uso de herramientas por parte del Secretario Legislativo.

## 1. Regla del Domingo (Cálculo Procesal en Cadena)

Para la **Planificación Total (Big Bang)**, DEBES usar el script `sunday_rule.py` en cadena para calcular T1, T2 y T3:

1.  **T1 (Fin Fase I):** Ejecuta `python3 sunday_rule.py --hours 24`. El resultado es T1.
2.  **T2 (Fin Fase II):** Ejecuta `python3 sunday_rule.py --hours 48 --start "T1"`. El resultado es T2.
3.  **T3 (Cierre):** Ejecuta `python3 sunday_rule.py --hours 24 --start "T2"`. El resultado es T3.

**Uso Crítico:** Inserta estos resultados exactos en el parámetro correspondiente al tiempo de trigger de cada `cron.add`.

## 2. Acciones de Discord (Gobernanza)

Instrucciones específicas para la interacción con el servidor de Alianza Caribe:

- **Fase III (Votación):** Invoca `discord.poll`.
  - **Pregunta:** "¿Elevar propuesta al Cuerpo de Árbitros?"
  - **Opciones:** `👍 Elevar`, `👎 No elevar`.
- **Detección de Árbitro:** Usa `discord.readMessages`.
  - **Patrón de búsqueda:** `[STATUS: ÁRBITRO-MODERADOR @... ASIGNADO]`.
  - **Extracción:** Captura el ID o mención para el registro en `state.md`.

## 3. Registro de Estado (state.md)

Estructura obligatoria para la persistencia de datos en el workspace:

- **Ruta:** `./state.md`
- **Formato:** Tabla delimitada por pipes (`|`).
- **Cabecera:** `ID_HILO | FASE | VENCIMIENTO_VET | ARBITRO_MODERADOR | ESTADO`

## 4. Cron Jobs (Transiciones)

Configuración mandatoria para los comandos `cron.add`:

- **Sesión:** `--session isolated`
- **Ejecución:** `--wake now`
- **Entrega:** `--delivery announce`
- **Modelo:** `anthropic/claude-sonnet-4-5`
- **Payload (Inyección de Contexto):**
  - El campo `message` (o payload) DEBE contener explícitamente el **ID numérico del hilo** y la referencia a la fase (ej: "Ejecuta Fase II en hilo 12345...").
  - **Prohibido:** No uses variables abstractas como "hilo actual" en el payload; el cron aislado no sabrá cuál es. Escribe el ID.

---

### Uso de discord.message
- Cuando respondas a una propuesta existente:
  `channelId`: placeholder (Caucus-Legislativo)
  `threadId`: [ID obtenido de state.md o del hilo actual]
- **Nota:** Nunca omitas el `threadId` si la acción ocurre dentro de una Propuesta en Gestación. Las respuestas deben ser únicamente dentro de los thread específicos.

---
*Cualquier error en la ejecución de estas herramientas será registrado como una falla en el protocolo notarial.*