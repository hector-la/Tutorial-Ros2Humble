# Service / Client (Python)

Referencia oficial: [Writing a simple service and client](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html).

## Teoría

Igual que con pub/sub, ya usaste servicios desde la terminal (módulo 03). Ahora los
implementamos: un nodo **servidor** ofrece el servicio, un nodo **cliente** lo llama.

Usamos `example_interfaces/srv/AddTwoInts`, un servicio **que ya viene con ROS2** (no
tenemos que crear una interfaz propia todavía — eso es el siguiente archivo). Tiene esta
forma (`ros2 interface show example_interfaces/srv/AddTwoInts`):

```
int64 a
int64 b
---
int64 sum
```

Piezas nuevas de `rclpy`:
- `self.create_service(TipoSrv, 'nombre_servicio', callback)` — crea el servidor. El
  `callback` recibe `(request, response)`, llena `response` y la retorna.
- `self.create_client(TipoSrv, 'nombre_servicio')` — crea el cliente.
- `cli.wait_for_service(timeout_sec=1.0)` — espera (en loop) a que el servidor esté
  disponible antes de intentar llamarlo.
- `cli.call_async(request)` + `rclpy.spin_until_future_complete(nodo, future)` — llama al
  servicio **sin bloquear** el nodo entero, y espera solo a que esa llamada puntual termine.

## Código (paquete `ejemplos_srv`)

**`servidor_suma.py`**:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServidorSuma(Node):
    def __init__(self):
        super().__init__('servidor_suma')
        self.srv = self.create_service(AddTwoInts, 'sumar_dos_enteros', self.callback_sumar)

    def callback_sumar(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Petición: {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    nodo = ServidorSuma()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()
```

**`cliente_suma.py`** (recibe `a` y `b` como argumentos de línea de comandos):

```python
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ClienteSuma(Node):
    def __init__(self):
        super().__init__('cliente_suma')
        self.cli = self.create_client(AddTwoInts, 'sumar_dos_enteros')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando a que el servicio esté disponible...')
        self.req = AddTwoInts.Request()

    def enviar_peticion(self, a, b):
        self.req.a = a
        self.req.b = b
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    nodo = ClienteSuma()
    respuesta = nodo.enviar_peticion(a, b)
    nodo.get_logger().info(f'Resultado: {a} + {b} = {respuesta.sum}')

    nodo.destroy_node()
    rclpy.shutdown()
```

## Probarlo tú mismo

```bash
cd ~/ros2humble_ws
colcon build --packages-select ejemplos_srv
source install/setup.bash
```

En una terminal:
```bash
ros2 run ejemplos_srv servidor_suma
```

En otra terminal:
```bash
ros2 run ejemplos_srv cliente_suma 7 5
```

**Verificado**: el servidor logueó `Petición: 7 + 5 = 12` y el cliente `Resultado: 7 + 5 = 12`.

También puedes llamarlo desde la terminal directamente, como en el módulo 03, sin usar
`cliente_suma.py`:
```bash
ros2 service call /sumar_dos_enteros example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"
```

## Ejercicio

1. Corre `servidor_suma` y llama al servicio con distintos valores usando `cliente_suma.py`
   Y también con `ros2 service call` — confirma que dan el mismo resultado.
2. Modifica `servidor_suma.py` para que en vez de sumar, **reste** `a - b`. Recompila y
   vuelve a probar.
3. ¿Qué pasa si corres `cliente_suma.py` **antes** de levantar el servidor? Fíjate en el
   mensaje "Esperando a que el servicio esté disponible..." — ¿qué línea del código produce
   eso?

➡️ Siguiente: [Mensajes y servicios propios](03-mensajes-servicios-custom.md)
