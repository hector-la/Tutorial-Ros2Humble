# Interfaces (msg / srv / action)

Referencia oficial: [Interfaces (Concepts)](https://docs.ros.org/en/humble/Concepts/Basic/About-Interfaces.html).

## Teoría

Una **interfaz** describe **la estructura de los datos** que viajan entre nodos. Ya las usaste
sin darte cuenta en los 4 archivos anteriores:

- **`.msg`** — estructura de un **mensaje** de tópico. Ej. `geometry_msgs/msg/Twist`.
- **`.srv`** — estructura de **petición + respuesta** de un servicio. Ej. `turtlesim/srv/Spawn`.
- **`.action`** — estructura de **goal + result + feedback** de una acción. Ej.
  `turtlesim/action/RotateAbsolute`.

Los tres son básicamente archivos de texto simples que listan **campos con su tipo** (parecido
a definir los atributos de una clase, sin lógica, solo datos). ROS2 genera automáticamente el
código (en Python/C++/etc.) para que puedas usar esa estructura como un objeto normal en tu
programa.

Por qué importa esto: cuando dos nodos se comunican por un tópico/servicio/acción, **ambos
deben usar exactamente la misma interfaz** — es el "contrato" que asegura que quien publica y
quien escucha se entienden.

## Ejemplo práctico — recorrido de las interfaces que ya usaste

```bash
ros2 interface list
```

Verás una lista larga con todos los `.msg`, `.srv` y `.action` disponibles en tu sistema,
organizados por paquete. Busca los que ya usaste en este módulo:

```bash
ros2 interface show geometry_msgs/msg/Twist       # el mensaje de /turtle1/cmd_vel
ros2 interface show turtlesim/msg/Pose             # el mensaje de /turtle1/pose
ros2 interface show turtlesim/srv/Spawn            # el servicio /spawn
ros2 interface show turtlesim/action/RotateAbsolute # la acción /turtle1/rotate_absolute
```

Fíjate en `Twist` — tiene dos sub-estructuras (`linear` y `angular`), cada una tipo `Vector3`
(`x`, `y`, `z`). Eso es una interfaz **compuesta por otra interfaz**:

```bash
ros2 interface show geometry_msgs/msg/Vector3
```

## Cierre del módulo 03

Con esto ya conectaste las 5 piezas básicas de ROS2:

- **Nodos**: los procesos que hacen el trabajo
- **Tópicos**: cómo fluyen datos continuos entre nodos (con una interfaz `.msg`)
- **Servicios**: cómo se piden/responden tareas puntuales (con una interfaz `.srv`)
- **Parámetros**: cómo se configura un nodo en caliente
- **Acciones**: cómo se manejan tareas largas con feedback y cancelación (con una interfaz
  `.action`)

## Ejercicio final del módulo

Sin mirar la guía, usando solo turtlesim y comandos `ros2`:
1. Levanta turtlesim, crea una segunda tortuga por servicio.
2. Cambia el color de fondo por parámetro.
3. Mueve una tortuga por tópico (`topic pub`), sin usar teleop.
4. Gírala a un ángulo exacto por acción.
5. Para cada uno de los 4 pasos anteriores, di en voz alta qué interfaz (`.msg`/`.srv`/`.action`)
   se usó por debajo.

Si puedes hacer esto de memoria, estás listo para el módulo 04.

➡️ Siguiente: **04 — Herramientas CLI** (`rqt_console`, `ros2 launch`, `ros2 bag`)
