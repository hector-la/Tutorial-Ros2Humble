# 03 — Conceptos básicos

Basado en la sección **Beginner: CLI Tools** de los
[tutoriales oficiales](https://docs.ros.org/en/humble/Tutorials.html) y en
[Concepts](https://docs.ros.org/en/humble/Concepts.html) (Basic).

Cada archivo tiene **teoría + un ejemplo práctico** usando `turtlesim` (ya instalado desde el
módulo 02) — todavía no escribimos código propio, eso empieza en el módulo 06. Aquí el
objetivo es entender **qué es cada pieza del sistema** usando la terminal para explorarlas.

Orden recomendado (cada uno se apoya en el anterior):

1. [Nodos](01-nodos.md)
2. [Tópicos](02-topicos.md)
3. [Servicios](03-servicios.md)
4. [Parámetros](04-parametros.md)
5. [Acciones](05-acciones.md)
6. [Interfaces (msg / srv / action)](06-interfaces.md)

## Antes de empezar

Vas a necesitar turtlesim corriendo en varias terminales. Abre **tres terminales** desde ya:

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtlesim turtle_teleop_key

# Terminal 3 (para los comandos ros2 <algo> de este módulo)
```

(Como vimos en el módulo 02, no importa desde qué carpeta abras estas terminales.)
