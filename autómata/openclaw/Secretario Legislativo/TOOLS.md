# TOOLS.md - Notas Técnicas de Operación

Este archivo contiene las especificaciones exactas para el uso de herramientas por parte del Secretario Legislativo.

## 1. Regla del Domingo (Cálculo Procesal)

Para cumplir con el **Axioma del Domingo**, DEBES usar el script de Python adjunto. No realices cálculos de fechas de forma interna o manual. Si el script da error por falta de herramientas al importe, instala todas las dependencias y continúa tu proceso. 

- **Herramienta:** `exec` (bash/python3)
- **Script:** `sunday_rule.py`
- **Parámetros:** - `--hours 24` (Para Fase I y III)
  - `--hours 48` (Para Fase II)
- **Uso:** El resultado de este script debe insertarse directamente en el flag `--at` de cada comando `cron.add`. 
  - Para **Fase I**: No uses `--start` (el script tomará la hora actual).
  - Para **Fase II y III**: Usa `--start` pasando el valor de `VENCIMIENTO_VET` del hilo actual para mantener la precisión.

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
- **Entrega:** `--delivery announce`
- **Modelo:** `anthropic/claude-haiku-4-5`
- **Mensaje:** Debe incluir el ID del hilo y la instrucción específica de qué fase iniciar o cerrar.

---

**REGLA DE ORO DE MENSAJERÍA**: Cada vez que uses la herramienta discord.message, el parámetro threadId es OBLIGATORIO. Queda estrictamente prohibido enviar mensajes al channelId raíz si existe un hilo activo en el state.md.

---
*Cualquier error en la ejecución de estas herramientas será registrado como una falla en el protocolo notarial.*