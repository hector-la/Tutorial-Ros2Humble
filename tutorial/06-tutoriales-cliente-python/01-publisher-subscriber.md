# Publisher / Subscriber (Python)

Referencia oficial: [Writing a simple publisher and subscriber](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html).

## Teoría

Ya viste el patrón publish/subscribe desde la terminal (módulo 03). Ahora lo escribimos en
código: un nodo **talker** publica mensajes `String` cada cierto tiempo, y un nodo
**listener** los recibe y los imprime.

Piezas nuevas de `rclpy` que vas a usar:
- `self.create_publisher(TipoDeMensaje, 'nombre_topico', profundidad_cola)` — crea un
  publicador. La "profundidad de cola" (queue size, normalmente `10`) es cuántos mensajes
  guarda en buffer si el suscriptor no alcanza a leerlos todos a tiempo.
- `self.create_timer(periodo_segundos, callback)` — ejecuta una función repetidamente cada
  cierto tiempo. Así es como un publisher "envía algo cada X segundos" sin bloquear el nodo.
- `self.create_subscription(TipoDeMensaje, 'nombre_topico', callback, profundidad_cola)` —
  crea un suscriptor: cada vez que llega un mensaje nuevo, ROS2 llama a `callback` con ese
  mensaje.
- `rclpy.spin(nodo)` — mantiene el nodo "vivo", procesando callbacks (timers, mensajes
  entrantes) indefinidamente hasta que lo detengas con Ctrl+C.

## Código (paquete `ejemplos_pubsub`)

**`talker.py`**:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(String, 'saludo', 10)
        self.contador = 0
        self.timer = self.create_timer(0.5, self.callback_timer)  # publica a 2 Hz

    def callback_timer(self):
        msg = String()
        msg.data = f'Hola desde ROS2, mensaje #{self.contador}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: "{msg.data}"')
        self.contador += 1


def main(args=None):
    rclpy.init(args=args)
    nodo = Talker()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()
```

**`listener.py`**:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String, 'saludo', self.callback_saludo, 10)

    def callback_saludo(self, msg):
        self.get_logger().info(f'Escuché: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    nodo = Listener()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()
```

Y en `setup.py`, cada nodo se registra como ejecutable en `entry_points`:

```python
entry_points={
    'console_scripts': [
        'talker = ejemplos_pubsub.talker:main',
        'listener = ejemplos_pubsub.listener:main',
    ],
},
```

## Probarlo tú mismo

```bash
cd ~/ros2humble_ws
colcon build --packages-select ejemplos_pubsub
source install/setup.bash
```

En una terminal:
```bash
ros2 run ejemplos_pubsub talker
```

En otra terminal:
```bash
ros2 run ejemplos_pubsub listener
```

Deberías ver al talker publicando `"Hola desde ROS2, mensaje #N"` y al listener recibiendo
exactamente esos mismos mensajes (**verificado**: así se comportó al probarlo).

En una tercera terminal, confirma con las herramientas del módulo 03:
```bash
ros2 topic list
ros2 topic echo /saludo
ros2 node info /talker
```

## Ejercicio

1. Cambia el período del timer de `talker.py` (de `0.5` a `2.0`) y recompila
   (`colcon build --packages-select ejemplos_pubsub`). ¿A qué frecuencia publica ahora?
2. Agrega un **segundo** listener corriendo al mismo tiempo que el primero (misma terminal
   distinta instancia). ¿Reciben ambos los mismos mensajes? (Sí — recuerda: tópicos son
   muchos-a-muchos).
3. Modifica `listener.py` para que solo imprima los mensajes con número **par** (pista:
   puedes extraer el número del string, o mejor, cambia el mensaje para publicar un `Int32`
   en vez de un `String` — más limpio, aunque requiere más cambios).

➡️ Siguiente: [Service / Client](02-service-client.md)
