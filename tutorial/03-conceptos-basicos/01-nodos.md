# Nodos

Referencia oficial: [Understanding ROS 2 Nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html).

## Teoría

Un **nodo** es un proceso que ejecuta cómputo. Cada nodo debería tener **una responsabilidad
concreta** (ej. controlar un motor, leer un sensor, hacer planificación de ruta). Un sistema
robótico completo con ROS2 es en realidad **muchos nodos pequeños** trabajando juntos, en vez
de un solo programa gigante — esto se llama **arquitectura modular**, y tiene ventajas:

- Puedes reiniciar/depurar un nodo sin tumbar todo el sistema.
- Puedes reescribir un nodo en otro lenguaje (Python/C++) sin tocar los demás.
- Distintos nodos pueden correr en distintas máquinas del mismo robot.

Los nodos se comunican entre sí mediante:
- **Tópicos** (flujo continuo de datos, muchos-a-muchos)
- **Servicios** (petición/respuesta puntual)
- **Acciones** (tareas largas con feedback)
- **Parámetros** (valores de configuración)

Al conjunto de nodos comunicándose se le llama el **grafo de ROS2 (ROS graph)**.

## Ejemplo práctico

Con `turtlesim_node` y `turtle_teleop_key` corriendo (ver [README del módulo](README.md)):

```bash
ros2 node list
```

Verás algo como:
```
/turtlesim
/teleop_turtle
```

Cada nodo tiene un nombre único en el grafo. Para ver el detalle de un nodo — qué tópicos
publica/suscribe, qué servicios ofrece, qué acciones tiene:

```bash
ros2 node info /turtlesim
```

Lee la salida con calma: verás secciones `Subscribers`, `Publishers`, `Service Servers`,
`Action Servers`, etc. Todo eso lo vamos a entender en los siguientes archivos.

### Remapear un nodo

Puedes cambiar el nombre con el que corre un nodo sin tocar su código:

```bash
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=mi_tortuga
```

Corre `ros2 node list` de nuevo — ahora en vez de `/turtlesim` verás `/mi_tortuga`. Esto es
útil cuando necesitas correr **el mismo nodo varias veces** (ej. dos cámaras del mismo tipo).

## Ejercicio

1. Con turtlesim y teleop corriendo, ejecuta `ros2 node info /teleop_turtle`. ¿Qué tópicos
   publica ese nodo? ¿Coincide con lo que esperarías de un nodo que lee el teclado y mueve
   una tortuga?
2. Corre un segundo `turtlesim_node` remapeado (como arriba) en una cuarta terminal. Ejecuta
   `ros2 node list` — ¿cuántos nodos ves ahora?

➡️ Siguiente: [Tópicos](02-topicos.md)
