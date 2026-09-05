# Reto 4 — Launch file completo

## Enunciado

Escribe un archivo de launch que levante **de una sola vez** el sistema del Reto 2 (sensor de
temperatura, sensor de batería, monitor), pasando parámetros configurables a cada nodo desde
el propio launch file, sin editar el código de los nodos.

## Requisitos

1. Primero, modifica los nodos del Reto 2 para que usen **parámetros** en vez de valores fijos
   (repasa módulo 06, archivo 4):
   - `sensor_temperatura`: parámetro `intervalo_publicacion` (segundos entre publicaciones,
     default `1.0`).
   - `sensor_bateria`: parámetro `nivel_inicial` (default `100.0`) y `tasa_descarga`
     (cuánto baja por ciclo, default `0.5`).
   - `monitor`: parámetro `umbral_bateria_baja` (default `20.0`) y
     `umbral_temperatura_alta` (default `30.0`).

2. Escribe `sistema_robot.launch.py` que:
   - Lance los 3 nodos.
   - Le pase a **cada uno** valores de parámetro **distintos a los defaults** (para
     comprobar que sí se están aplicando).

## Criterios de éxito

- `ros2 launch sistema_robot.launch.py` levanta los 3 nodos con un solo comando.
- `ros2 param get /sensor_bateria nivel_inicial` (u otro similar) muestra el valor que
  pusiste en el launch file, **no** el default del código.
- Puedes matar todo con un solo Ctrl+C en la terminal del launch.
- Cambias un valor en el launch file (ej. `tasa_descarga` a `5.0`) y ves que la batería baja
  mucho más rápido, sin tocar el `.py` del nodo.

## Pistas (si te trabas)

<details>
<summary>Pista 1 — sintaxis de parámetros en launch</summary>

```python
Node(
    package='tu_paquete',
    executable='tu_nodo',
    name='tu_nodo',
    parameters=[{'nombre_parametro': valor}],
    output='screen',
)
```
`parameters` recibe una **lista de diccionarios** (puedes pasar varios parámetros en un
mismo diccionario).
</summary>
</details>

<details>
<summary>Pista 2 — leer el parámetro dentro del nodo</summary>

Igual que en módulo 06/04: `self.declare_parameter('nombre', valor_default)` en `__init__`,
y `self.get_parameter('nombre').get_parameter_value().double_value` (o `.integer_value`
según el tipo) para leerlo.
</details>

<details>
<summary>Pista 3 — ¿dónde va el archivo launch?</summary>

Como en el módulo 04, no necesitas meterlo dentro de un paquete todavía — puedes correrlo
directo con `ros2 launch sistema_robot.launch.py` desde la carpeta donde lo guardes.
</details>

➡️ Siguiente: [Reto 5 — Mini-proyecto integrador](../reto-05-mini-proyecto-robot-simulado/README.md)
