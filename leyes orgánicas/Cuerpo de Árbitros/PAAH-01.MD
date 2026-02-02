# PROTOCOLO TÉCNICO DE ASIGNACIÓN ARBITRAL HÍBRIDA (PAAH-01)

---

## 1. Propósito

Este protocolo gobierna la asignación de un Árbitro-Moderador a cada nuevo hilo abierto en #caucus-legislativo, garantizando eficiencia, equidad y continuidad procesal. Es un protocolo técnico ejecutado por el bot del sistema, "El Autómata", bajo la supervisión del Cuerpo de Árbitros.

## 2. Evento Desencadenante

El protocolo se activa en el momento en que un Legislador crea un nuevo hilo en #caucus-legislativo que cumple con el formato definido en el anexo A de la LODL-01

## 3. Fase I: Mercado de Tareas (Pull)

**3.1.** Al activarse, El Autómata publicará inmediatamente un mensaje en un canal privado para Árbitros, #tareas-arbitrales, con el siguiente formato:

```
NUEVA TAREA LEGISLATIVA DISPONIBLE
Hilo: [Enlace al nuevo hilo en #caucus-legislativo]
Proponente: [@Usuario]
Estado: PENDIENTE DE ASIGNACIÓN
```

Un Árbitro disponible debe reclamar esta tarea reaccionando a este mensaje con el botón ✋ en las próximas 2 horas.

**3.2.** Cualquier miembro con el rol de Árbitro puede reaccionar con ✋. El primer Árbitro que reaccione se convierte en el Árbitro-Moderador asignado.

**3.3.** El Autómata actualizará el mensaje en #tareas-arbitrales a "ASIGNADO a [@Árbitro]" y anunciará en el hilo legislativo original: "El Árbitro-Moderador para este hilo es [@Árbitro]. Comienza la Fase I (Clarificación) de 24 horas."

**3.4.** El Autómata iniciará un contador de tiempo visible para la fase, conforme a la LODL-01.

## 4. Fase II: Asignación Supervisada (Push)

**4.1.** Si transcurren dos (2) horas desde la publicación en #tareas-arbitrales y ningún Árbitro ha reclamado la tarea, se activa la Fase II.

**4.2.** El Autómata ejecutará un comando para determinar la carga de trabajo actual de todos los Árbitros. La "carga" se define como el número de hilos legislativos que un Árbitro está moderando activamente.

**4.3.** El Autómata asignará automáticamente la tarea al Árbitro con la menor carga de trabajo. En caso de empate, la asignación se hará al Árbitro que haya recibido su última asignación automática hace más tiempo (para garantizar la rotación).

**4.4.** El Autómata ejecutará las mismas acciones descritas en los puntos 3.3 y 3.4. El anuncio en el hilo legislativo indicará que la asignación fue automática: "Ningún Árbitro reclamó esta tarea. Por protocolo PAAH-01, se asigna al Árbitro-Moderador [@Árbitro]. Comienza la Fase I..."

## 5. Registro y Auditoría

Todas las acciones de El Autómata (creación de tarea, reclamación, asignación automática) serán registradas en el canal de log (#logs-del-sistema) para garantizar la total transparencia del proceso de asignación, conforme a la LOCAr-01.
