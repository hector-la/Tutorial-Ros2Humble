# ros2 bag — grabar y reproducir datos

Referencia oficial: [Recording and playing back data](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html).

## Teoría

**`ros2 bag`** graba en disco todos los mensajes que pasan por uno o varios tópicos, con su
timestamp exacto, y luego los puede **reproducir** exactamente como pasaron. Es como grabar un
video, pero de datos de ROS2.

¿Para qué sirve esto?
- **Depurar sin el robot prendido**: grabas una sesión real una vez, y luego la repites cuantas
  veces quieras para probar tu código, sin necesitar el robot/sensor físico cada vez.
- **Reproducibilidad**: si algo falló en una prueba, grabas el bag y lo puedes analizar/repetir
  después con calma.
- **Compartir datos**: le puedes pasar un archivo `.bag` (en realidad una carpeta) a otra
  persona del equipo para que reproduzca exactamente lo que tú viste.

## Ejemplo práctico

Levanta turtlesim y teleop:

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtlesim turtle_teleop_key
```

### Grabar un tópico

En una tercera terminal:

```bash
mkdir -p ~/bags && cd ~/bags
ros2 bag record /turtle1/cmd_vel
```

Ve a la terminal de teleop y mueve la tortuga un rato con las flechas (10-15 segundos).
Vuelve a la terminal de la grabación y presiona **Ctrl+C** para detenerla. Se crea una carpeta
(ej. `rosbag2_2026_09_05-.../`) con los datos grabados.

### Grabar varios tópicos, o todos

```bash
ros2 bag record /turtle1/cmd_vel /turtle1/pose      # solo estos dos
ros2 bag record -a                                   # TODOS los tópicos activos
```

### Ver info de una grabación

```bash
ros2 bag info <nombre_de_la_carpeta_del_bag>
```

Te dice: duración, cantidad de mensajes, qué tópicos y tipos contiene.

### Reproducir la grabación

Con turtlesim corriendo (y **teleop cerrado**, para no mandar comandos duplicados), en otra
terminal:

```bash
ros2 bag play <nombre_de_la_carpeta_del_bag>
```

Verás a la tortuga repetir **exactamente el mismo movimiento** que grabaste, sin que nadie
esté tocando el teclado — está leyendo del bag y republicando en `/turtle1/cmd_vel`.

Puedes confirmarlo en otra terminal mientras reproduce:

```bash
ros2 topic echo /turtle1/cmd_vel
```

## Ejercicio

1. Graba 15 segundos de movimiento de la tortuga (solo `/turtle1/cmd_vel`).
2. Cierra teleop, reinicia `turtlesim_node` (para que la tortuga vuelva al centro) y reproduce
   tu grabación con `ros2 bag play`. ¿La tortuga repite el mismo camino?
3. Corre `ros2 bag info` sobre tu grabación — ¿cuántos mensajes se grabaron? ¿A qué frecuencia
   aproximada corresponde eso, según cuánto tiempo grabaste?
4. (Extra) Graba con `-a` en vez de un tópico específico, y compara con `ros2 bag info` cuántos
   tópicos distintos capturó esta vez frente a la grabación anterior.

## ✅ Cierre del módulo 04

Ya sabes: ver qué está pasando en el sistema (`rqt_console`), levantar sistemas completos con
un comando (`ros2 launch`), y grabar/reproducir datos sin depender del robot en vivo
(`ros2 bag`). Con esto termina la parte de **herramientas CLI** — de aquí en adelante,
empezamos a **escribir nuestros propios paquetes y nodos**.

➡️ Siguiente: **05 — Colcon y workspaces**
