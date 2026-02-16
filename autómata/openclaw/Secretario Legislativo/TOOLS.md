# TOOLS.md - Notas Técnicas de Operación

Este archivo contiene las especificaciones exactas para el uso de herramientas por parte del Secretario Legislativo.

## 1. Regla del Domingo (Cálculo Procesal en Cadena)

Para la **Planificación Total (Big Bang)**, DEBES usar el script `sunday_rule.py` con tu herramienta `exec` en cadena para calcular T1, T2 y T3:

1.  **T1 (Fin Fase I):** Ejecuta `python3 sunday_rule.py --hours 24`. El resultado es T1.
2.  **T2 (Fin Fase II):** Ejecuta `python3 sunday_rule.py --hours 48 --start "T1"`. El resultado es T2.
3.  **T3 (Cierre):** Ejecuta `python3 sunday_rule.py --hours 24 --start "T2"`. El resultado es T3.

**Uso Crítico:** Inserta estos resultados exactos en el parámetro `schedule.at` de cada objeto `job`.

## 2. Acciones de Discord (Gobernanza)

Instrucciones específicas para la interacción con el servidor de Alianza Caribe:

- **Envío de mensajes en Hilo:** Utilizar `discord.sendMessage`
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

## 4. Cron Jobs (Transiciones - JSON SCHEMA)

Configuración MANDATORIA para los objetos `job` dentro de `cron.add`. NO USES FLAGS DE TERMINAL (`--`). Usa esta estructura de datos:

- **sessionTarget:** `"isolated"`
- **wakeMode:** `"now"` (OBLIGATORIO)
- **delivery:** `{ "mode": "announce" }`
- **payload:**
  - **kind:** `"agentTurn"`
  - **model:** `"anthropic/claude-3-5-sonnet-20241022"`
  - **message:** DEBE contener explícitamente:
    1. El **ID numérico del hilo**.
    2. El **ID numérico del GUILD**.
    3. El **ID numérico del canal padre `#caucus-legislativo`**.
    4. La instrucción clara (ej: "Ejecuta Fase II...").
  
**Prohibido:** Usar variables abstractas como "hilo actual". El cron aislado nace ciego; si no le pasas los IDs en el `message`, fallará.

---

### Uso de discord.sendMessage
- Cuando respondas a una propuesta existente:
  `guildId`: [ID del Servidor]
  `channelId`: [ID del Hilo Específico]
  `threadId`: [ID del Hilo Específico]
- **Nota:** Nunca omitas el `threadId`. Las respuestas deben ser quirúrgicas dentro del contenedor de la propuesta.

---
*Cualquier error en la ejecución de estas herramientas será registrado como una falla en el protocolo notarial.*