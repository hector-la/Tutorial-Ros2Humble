# Servicios (Services)

Referencia oficial: [Understanding ROS 2 Services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html).

## Teoría

Un **servicio** es un patrón de comunicación **petición/respuesta (síncrono)**: un nodo
**cliente** envía una petición, un nodo **servidor** la procesa y devuelve una respuesta.
A diferencia de un tópico, el cliente **sí espera** el resultado.

Úsalo cuando:
- La tarea es **rápida** (se resuelve en un instante, no es un proceso largo).
- Necesitas **un resultado concreto**, no un flujo continuo de datos.

Ejemplos típicos: "dame el estado actual de la batería", "activa este relé", "crea una
tortuga nueva en esta posición".

Diferencia clave con tópicos:

| | Tópico | Servicio |
|---|---|---|
| Patrón | Publish/Subscribe | Petición/Respuesta |
| Participantes | Muchos a muchos | Uno a uno (por llamada) |
| Espera respuesta | No | Sí |
| Uso típico | Flujo continuo (sensores, velocidad) | Acción puntual (spawn, reset, activar algo) |

## Ejemplo práctico

Con turtlesim corriendo:

```bash
ros2 service list
```

```
/clear
/kill
/reset
/spawn
/turtle1/set_pen
/turtle1/teleport_absolute
/turtle1/teleport_relative
...
```

Ver el tipo de un servicio:

```bash
ros2 service type /spawn
```

```
turtlesim/srv/Spawn
```

### Llamar un servicio desde la terminal

```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 3.0, y: 3.0, theta: 0.0, name: 'turtle2'}"
```

Aparece una segunda tortuga en la ventana. Fíjate que el comando **espera y muestra la
respuesta** del servicio (el `name` de la tortuga creada), a diferencia de `topic pub`.

Otro ejemplo — limpiar el rastro dibujado:

```bash
ros2 service call /clear std_srvs/srv/Empty
```

### Ver qué campos necesita un servicio

```bash
ros2 interface show turtlesim/srv/Spawn
```

```
float32 x
float32 y
float32 theta
string name
---
string name
```

Todo lo que está **antes** de `---` es lo que mandas (petición); lo que está **después** es
lo que recibes de vuelta (respuesta).

## Ejercicio

1. Usa `ros2 service call` para crear (`/spawn`) tres tortugas nuevas en distintas posiciones.
2. Usa `ros2 service call /kill` (revisa sus campos con `ros2 interface show turtlesim/srv/Kill`)
   para eliminar una de las que creaste.
3. Compara: ¿qué diferencia notas entre correr `ros2 service call /spawn ...` y
   `ros2 topic pub /turtle1/cmd_vel ...`? Piensa en la respuesta, no solo en el efecto visual.

➡️ Siguiente: [Parámetros](04-parametros.md)
