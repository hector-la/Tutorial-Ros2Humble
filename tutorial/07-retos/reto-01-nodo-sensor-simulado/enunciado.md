# Reto 1 — Nodo sensor simulado

## Enunciado

Crea un paquete y un nodo que simule un **sensor de distancia** (como un ultrasónico), que
publique una lectura nueva periódicamente.

## Requisitos

1. Crea un paquete nuevo (`ament_python`), nómbralo como quieras (ej. `reto_sensor`).
2. El nodo debe publicar en un tópico llamado `/sensor_distancia`, tipo `std_msgs/msg/Float32`.
3. Debe publicar un valor **cada 0.5 segundos**.
4. El valor debe ser aleatorio, entre `0.0` y `4.0` (simulando metros).
5. **Regla extra**: si el valor simulado es menor a `0.3`, el nodo debe loguear una
   **advertencia** (`self.get_logger().warn(...)`) diciendo algo como "¡Obstáculo muy cerca!".

## Criterios de éxito

- `colcon build --packages-select <tu_paquete>` compila sin errores.
- `ros2 run <tu_paquete> <tu_nodo>` corre y no se cae.
- `ros2 topic echo /sensor_distancia` muestra valores cambiando cada 0.5s.
- `ros2 topic list -t` muestra `/sensor_distancia` con tipo `[std_msgs/msg/Float32]`.
- Cuando el valor simulado baja de `0.3`, ves un `[WARN]` en la terminal (puedes forzarlo
  bajando temporalmente el rango aleatorio a `0.0`-`0.5` para probarlo más seguido).

## Pistas (si te trabas)

<details>
<summary>Pista 1 — estructura del paquete</summary>

Repasa el módulo 05, archivo 3 (`ros2 pkg create --build-type ament_python ...`). No olvides
agregar el ejecutable en `entry_points` de `setup.py`.
</details>

<details>
<summary>Pista 2 — publicar un Float32</summary>

```python
from std_msgs.msg import Float32
```
Revisa `ros2 interface show std_msgs/msg/Float32` para ver qué campo tiene el mensaje
(spoiler: solo tiene uno, `data`).
</details>

<details>
<summary>Pista 3 — números aleatorios</summary>

Python trae `random` en la librería estándar: `random.uniform(0.0, 4.0)`.
</details>

<details>
<summary>Pista 4 — log de advertencia</summary>

`self.get_logger().warn('mensaje')` — mismo patrón que `.info()`, distinto nivel (repasa el
módulo 04, `rqt_console`).
</details>

➡️ Siguiente: [Reto 2 — Sistema pub/sub múltiple](../reto-02-pub-sub-multiple/enunciado.md)
