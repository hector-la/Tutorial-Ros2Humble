# 02 — Entorno, turtlesim y rqt

Basado en los tutoriales oficiales
[Configuring your ROS 2 Environment](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment/Configuring-ROS2-Environment.html)
y [Turtlesim, ros2, and rqt](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html).

> 🖐️ Este módulo es **manos a la obra**: los comandos los corres tú en tu terminal. Ve
> paso a paso, no copies todo de una — la idea es que veas qué hace cada cosa.

---

## ❓ ¿Desde qué carpeta ejecuto estos comandos?

Duda típica de principiante: **no importa**. Puedes ejecutar `ros2 run turtlesim
turtlesim_node` desde tu carpeta personal (`~`), desde el Desktop, desde donde sea.

¿Por qué? Porque `turtlesim` es un paquete **instalado con `apt`** — ya viene compilado en
`/opt/ros/humble/`. Cuando haces `source /opt/ros/humble/setup.bash` (módulo 01), ROS2 guarda
en variables de entorno (como `AMENT_PREFIX_PATH`) **dónde** están todos los paquetes
instalados. El comando `ros2 run` busca ahí, no en tu carpeta actual.

La carpeta **sí** importa a partir del módulo 05, cuando empecemos a **crear nuestros propios
paquetes** dentro de `~/ros2humble_ws/src/` y a compilarlos con `colcon build` — ahí sí hay
que estar parado en la raíz del workspace (`~/ros2humble_ws`) para compilar. Pero eso es
código nuestro, no turtlesim.

**Regla mental para todo este tutorial:**
- ¿Es un paquete que instalaste con `apt` (turtlesim, rqt, demos)? → Ejecuta desde donde sea.
- ¿Es un paquete que **creamos nosotros** en `src/`? → Compílalo desde la raíz del workspace
  (`~/ros2humble_ws`) y luego sí puedes ejecutarlo desde donde sea (una vez compilado y
  "sourceado").

---

## Parte 1 — Repaso rápido del entorno

Ya vimos en el módulo 01 que hay que hacer `source` y que existen variables como
`ROS_DISTRO` o `ROS_DOMAIN_ID`. Dos utilidades extra que trae el entorno de ROS2:

### `colcon_cd` (opcional pero útil)

Te permite saltar directo a la carpeta de un paquete ROS2 por su nombre, sin importar dónde
esté instalado:

```bash
echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
echo "export _colcon_cd_root=/opt/ros/humble/" >> ~/.bashrc
source ~/.bashrc
```

Luego puedes hacer, por ejemplo: `colcon_cd turtlesim` y te lleva a esa carpeta.

### Autocompletado con tab

Al escribir `ros2 <TAB><TAB>` en la terminal, deberías ver sugerencias de subcomandos
(`node`, `topic`, `run`, `launch`, etc.). Si no te autocompleta, instala:

```bash
sudo apt install python3-argcomplete
```

y reinicia la terminal.

---

## Parte 2 — Instalar y correr turtlesim

**Turtlesim** es un simulador simple (una tortuga en una ventana 2D) que ROS2 usa para enseñar
sus conceptos sin necesitar un robot real.

### Instalar

```bash
sudo apt install ros-humble-turtlesim
```

### Verificar que se instaló

```bash
ros2 pkg executables turtlesim
```

Deberías ver ejecutables como `turtlesim_node` y `turtle_teleop_key`.

### Ejecutarlo

En una terminal:

```bash
ros2 run turtlesim turtlesim_node
```

Se abre una ventana con una tortuga en el centro. **`ros2 run <paquete> <ejecutable>`** es el
comando base para correr un solo nodo de ROS2.

### Moverla con el teclado

Abre **otra terminal** (deja la primera corriendo) y ejecuta:

```bash
ros2 run turtlesim turtle_teleop_key
```

Con esa terminal en foco, usa las flechas del teclado para mover la tortuga. Cada tecla envía
comandos de velocidad al nodo `turtlesim_node` — estás viendo dos nodos **comunicándose por
un tópico**, aunque todavía no hablemos de tópicos formalmente (eso es el módulo 03).

### 🐢 Ejercicio 1

Con turtlesim y teleop corriendo:
1. Mueve la tortuga hasta un borde de la ventana. ¿Qué pasa?
2. Abre una tercera terminal y corre `ros2 node list`. ¿Qué nombres de nodos ves?

---

## Parte 3 — Explorar con comandos `ros2`

Con turtlesim y teleop todavía corriendo, abre una tercera terminal y prueba:

```bash
ros2 node list          # lista de nodos activos
ros2 topic list         # lista de tópicos activos
ros2 topic echo /turtle1/cmd_vel   # ve en vivo los comandos de velocidad (mueve la tortuga con teleop para verlo)
```

No te preocupes si no entiendes todo el output todavía — el módulo 03 explica nodos y
tópicos en detalle. Aquí solo estamos "tocando" la herramienta.

Para remapear el nombre de un nodo al ejecutarlo (útil si quieres correr dos turtlesim a la
vez, por ejemplo):

```bash
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=mi_tortuga
```

---

## Parte 4 — rqt

**rqt** es una interfaz gráfica con plugins para inspeccionar y controlar un sistema ROS2 sin
escribir comandos.

### Instalar

```bash
sudo apt install '~nros-humble-rqt*'
```

(Si tu shell no soporta ese patrón con `~n`, usa: `sudo apt install ros-humble-rqt*`)

### Ejecutar

```bash
ros2 run rqt_gui rqt_gui
```

Se abre una ventana vacía. Ve al menú **Plugins → Services → Service Caller**.

### Llamar un servicio desde rqt

Con turtlesim corriendo, en el Service Caller:
1. En el dropdown de **Service**, selecciona `/spawn`
2. Rellena `x`, `y`, `theta` y un `name` (ej. `turtle2`)
3. Presiona **Call** → aparece una segunda tortuga en la ventana

Prueba también el servicio `/turtle1/set_pen` — cambia el color/grosor del trazo que deja la
tortuga al moverse.

### 🐢 Ejercicio 2

1. Desde rqt, llama a `/spawn` para crear una tortuga nueva con un nombre distinto.
2. Corre `ros2 node list` en terminal — ¿aparece un nodo nuevo?
3. Usa `/set_pen` sobre `turtle1` para cambiar el color de su trazo, luego muévela con teleop
   (necesitarás correr otro teleop apuntando a esa tortuga, o mover la original) y observa el
   cambio.

---

## ✅ Verificación del módulo

Al terminar deberías poder responder sin mirar la guía:
- ¿Qué comando corre un solo nodo de un paquete?
- ¿Qué diferencia hay entre `ros2 node list` y `ros2 topic list`?
- ¿Para qué sirve rqt frente a usar solo la terminal?

Cuando puedas cerrar todas las terminales (Ctrl+C) y volver a levantar turtlesim + teleop sin
mirar esta guía, estás listo para el siguiente módulo.

➡️ Siguiente: **03 — Conceptos básicos** (nodos, tópicos, servicios, parámetros, acciones)
