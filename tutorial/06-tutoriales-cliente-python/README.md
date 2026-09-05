# 06 — Tutoriales cliente (Python)

Basado en la sección **Beginner: Client Libraries** de la
[documentación oficial](https://docs.ros.org/en/humble/Tutorials.html), específicamente:
[Writing a simple publisher and subscriber (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html),
[Writing a simple service and client (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html),
[Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html) y
[Using parameters in a class (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html).

Este es el módulo más importante del tutorial: aquí escribes nodos reales que hacen las 4
cosas que viste en teoría en el módulo 03 (tópicos, servicios, interfaces, parámetros), pero
ahora en código propio, no solo con `ros2 topic pub` desde la terminal.

**Todos los paquetes y nodos de este módulo ya existen en `src/`, y ya los compilé y corrí
para verificar que funcionan antes de documentarlos.** Tú vas a volver a correrlos y también
modificarlos en los ejercicios.

| # | Tema | Paquete | Nodos |
|---|------|---------|-------|
| 1 | [Publisher / Subscriber](01-publisher-subscriber.md) | `ejemplos_pubsub` | `talker`, `listener` |
| 2 | [Service / Client](02-service-client.md) | `ejemplos_srv` | `servidor_suma`, `cliente_suma` |
| 3 | [Mensajes y servicios propios](03-mensajes-servicios-custom.md) | `ejemplos_interfaces` + `ejemplos_uso_custom` | `publicador_sensor`, `servidor_suma3` |
| 4 | [Parámetros en una clase](04-parametros-en-nodo.md) | `mi_primer_paquete` | `nodo_parametros` |

Antes de cada archivo, recuerda compilar y sourcear si es la primera vez:

```bash
cd ~/ros2humble_ws
colcon build
source install/setup.bash
```
