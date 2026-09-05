# Acciones (Actions)

Referencia oficial: [Understanding ROS 2 Actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html).

## Teoría

Una **acción** es para tareas que **toman tiempo en completarse** y donde quieres:
- Enviar un **goal** (objetivo) y no bloquear esperando el resultado.
- Recibir **feedback** periódico de progreso mientras se ejecuta.
- Poder **cancelar** la tarea a mitad de camino.
- Recibir un **resultado** final cuando termina.

Es, en esencia, una combinación de tópicos + servicios: por dentro, una acción usa servicios
para enviar el goal y cancelarlo, y tópicos para el feedback continuo. Por eso ROS2 la
construye **sobre** esos dos conceptos que ya viste, no es un mecanismo aparte desde cero.

| | Servicio | Acción |
|---|---|---|
| Duración típica | Instantánea | Puede tardar (segundos/minutos) |
| Feedback de progreso | No | Sí |
| Cancelable | No | Sí |
| Ejemplo | "dame la posición actual" | "muévete al punto X" (mientras viaja, reporta avance) |

## Ejemplo práctico

Con turtlesim corriendo:

```bash
ros2 action list
```

```
/turtle1/rotate_absolute
```

Ver info del tipo:

```bash
ros2 action info /turtle1/rotate_absolute
```

Ver la estructura del goal/feedback/result:

```bash
ros2 interface show turtlesim/action/RotateAbsolute
```

```
float32 theta
---
float32 delta
---
float32 remaining
```

Igual que en servicios, lo de arriba de la primera `---` es lo que envías (goal), lo de en
medio es el resultado final, y lo de abajo es el feedback que llega mientras se ejecuta.

### Enviar un goal y ver el feedback en vivo

```bash
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}" --feedback
```

Verás la tortuga girar hasta apuntar al ángulo indicado (en radianes), y en la terminal vas a
ver mensajes de **feedback** (`remaining`) mientras gira, hasta el mensaje final de
**resultado**.

Prueba cancelarlo a mitad de camino: lanza el mismo comando y presiona **Ctrl+C** antes de
que termine — el goal se cancela y la tortuga se detiene donde estaba.

## Ejercicio

1. Envía un goal a `/turtle1/rotate_absolute` con `--feedback` y observa cómo baja el valor
   de `remaining` hasta 0.
2. Envía otro goal y cancélalo con Ctrl+C a la mitad. ¿En qué ángulo se quedó la tortuga?
3. Compara con tu propia definición: ¿por qué "girar hasta un ángulo" es una acción y no un
   servicio? ¿Qué pasaría si `rotate_absolute` fuera un servicio en vez de una acción?

➡️ Siguiente: [Interfaces (msg / srv / action)](06-interfaces.md)
