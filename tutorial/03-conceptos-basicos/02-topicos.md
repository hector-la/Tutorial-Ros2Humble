# Tópicos (Topics)

Referencia oficial: [Understanding ROS 2 Topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html).

## Teoría

Un **tópico** es un canal con nombre por el que los nodos intercambian **mensajes**. Es el
mecanismo de comunicación más usado en ROS2, pensado para **flujos continuos de datos**
(lecturas de sensores, comandos de velocidad, imágenes de cámara, etc.).

Características clave:
- **Publish/Subscribe**: un nodo **publica** (envía) mensajes en un tópico, otro(s) nodo(s) se
  **suscriben** (reciben) a ese tópico. Ni el publicador sabe quién lo escucha, ni el
  suscriptor sabe quién publica — están **desacoplados**.
- **Muchos a muchos**: puede haber varios publicadores y varios suscriptores en el mismo
  tópico al mismo tiempo.
- **Asíncrono**: el publicador no espera respuesta. Es "dispara y olvida".
- Cada tópico tiene un **tipo de mensaje** fijo (ej. `geometry_msgs/msg/Twist`) — todos los
  publicadores/suscriptores de ese tópico deben usar el mismo tipo.

## Ejemplo práctico

Con turtlesim y teleop corriendo:

```bash
ros2 topic list
```

```
/turtle1/cmd_vel
/turtle1/pose
...
```

Ver también los **tipos**:

```bash
ros2 topic list -t
```

```
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/pose [turtlesim/msg/Pose]
```

### Ver los mensajes en vivo

```bash
ros2 topic echo /turtle1/pose
```

Mueve la tortuga con teleop en otra terminal — verás la posición (`x`, `y`, `theta`)
actualizarse en tiempo real. Ctrl+C para parar.

### Info de un tópico

```bash
ros2 topic info /turtle1/cmd_vel
```

Te dice el tipo de mensaje y cuántos publicadores/suscriptores tiene ese tópico ahora mismo.

### Frecuencia de publicación

```bash
ros2 topic hz /turtle1/pose
```

Muestra a qué frecuencia (Hz) se está publicando ese tópico.

### Publicar manualmente (sin teleop)

Puedes publicar en un tópico directamente desde la terminal, sin escribir ningún nodo:

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {z: 1.8}}"
```

La tortuga se mueve en círculo, sin que teleop esté haciendo nada. Esto demuestra el punto
clave: **a `turtlesim_node` no le importa quién publique en `/turtle1/cmd_vel`**, solo escucha
el tópico.

Ctrl+C para parar (o usa `--once` para publicar un solo mensaje en vez de en loop).

### Visualizar el grafo

```bash
rqt_graph
```

Muestra gráficamente los nodos (óvalos) y tópicos (rectángulos) conectándolos con flechas —
muy útil para entender sistemas grandes de un vistazo.

## Ejercicio

1. Con `ros2 topic pub` (arriba) mueve la tortuga sin usar teleop.
2. Abre `rqt_graph` con turtlesim + teleop corriendo. Identifica: ¿qué nodo publica en
   `/turtle1/cmd_vel`? ¿Qué nodo se suscribe?
3. Corre `ros2 topic echo /turtle1/pose` y en otra terminal `ros2 topic hz /turtle1/pose` al
   mismo tiempo — ¿a qué frecuencia publica su posición `turtlesim_node`?

➡️ Siguiente: [Servicios](03-servicios.md)
