# Crear tu primer paquete

Referencia oficial: [Creating your first ROS2 package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html).

## Teoría

Un **paquete** es la unidad básica de organización de código en ROS2: agrupa nodos,
librerías, mensajes propios, archivos de configuración, etc. bajo un mismo nombre y con sus
dependencias declaradas. Todo en `src/` de tu workspace son paquetes (uno o varios).

`ros2 pkg create` genera el "esqueleto" de un paquete nuevo con todos los archivos que ROS2
necesita para reconocerlo.

## Ejemplo práctico — paso a paso (ya ejecutado y verificado)

Este paquete **ya existe** en tu `src/` — lo creé y probé para escribir esta guía. Aun así,
sigue los pasos tú mismo en un paquete nuevo (con otro nombre) para practicar.

### 1. Crear el paquete

Desde `src/` del workspace:

```bash
cd ~/ros2humble_ws/src
ros2 pkg create --build-type ament_python mi_primer_paquete --node-name hola_ros2 --dependencies rclpy
```

- `--build-type ament_python`: paquete en Python.
- `--node-name hola_ros2`: genera automáticamente un archivo `hola_ros2.py` con una función
  `main()` mínima, y lo registra como ejecutable.
- `--dependencies rclpy`: declara que este paquete depende de `rclpy` (la librería cliente de
  Python para ROS2).

### 2. Estructura generada

```
mi_primer_paquete/
├── package.xml                       # metadata del paquete: nombre, dependencias, mantenedor
├── setup.py                          # cómo se instala (equivalente a package.xml pero para Python/colcon)
├── setup.cfg
├── resource/mi_primer_paquete        # archivo vacío que marca este paquete como "ament index"
├── mi_primer_paquete/
│   ├── __init__.py
│   └── hola_ros2.py                  # AQUÍ va tu código del nodo
└── test/                             # tests de estilo (flake8, pep257) que genera la plantilla
```

`package.xml` declara las dependencias (ahí verás `<depend>rclpy</depend>`). `setup.py` tiene
la sección clave `entry_points`, que le dice a ROS2 qué función correr cuando hagas
`ros2 run mi_primer_paquete hola_ros2`:

```python
entry_points={
    'console_scripts': [
        'hola_ros2 = mi_primer_paquete.hola_ros2:main'
    ],
},
```

### 3. Escribir el nodo

Reemplazamos el contenido por defecto de `hola_ros2.py` (que solo hacía un `print`) por un
nodo real de ROS2, usando `rclpy`:

```python
import rclpy
from rclpy.node import Node


class HolaRos2(Node):
    def __init__(self):
        super().__init__('hola_ros2')
        self.get_logger().info('¡Hola ROS2! Este nodo arrancó y está funcionando.')


def main(args=None):
    rclpy.init(args=args)
    nodo = HolaRos2()
    rclpy.spin_once(nodo, timeout_sec=0.5)  # deja procesar un ciclo antes de cerrar
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Puntos clave de **cualquier** nodo Python de ROS2:
- Tu clase hereda de `Node` y llama a `super().__init__('<nombre_del_nodo>')`.
- `rclpy.init()` / `rclpy.shutdown()` inician y cierran la comunicación con ROS2 — todo nodo
  los necesita.
- `self.get_logger().info(...)` es la forma correcta de "imprimir" en ROS2 (recuerda
  `rqt_console`, módulo 04) — mejor que un `print()` normal.

### 4. Compilar

```bash
cd ~/ros2humble_ws
colcon build --packages-select mi_primer_paquete
```

Salida esperada:
```
Starting >>> mi_primer_paquete
Finished <<< mi_primer_paquete [0.83s]

Summary: 1 package finished
```

### 5. Activar el overlay y ejecutar

```bash
source install/setup.bash
ros2 run mi_primer_paquete hola_ros2
```

Salida real verificada:
```
[INFO] [...] [hola_ros2]: ¡Hola ROS2! Este nodo arrancó y está funcionando.
```

🎉 Ese es tu primer nodo propio, compilado e instalado desde cero en tu workspace.

## Ejercicio

1. Crea tu **propio** paquete con otro nombre (ej. `practica_pkg`) y otro nodo (ej.
   `mi_nodo`), siguiendo los mismos 5 pasos.
2. Modifica el mensaje de log para que incluya tu nombre.
3. Corre `ros2 node list` con tu nodo corriendo — confirma que aparece.
4. Corre `ros2 pkg list | grep <tu_paquete>` — confirma que ROS2 reconoce tu paquete como
   instalado.

## ✅ Cierre del módulo 05

Ya sabes: qué es un workspace y la relación overlay/underlay, cómo compilar con `colcon`, y
cómo crear un paquete Python desde cero con un nodo funcional. Con esto tienes toda la base
para escribir nodos "de verdad" (publishers, subscribers, servicios, parámetros) en el
siguiente módulo.

➡️ Siguiente: **06 — Tutoriales cliente (Python)**
