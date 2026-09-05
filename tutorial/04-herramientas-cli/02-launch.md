# ros2 launch — levantar varios nodos a la vez

Referencia oficial: [Launching Nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html).

## Teoría

Hasta ahora hemos abierto **una terminal por nodo** (`turtlesim_node` en una, `teleop_key` en
otra...). Eso no escala: un robot real puede tener 10, 20, 50 nodos corriendo a la vez. Un
**archivo de launch** describe, en un solo lugar, **qué nodos levantar y con qué
configuración** (nombre, namespace, parámetros, remapeos), y con un solo comando los levanta
todos juntos.

En ROS2, los launch files se escriben normalmente en **Python** (también existen en XML/YAML,
pero Python es el formato recomendado por default). Un launch file define una función
`generate_launch_description()` que devuelve una `LaunchDescription` con una lista de
acciones — la más común es `Node(...)`, que describe un nodo a lanzar.

## Ejemplo práctico

Este módulo incluye un archivo ya escrito y probado:
[`ejemplos/dos_turtlesim.launch.py`](ejemplos/dos_turtlesim.launch.py), que lanza **dos**
`turtlesim_node` al mismo tiempo, cada uno en su propio **namespace** (`/tortuga1` y
`/tortuga2`) para que no choquen de nombres:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            namespace='tortuga1',
            output='screen',
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            namespace='tortuga2',
            output='screen',
        ),
    ])
```

Ejecútalo así (no necesitas un paquete todavía — `ros2 launch` acepta la ruta directa a un
archivo):

```bash
cd ~/ros2humble_ws/tutorial/04-herramientas-cli/ejemplos
ros2 launch dos_turtlesim.launch.py
```

Deberían abrirse **dos ventanas** de turtlesim. En otra terminal, confirma que hay dos
turtlesim separados:

```bash
ros2 node list
```

```
/tortuga1/turtlesim_node
/tortuga2/turtlesim_node
```

```bash
ros2 topic list
```

```
/tortuga1/turtle1/cmd_vel
/tortuga1/turtle1/pose
/tortuga2/turtle1/cmd_vel
/tortuga2/turtle1/pose
...
```

Fíjate: el **namespace** (`tortuga1`/`tortuga2`) se antepone automáticamente a todos los
tópicos/servicios/acciones de ese nodo — así evitas colisiones de nombres sin tener que
remapear cada tópico a mano.

### Mover solo una de las dos tortugas

```bash
ros2 topic pub /tortuga1/turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}}" --once
```

Solo se mueve la tortuga de `/tortuga1`, la de `/tortuga2` queda quieta.

Para detener todo (ambos nodos a la vez): `Ctrl+C` en la terminal donde corriste `ros2 launch`.

## Ejercicio

1. Ejecuta `dos_turtlesim.launch.py` y confirma con `ros2 node list` que ves los dos nodos.
2. Modifica el archivo (copia a `tres_turtlesim.launch.py`) para lanzar una **tercera**
   tortuga con su propio namespace. Vuelve a correr `ros2 launch` sobre tu nuevo archivo.
3. Investiga el parámetro `output='screen'` en la clase `Node` — quítalo y vuelve a correr.
   ¿Notas alguna diferencia en lo que se imprime en la terminal?

➡️ Siguiente: [ros2 bag](03-bag.md)
