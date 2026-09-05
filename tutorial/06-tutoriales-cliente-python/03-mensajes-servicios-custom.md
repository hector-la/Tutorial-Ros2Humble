# Mensajes y servicios propios

Referencia oficial: [Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html).

## Teoría

Hasta ahora usamos interfaces que **ya vienen con ROS2** (`std_msgs/String`,
`example_interfaces/AddTwoInts`). Pero en un proyecto real, casi siempre necesitas definir
**tus propios** tipos de mensaje/servicio (ej. el estado específico de tu robot, con campos
que nadie más definió).

### ⚠️ Detalle importante: el paquete de interfaces debe ser `ament_cmake`, no `ament_python`

Aunque tus **nodos** estén en Python, el paquete que **define** interfaces custom (`.msg` /
`.srv`) tiene que crearse con `--build-type ament_cmake`. Esto es así incluso si nunca vas a
escribir C++ — es una limitación/convención del generador de interfaces de ROS2
(`rosidl`), que la documentación oficial también sigue. Por eso, en este tutorial, separamos
las interfaces custom en su **propio paquete** (`ejemplos_interfaces`), distinto del paquete
donde están los nodos que las usan (`ejemplos_uso_custom`) — es el patrón recomendado.

## Paso 1 — Crear el paquete de interfaces

```bash
cd ~/ros2humble_ws/src
ros2 pkg create --build-type ament_cmake ejemplos_interfaces
mkdir ejemplos_interfaces/msg ejemplos_interfaces/srv
```

### Definir un mensaje propio: `msg/Sensor.msg`

```
string nombre
float64 valor
bool activo
```

Un archivo `.msg` es solo una lista de `tipo nombre_del_campo`, una por línea — nada de
lógica.

### Definir un servicio propio: `srv/SumarTresEnteros.srv`

```
int64 a
int64 b
int64 c
---
int64 suma
```

Igual que antes: arriba de `---` es la petición, abajo la respuesta.

### Configurar `CMakeLists.txt`

Hay que decirle al build system que genere código a partir de esos archivos. Se agrega esto
**después** de `find_package(ament_cmake REQUIRED)`:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Sensor.msg"
  "srv/SumarTresEnteros.srv"
)
```

### Configurar `package.xml`

Se agregan estas líneas (después de `<buildtool_depend>ament_cmake</buildtool_depend>`):

```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

### Compilar

```bash
cd ~/ros2humble_ws
colcon build --packages-select ejemplos_interfaces
source install/setup.bash
```

### Verificar que se generaron bien

```bash
ros2 interface show ejemplos_interfaces/msg/Sensor
ros2 interface show ejemplos_interfaces/srv/SumarTresEnteros
```

**Verificado**: ambos comandos devuelven exactamente los campos que definiste — ROS2 ya
reconoce tus interfaces igual que reconoce `std_msgs` o `example_interfaces`.

## Paso 2 — Usar las interfaces propias en un nodo

Creamos un paquete nuevo que **depende** de `ejemplos_interfaces`:

```bash
cd ~/ros2humble_ws/src
ros2 pkg create --build-type ament_python ejemplos_uso_custom --dependencies rclpy ejemplos_interfaces
```

**`publicador_sensor.py`** — publica lecturas simuladas usando `Sensor.msg`:

```python
import random
import rclpy
from rclpy.node import Node
from ejemplos_interfaces.msg import Sensor


class PublicadorSensor(Node):
    def __init__(self):
        super().__init__('publicador_sensor')
        self.publisher_ = self.create_publisher(Sensor, 'datos_sensor', 10)
        self.timer = self.create_timer(1.0, self.callback_timer)

    def callback_timer(self):
        msg = Sensor()
        msg.nombre = 'temperatura_1'
        msg.valor = round(random.uniform(18.0, 30.0), 2)
        msg.activo = True
        self.publisher_.publish(msg)
        self.get_logger().info(f'{msg.nombre} = {msg.valor} (activo={msg.activo})')
```

**`servidor_suma3.py`** — servicio usando `SumarTresEnteros.srv`:

```python
import rclpy
from rclpy.node import Node
from ejemplos_interfaces.srv import SumarTresEnteros


class ServidorSuma3(Node):
    def __init__(self):
        super().__init__('servidor_suma3')
        self.srv = self.create_service(
            SumarTresEnteros, 'sumar_tres_enteros', self.callback_sumar)

    def callback_sumar(self, request, response):
        response.suma = request.a + request.b + request.c
        self.get_logger().info(
            f'Petición: {request.a} + {request.b} + {request.c} = {response.suma}')
        return response
```

Nota que el `import` es idéntico al patrón que ya conocías
(`from ejemplos_interfaces.msg import Sensor`, `from ejemplos_interfaces.srv import
SumarTresEnteros`) — para tu código, una interfaz propia se usa exactamente igual que una de
ROS2.

## Probarlo tú mismo

```bash
cd ~/ros2humble_ws
colcon build --packages-select ejemplos_interfaces ejemplos_uso_custom
source install/setup.bash
```

```bash
ros2 run ejemplos_uso_custom publicador_sensor
```
**Verificado**: `temperatura_1 = 21.51 (activo=True)`, un valor nuevo cada segundo.

En otra terminal:
```bash
ros2 run ejemplos_uso_custom servidor_suma3
```
Y en una tercera:
```bash
ros2 service call /sumar_tres_enteros ejemplos_interfaces/srv/SumarTresEnteros "{a: 1, b: 2, c: 3}"
```
**Verificado**: responde `suma=6`.

## Ejercicio

1. Agrega un campo nuevo a `Sensor.msg` (ej. `string unidad`, para "°C"). Recompila
   `ejemplos_interfaces` **y** `ejemplos_uso_custom`, actualiza `publicador_sensor.py` para
   llenar ese campo, y confirma con `ros2 topic echo /datos_sensor`.
2. Crea tu propio `.srv` (ej. `MultiplicarDosEnteros.srv`) y un nodo servidor para él, desde
   cero, sin mirar la guía.
3. ¿Por qué crees que ROS2 obliga a separar las interfaces en su propio paquete `ament_cmake`
   en vez de dejarte definirlas directo en tu paquete Python? (Pista: piensa en que C++ y
   Python necesitan poder usar la *misma* interfaz.)

➡️ Siguiente: [Parámetros en una clase](04-parametros-en-nodo.md)
