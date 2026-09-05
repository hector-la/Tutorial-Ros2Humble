# Tutorial ROS2 Humble — Desde Cero

Tutorial completo de **ROS2 Humble Hawksbill** sobre **Ubuntu 22.04 LTS**, basado en la
[documentación oficial de ROS2](https://docs.ros.org/en/humble/index.html). Combina teoría
con ejercicios prácticos y retos técnicos, todo ejecutado dentro de este mismo workspace
(`ros2humble_ws`).

> 💡 Este repo **es a la vez** un workspace de ROS2 (carpeta `src/`) y un curso (carpeta
> `tutorial/`). Cuando crees tu propio workspace más adelante, la convención de nombre
> `<algo>_ws` con una carpeta `src/` dentro es el estándar que usa toda la comunidad ROS2.

## Estado de este entorno

- ROS2 Humble Desktop instalado (`ros-humble-desktop`)
- Ubuntu 22.04.5 LTS
- Lenguaje de los ejercicios: **Python (`rclpy`)**

## Roadmap

| # | Módulo | Contenido |
|---|--------|-----------|
| 00 | [Prerrequisitos](tutorial/00-prerequisitos/README.md) | Qué necesitas saber antes de empezar (incluye guía de instalación de Ubuntu 22.04 si no la tienes) |
| 01 | [Instalación](tutorial/01-instalacion/README.md) | Qué es ROS2, distros, instalación por apt paso a paso, variables de entorno (`ROS_DISTRO`, `ROS_DOMAIN_ID`, etc.) |
| 02 | [Entorno, turtlesim y rqt](tutorial/02-entorno-turtlesim-rqt/README.md) | Configurar el entorno, primer contacto con `ros2`, `turtlesim`, `rqt` |
| 03 | [Conceptos básicos](tutorial/03-conceptos-basicos/README.md) | Nodos, tópicos, servicios, parámetros, acciones, interfaces (teoría + ejemplo con turtlesim) |
| 04 | [Herramientas CLI](tutorial/04-herramientas-cli/README.md) | `rqt_console`, `ros2 launch`, `ros2 bag` |
| 05 | [Colcon y workspaces](tutorial/05-colcon-y-workspaces/README.md) | Qué es un workspace, overlay/underlay, `colcon build`, crear tu primer paquete |
| 06 | [Tutoriales cliente (Python)](tutorial/06-tutoriales-cliente-python/README.md) | Publisher/Subscriber, Service/Client, mensajes e interfaces custom, parámetros en una clase — con código real probado |
| 07 | [Retos técnicos](tutorial/07-retos/README.md) | 4 retos sin solución dada + 1 mini-proyecto integrador guiado con código |

✅ Los 8 módulos (00-07) ya están completos.

## Cómo usar este tutorial

1. Sigue los módulos **en orden**, cada uno construye sobre el anterior (igual que la doc oficial).
2. Cada carpeta de módulo tiene un `README.md` con teoría y, cuando aplica, comandos a ejecutar.
3. Los ejercicios y retos crean paquetes reales dentro de `src/`, que compilamos con `colcon build`.
4. Verifica siempre el resultado antes de pasar al siguiente paso — cada módulo indica cómo comprobar que "funcionó".

## Referencias oficiales

- [About ROS 2](https://docs.ros.org/en/humble/About-ROS.html)
- [Installation (Ubuntu, Debians)](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
- [Concepts](https://docs.ros.org/en/humble/Concepts.html)
- [Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [Citations](https://docs.ros.org/en/humble/Citations.html)
