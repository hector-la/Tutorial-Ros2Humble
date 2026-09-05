# Reto 5 — Mini-proyecto integrador: "robot" simulado con turtlesim

## Enunciado

Vas a construir un sistema de control simulado para un "robot" (usando turtlesim como
representación visual), compuesto por **3 nodos** que trabajan juntos:

- Un nodo **controlador** que mueve el robot y expone un **servicio propio** para cambiar su
  modo de operación en caliente (`avanzar`, `girar`, `detener`), con velocidades ajustables
  por **parámetro**.
- Un nodo **monitor** que vigila la posición del robot y **advierte** cuando se acerca
  demasiado a un límite (simulando un sensor de proximidad/colisión), también con un
  parámetro configurable.
- Un **launch file** que levanta los 3 nodos (turtlesim + controlador + monitor) de una sola
  vez, configurando cada uno con parámetros distintos a sus valores por defecto.

El objetivo es que este único proyecto combine, de punta a punta, **todo lo que viste en los
módulos 03 a 06**: nodos, tópicos, servicios, interfaces custom, parámetros, colcon/workspace
y `ros2 launch`.

A diferencia de los retos 1-4, **este sí viene con código completo**, porque es el cierre de
todo el tutorial. Aun así:

> 🎯 **En cada paso, primero intenta escribirlo tú solo** con lo que ya sabes de los módulos
> 03-06. Solo mira el código dado si te trabaste o para comparar tu solución después. Copiar
> sin haber intentado te va a servir mucho menos que forzarte a pensarlo primero.

**Todo lo de esta guía ya lo construí, compilé y probé** en este workspace — los outputs que
ves abajo son reales, no inventados.

## Qué vamos a construir

Un sistema de 3 nodos que trata a **turtlesim como si fuera un robot móvil real**:

- **`turtlesim_node`** — el "robot" (ya lo conoces).
- **`controlador_tortuga`** — controla el movimiento del robot. Tiene un **servicio propio**
  `/cambiar_modo` para cambiar entre `avanzar`, `girar` y `detener` en caliente, y
  **parámetros** para configurar las velocidades.
- **`monitor_pose`** — se suscribe a la posición del robot y **advierte** cuando se acerca
  demasiado al borde (como un sensor de proximidad simplificado).

Todo se levanta con **un solo launch file**.

---

## Paso 1 — El servicio propio: `CambiarModo.srv`

**Intenta tú primero**: ¿qué campos necesitarías para pedir "cambia el robot a este modo" y
recibir de vuelta si funcionó o no? (Repasa módulo 06, archivo 3.)

<details>
<summary>Ver solución</summary>

Paquete `reto_final_interfaces` (`ament_cmake`), archivo `srv/CambiarModo.srv`:

```
string modo
---
bool exito
string mensaje
```

`CMakeLists.txt` (después de `find_package(ament_cmake REQUIRED)`):
```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/CambiarModo.srv"
)
```

`package.xml` (después de `<buildtool_depend>ament_cmake</buildtool_depend>`):
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```
</details>

---

## Paso 2 — El controlador

**Intenta tú primero**: un nodo que publique `Twist` en `/turtle1/cmd_vel` según un "modo"
interno (empezando en `detener`), con un servicio que cambie ese modo, y con **parámetros**
para las velocidades (repasa módulos 06.1, 06.2 y 06.4).

<details>
<summary>Ver solución</summary>

Paquete `reto_final_robot` (`ament_python`, dependencias `rclpy geometry_msgs turtlesim
reto_final_interfaces`), archivo `controlador_tortuga.py`:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from reto_final_interfaces.srv import CambiarModo

MODOS_VALIDOS = ('avanzar', 'girar', 'detener')


class ControladorTortuga(Node):
    def __init__(self):
        super().__init__('controlador_tortuga')

        self.declare_parameter('velocidad_lineal', 2.0)
        self.declare_parameter('velocidad_angular', 1.0)

        self.modo = 'detener'
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.srv = self.create_service(CambiarModo, 'cambiar_modo', self.callback_cambiar_modo)
        self.timer = self.create_timer(0.2, self.callback_timer)

        self.get_logger().info('Controlador listo. Modo inicial: detener')

    def callback_cambiar_modo(self, request, response):
        if request.modo not in MODOS_VALIDOS:
            response.exito = False
            response.mensaje = f'Modo inválido. Usa uno de: {MODOS_VALIDOS}'
            return response

        self.modo = request.modo
        response.exito = True
        response.mensaje = f'Modo cambiado a: {self.modo}'
        self.get_logger().info(response.mensaje)
        return response

    def callback_timer(self):
        vel_lineal = self.get_parameter('velocidad_lineal').get_parameter_value().double_value
        vel_angular = self.get_parameter('velocidad_angular').get_parameter_value().double_value

        msg = Twist()
        if self.modo == 'avanzar':
            msg.linear.x = vel_lineal
        elif self.modo == 'girar':
            msg.angular.z = vel_angular
        # 'detener' deja msg en 0.0 en todos los campos (valor por defecto)

        self.publisher_.publish(msg)
```

Puntos clave: el `callback_cambiar_modo` **valida** el modo antes de aceptarlo (igual que
pediste hacer en el Reto 3), y `callback_timer` lee los parámetros **en cada ciclo**, así que
si los cambias en caliente con `ros2 param set`, se aplican de inmediato.
</details>

---

## Paso 3 — El monitor de posición

**Intenta tú primero**: un nodo suscrito a `/turtle1/pose` (`turtlesim/msg/Pose`) que
advierta cuando `x` o `y` estén cerca de los bordes de la ventana (turtlesim usa una ventana
de aprox. 11×11), con un parámetro `margen` configurable (repasa módulo 06.4).

<details>
<summary>Ver solución</summary>

`monitor_pose.py`:

```python
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

LIMITE_VENTANA = 11.0  # turtlesim usa una ventana ~11x11


class MonitorPose(Node):
    def __init__(self):
        super().__init__('monitor_pose')
        self.declare_parameter('margen', 1.0)
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.callback_pose, 10)

    def callback_pose(self, msg):
        margen = self.get_parameter('margen').get_parameter_value().double_value
        cerca_del_borde = (
            msg.x < margen or msg.x > (LIMITE_VENTANA - margen) or
            msg.y < margen or msg.y > (LIMITE_VENTANA - margen)
        )
        if cerca_del_borde:
            self.get_logger().warn(
                f'¡Tortuga cerca del borde! x={msg.x:.2f}, y={msg.y:.2f}')
```
</details>

No olvides agregar ambos nodos a `entry_points` en `setup.py`:
```python
entry_points={
    'console_scripts': [
        'controlador_tortuga = reto_final_robot.controlador_tortuga:main',
        'monitor_pose = reto_final_robot.monitor_pose:main',
    ],
},
```

---

## Paso 4 — El launch file

**Intenta tú primero**: un launch que levante los 3 nodos, pasándole al controlador
velocidades distintas a los defaults, y al monitor un margen distinto (repasa módulo 06.4 y
el Reto 4).

<details>
<summary>Ver solución</summary>

[`ejemplo/sistema_robot_tortuga.launch.py`](ejemplo/sistema_robot_tortuga.launch.py):

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            output='screen',
        ),
        Node(
            package='reto_final_robot',
            executable='controlador_tortuga',
            name='controlador_tortuga',
            parameters=[{
                'velocidad_lineal': 3.0,
                'velocidad_angular': 1.5,
            }],
            output='screen',
        ),
        Node(
            package='reto_final_robot',
            executable='monitor_pose',
            name='monitor_pose',
            parameters=[{'margen': 1.5}],
            output='screen',
        ),
    ])
```
</details>

---

## Compilar y probar todo el sistema (verificado)

```bash
cd ~/ros2humble_ws
colcon build --packages-select reto_final_interfaces reto_final_robot
source install/setup.bash
```

```bash
cd ~/ros2humble_ws/tutorial/07-retos/reto-05-mini-proyecto-robot-simulado/ejemplo
ros2 launch sistema_robot_tortuga.launch.py
```

En otra terminal, con el sistema corriendo:

```bash
ros2 node list
```
```
/controlador_tortuga
/monitor_pose
/turtlesim_node
```

```bash
ros2 param get /controlador_tortuga velocidad_lineal
```
```
Double value is: 3.0
```
(Confirma que el valor viene del launch file, no del default `2.0` del código.)

```bash
ros2 service call /cambiar_modo reto_final_interfaces/srv/CambiarModo "{modo: 'avanzar'}"
```
```
response:
reto_final_interfaces.srv.CambiarModo_Response(exito=True, mensaje='Modo cambiado a: avanzar')
```

La tortuga empieza a moverse. Cuando se acerca al borde de la ventana, en la terminal del
launch aparecen automáticamente warnings del monitor:
```
[monitor_pose-3] [WARN] [...] [monitor_pose]: ¡Tortuga cerca del borde! x=9.86, y=5.54
```

Prueba también un modo inválido:
```bash
ros2 service call /cambiar_modo reto_final_interfaces/srv/CambiarModo "{modo: 'volar'}"
```
```
response:
reto_final_interfaces.srv.CambiarModo_Response(exito=False, mensaje="Modo inválido. Usa uno de: ('avanzar', 'girar', 'detener')")
```
El sistema no se cae — sigue funcionando igual después.

Y para detenerla:
```bash
ros2 service call /cambiar_modo reto_final_interfaces/srv/CambiarModo "{modo: 'detener'}"
```

## Qué integraste en este reto

- **Nodos** (módulo 03.1) — 3 nodos trabajando juntos
- **Tópicos** (módulo 03.2 / 06.1) — `/turtle1/cmd_vel` (publisher) y `/turtle1/pose`
  (subscriber), ambos tópicos **reales de turtlesim**, no inventados
- **Servicios + interfaces custom** (módulo 03.3 / 06.2 / 06.3) — `/cambiar_modo` con
  validación de errores
- **Parámetros** (módulo 03.4 / 06.4) — configurables desde el launch file
- **colcon y workspaces** (módulo 05) — dos paquetes (`ament_cmake` + `ament_python`)
  compilando juntos
- **`ros2 launch`** (módulo 04.2) — todo el sistema con un solo comando

## Para ir más allá (opcional)

- Agrega un cuarto modo, `"cuadrado"`, que haga que la tortuga dibuje un cuadrado (vas a
  necesitar guardar un pequeño estado interno de tiempo/pasos en el controlador).
- Haz que `monitor_pose`, en vez de solo advertir, **llame automáticamente** al servicio
  `/cambiar_modo` con `"detener"` cuando la tortuga esté muy cerca del borde — ahora tienes
  un nodo que es cliente Y el otro es servidor, comunicándose sin intervención tuya. Esto es,
  en esencia, cómo funciona un sistema real de evasión de obstáculos.

---

## 📓 Documenta tu progreso en tu propio repositorio

Este reto no termina cuando el código corre — parte de la entrega es **documentar cómo lo
hiciste**, como harías en un proyecto real de robótica. Antes de empezar:

1. Crea un repositorio propio en GitHub (ej. `tu-usuario/reto-robot-turtlesim`), separado de
   este tutorial.
2. Ve documentando tu avance **a medida que trabajas**, no todo al final. Por cada paso (1 a
   4), como mínimo:
   - Un commit con tu código de ese paso, con un mensaje descriptivo (ej.
     `feat: servicio CambiarModo con validación de modos`).
   - Una sección en el `README.md` de tu repo explicando **qué intentaste primero**, en qué
     te trabaste (si te trabaste), y cómo lo resolviste — no solo "aquí está el código".
3. Al final, tu `README.md` debe tener, como mínimo:
   - Cómo compilar y correr tu proyecto desde cero (`colcon build`, `ros2 launch`, etc.).
   - Un GIF o screenshots de la tortuga funcionando (moviéndose, cambiando de modo,
     advertencia de borde).
   - Qué agregaste extra si hiciste la sección "Para ir más allá".

Esto tiene dos propósitos: te obliga a explicar tu propio razonamiento (que es donde
realmente se fija el aprendizaje), y queda como evidencia de tu trabajo — algo que puedes
mostrar después dentro del club o en tu portafolio.

> 💡 Si quieres, cuando termines me pasas el link del repo y lo revisamos juntos.

---

🎉 **Con esto termina el tutorial completo de ROS2 Humble.** Repasa el
[README principal](../../../README.md) si quieres revisar el roadmap completo.
