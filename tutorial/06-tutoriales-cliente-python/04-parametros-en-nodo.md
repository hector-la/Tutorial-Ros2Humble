# Parámetros en una clase

Referencia oficial: [Using parameters in a class (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html).

## Teoría

Ya usaste parámetros desde la terminal (`ros2 param get/set`, módulo 03) sobre `turtlesim`.
Ahora los declaramos y leemos **dentro de tu propio nodo**.

Piezas nuevas de `rclpy`:
- `self.declare_parameter('nombre', valor_por_defecto)` — declara el parámetro y su valor
  inicial. **Obligatorio** — si no declaras un parámetro, no puedes usarlo (ni cambiarlo
  desde fuera).
- `self.get_parameter('nombre').get_parameter_value().string_value` — lee el valor actual.
  El sufijo depende del tipo: `string_value`, `integer_value`, `double_value`, `bool_value`,
  etc.

## Código (paquete `mi_primer_paquete`, nodo `nodo_parametros`)

```python
import rclpy
from rclpy.node import Node


class NodoParametros(Node):
    def __init__(self):
        super().__init__('nodo_parametros')
        self.declare_parameter('saludo', 'Hola desde un parámetro')
        self.timer = self.create_timer(1.0, self.callback_timer)

    def callback_timer(self):
        valor = self.get_parameter('saludo').get_parameter_value().string_value
        self.get_logger().info(valor)


def main(args=None):
    rclpy.init(args=args)
    nodo = NodoParametros()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()
```

El truco pedagógico aquí: el valor se **lee de nuevo en cada ciclo del timer** (no se guarda
en una variable aparte), así que si alguien cambia el parámetro mientras el nodo corre, el
próximo log ya refleja el cambio — eso es exactamente lo que vas a comprobar abajo.

## Probarlo tú mismo

```bash
cd ~/ros2humble_ws
colcon build --packages-select mi_primer_paquete
source install/setup.bash
```

### Con el valor por defecto

```bash
ros2 run mi_primer_paquete nodo_parametros
```
**Verificado**: imprime `Hola desde un parámetro` cada segundo.

### Pasando un valor distinto al arrancar

```bash
ros2 run mi_primer_paquete nodo_parametros --ros-args -p saludo:="Mensaje personalizado"
```
**Verificado**: imprime `Mensaje personalizado` desde el primer ciclo.

### Cambiándolo en caliente (nodo ya corriendo)

En una terminal, deja corriendo el nodo con el valor por defecto. En otra:
```bash
ros2 param set /nodo_parametros saludo "Cambiado en caliente"
```
**Verificado**: la salida de `ros2 param set` fue `Set parameter successful`, y el log del
nodo cambió de `Hola desde un parámetro` a `Cambiado en caliente` en el siguiente ciclo del
timer — **sin reiniciar el nodo**.

## Ejercicio

1. Reproduce los 3 casos de arriba tú mismo y confirma los mismos resultados.
2. Agrega un **segundo parámetro** (ej. `periodo_segundos`, tipo `double`) que controle cada
   cuánto se imprime el mensaje, en vez de tenerlo fijo en `1.0`. Pista: vas a necesitar leer
   ese parámetro **antes** de crear el timer, en `__init__`.
3. Prueba `ros2 param list /nodo_parametros` y `ros2 param describe /nodo_parametros saludo`
   — compara con lo que viste en el módulo 03 sobre turtlesim.

## ✅ Cierre del módulo 06

Con esto ya escribiste, compilaste y probaste, con tu propio código: un publisher/subscriber,
un service/client, interfaces (msg/srv) propias, y un nodo con parámetros configurables. Es
literalmente todo lo que necesitas para empezar a construir nodos reales de un robot.

➡️ Siguiente: **07 — Retos técnicos**
