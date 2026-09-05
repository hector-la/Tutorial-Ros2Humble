# Parámetros (Parameters)

Referencia oficial: [Understanding ROS 2 Parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html).

## Teoría

Un **parámetro** es un valor de configuración que pertenece a un nodo (un número, texto,
booleano, etc.). Sirven para ajustar el comportamiento de un nodo **sin tener que modificar
ni recompilar su código** — por ejemplo, la velocidad máxima de un motor, el puerto serial a
usar, o (como veremos) el color de fondo de turtlesim.

Cada nodo mantiene su propia lista de parámetros. Se pueden:
- Consultar (`get`)
- Modificar en caliente mientras el nodo corre (`set`)
- Definir valores por defecto al arrancar el nodo
- Guardar/cargar desde un archivo YAML (`dump` / `load`) — útil para tener distintas
  "configuraciones" guardadas y reusarlas

## Ejemplo práctico

Con turtlesim corriendo:

```bash
ros2 param list
```

```
/turtlesim:
  background_b
  background_g
  background_r
  ...
```

Ver el valor actual de un parámetro:

```bash
ros2 param get /turtlesim background_r
```

Cambiarlo en caliente:

```bash
ros2 param set /turtlesim background_r 150
ros2 param set /turtlesim background_g 0
ros2 param set /turtlesim background_b 150
```

Llama al servicio `/clear` (visto en el archivo anterior) para que se redibuje el fondo con
el nuevo color:

```bash
ros2 service call /clear std_srvs/srv/Empty
```

### Guardar y cargar configuración

```bash
ros2 param dump /turtlesim > ~/turtlesim_config.yaml
```

Abre ese archivo con un editor — verás todos los parámetros actuales en formato YAML. Puedes
editarlo y luego cargarlo con:

```bash
ros2 param load /turtlesim ~/turtlesim_config.yaml
```

## Ejercicio

1. Cambia los tres parámetros `background_r/g/b` para poner un color de fondo a tu gusto.
2. Haz `ros2 param dump /turtlesim > mi_config.yaml` y abre el archivo — identifica al menos
   3 parámetros que no sean de color.
3. Investiga con `ros2 param describe /turtlesim background_r` — ¿qué información extra te da
   sobre ese parámetro que no ves con `get`?

➡️ Siguiente: [Acciones](05-acciones.md)
