# 01 — Instalación de ROS2 Humble

> Este módulo asume que **no tienes nada instalado todavía**. Si ya tienes ROS2 Humble
> funcionando, puedes saltar directo a la sección de [Verificación](#-verificación), pero te
> recomendamos igual leer la teoría de variables de entorno, porque la vas a necesitar en
> todo el resto del tutorial.

## Teoría: ¿Qué es ROS2?

ROS2 (**Robot Operating System 2**) no es un sistema operativo: es un **framework/middleware**
de código abierto para escribir software de robótica. Provee:

- **Comunicación entre procesos** (nodos) vía tópicos, servicios y acciones, construida sobre
  DDS (**Data Distribution Service**) — a diferencia de ROS1, no necesita un "master" central:
  los nodos se descubren entre sí automáticamente en la red.
- **Herramientas** de build (`colcon`), línea de comandos (`ros2 ...`), visualización (`rqt`,
  `RViz`) y simulación.
- **Librerías cliente** para escribir nodos: `rclpy` (Python) y `rclcpp` (C++).

Referencia oficial: [About ROS 2](https://docs.ros.org/en/humble/About-ROS.html).

### ¿Por qué Humble?

Cada distribución (distro) de ROS2 tiene un nombre en orden alfabético y un ciclo de soporte
propio. **Humble Hawksbill** es una release **LTS (Long Term Support)**, con soporte oficial
sobre **Ubuntu 22.04 (Jammy Jellyfish)** hasta 2027. Por eso es la combinación recomendada
para aprender hoy, y la que usa el club.

Guía oficial de instalación por Debian/apt: [Installation (Ubuntu, Debians)](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

---

## Requisito previo

Necesitas **Ubuntu 22.04** ya instalado y arrancando. Si no lo tienes, ve primero al
[Módulo 00 — Prerrequisitos](../00-prerequisitos/README.md).

Confirma tu versión antes de continuar:

```bash
lsb_release -a
```

Debe mostrar `Release: 22.04` y `Codename: jammy`.

---

## Paso 1 — Configurar el locale (idioma/codificación)

ROS2 necesita que el sistema soporte **UTF-8**. Un *locale* define el idioma y la codificación
de caracteres que usa tu sistema (cómo interpreta tildes, símbolos, etc.). Si no está bien
configurado, algunas herramientas de ROS2 pueden fallar al mostrar texto.

Revisa tu configuración actual:

```bash
locale
```

Si no ves `UTF-8` en las variables (`LANG`, `LC_ALL`, etc.), configúralo así:

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Verifica de nuevo con `locale` — ahora debería mostrar `en_US.UTF-8` en todas las variables.

## Paso 2 — Habilitar el repositorio "universe" de Ubuntu

Ubuntu organiza sus paquetes en repositorios. `universe` contiene software mantenido por la
comunidad (no oficialmente soportado por Canonical), y ahí es donde vive parte de lo que
necesita ROS2:

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

## Paso 3 — Agregar el repositorio de ROS2 a tu sistema

Por defecto, `apt` (el gestor de paquetes de Ubuntu) solo conoce los repositorios oficiales
de Ubuntu. Para poder instalar ROS2 con `apt install`, hay que decirle a Ubuntu dónde están
los paquetes de ROS2 y darle la llave (keyring) que garantiza que esos paquetes son
auténticos (firmados por el equipo de ROS2):

```bash
sudo apt update && sudo apt install curl -y

# Descarga la llave GPG del repositorio de ROS2
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

# Registra el repositorio de ROS2 para tu versión de Ubuntu
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

`$(source /etc/os-release && echo $UBUNTU_CODENAME)` inserta automáticamente `jammy` (el
nombre en código de Ubuntu 22.04), para que el mismo comando sirva en otras versiones de Ubuntu.

## Paso 4 — Instalar ROS2 Humble

Con el repositorio ya agregado, actualiza la lista de paquetes disponibles e instala:

```bash
sudo apt update
sudo apt upgrade

sudo apt install ros-humble-desktop
```

`ros-humble-desktop` es el metapaquete "completo": incluye el core de ROS2, RViz (visualización
3D), demos y herramientas gráficas. Existe también `ros-humble-ros-base`, una versión mínima
solo con la comunicación (sin GUI) — útil para robots embebidos sin pantalla, pero para
aprender usamos `desktop`.

## Paso 5 — Herramientas de desarrollo

Además del core de ROS2, necesitas herramientas para compilar tus propios paquetes:

```bash
sudo apt install ros-dev-tools
```

Esto instala, entre otras cosas, **`colcon`** (la herramienta de build de ROS2, la vemos en
el módulo 05) y **`rosdep`** (resuelve dependencias de paquetes ROS2 automáticamente).

---

## Paso 6 — Configurar el entorno (`source`)

ROS2 **no se activa solo**: cada vez que abres una terminal nueva, tienes que decirle a esa
terminal "carga las variables y comandos de ROS2". Esto se hace con `source`, que ejecuta un
script y aplica sus variables de entorno a tu sesión actual de terminal:

```bash
source /opt/ros/humble/setup.bash
```

Si no haces esto, el comando `ros2` no existirá en tu terminal.

### Hacerlo automático

Escribir ese comando cada vez es molesto, así que se agrega al final de `~/.bashrc` (un script
que Bash ejecuta automáticamente cada vez que abres una terminal nueva):

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

A partir de ahora, **toda terminal nueva** ya tiene ROS2 cargado automáticamente.

> ⚠️ Si en algún momento instalas **otra distro de ROS2** en la misma máquina (ej. otra
> versión), solo puedes tener una "sourceada" a la vez por terminal — la última que hagas
> `source` es la que manda en esa sesión.

---

## Variables de entorno de ROS2 (explicadas)

Al hacer `source`, se configuran varias variables de entorno que ROS2 usa internamente.
Puedes verlas todas con:

```bash
printenv | grep -i ROS
```

Las más importantes, tal como las define la documentación oficial
([Configuring your ROS 2 Environment](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment/Configuring-ROS2-Environment.html)):

| Variable | Qué es |
|---|---|
| **`ROS_DISTRO`** | El nombre de la distribución de ROS2 activa en esta terminal (en nuestro caso `humble`). Todas las rutas de instalación (`/opt/ros/<ROS_DISTRO>/`) dependen de este valor. |
| **`ROS_VERSION`** | Indica si es ROS 1 o ROS 2. Para nosotros siempre vale `2`. |
| **`ROS_PYTHON_VERSION`** | Versión de Python que usan las librerías cliente de Python (`rclpy`). En Humble/Ubuntu 22.04 es `3`. |
| **`ROS_DOMAIN_ID`** | Aísla grupos de nodos ROS2 en la misma red. Todos los nodos con el mismo `ROS_DOMAIN_ID` se ven entre sí; nodos con IDs distintos **no** se ven, aunque estén en la misma red física/WiFi. Por defecto es `0`. En un salón con varias personas usando ROS2 en la misma red (como en el club), **cada quien debería usar un `ROS_DOMAIN_ID` distinto** para no interferir con los tópicos/nodos de los demás. Ejemplo: `export ROS_DOMAIN_ID=42` (valores válidos: 0-101). |
| **`RMW_IMPLEMENTATION`** | Qué implementación de DDS (el protocolo de comunicación de bajo nivel) usa ROS2. Humble trae `rmw_fastrtps_cpp` por defecto. No hace falta tocarla para este tutorial. |
| **`ROS_LOCALHOST_ONLY`** | Si la pones en `1`, restringe la comunicación de ROS2 solo a tu propia máquina (no se comunica con otros equipos en la red). Útil si estás en una red compartida y quieres aislarte por completo. |

Puedes ver el valor de una variable específica así:

```bash
printenv ROS_DISTRO
printenv ROS_DOMAIN_ID
```

> 📌 **Para el club AIRoS**: si varias personas van a correr ejemplos de ROS2 al mismo tiempo
> conectadas a la misma red WiFi, es buena práctica que cada quien fije su propio
> `ROS_DOMAIN_ID` en su `~/.bashrc` para no ver (ni interferir con) los nodos de los demás:
>
> ```bash
> echo "export ROS_DOMAIN_ID=<un número del 0 al 101, distinto al de tus compañeros>" >> ~/.bashrc
> source ~/.bashrc
> ```

---

## ✅ Verificación

Corre esto en tu terminal para confirmar que todo quedó bien instalado y configurado:

```bash
printenv ROS_DISTRO        # debe imprimir: humble
which ros2                 # debe imprimir: /opt/ros/humble/bin/ros2
ros2 pkg list | head       # debe listar paquetes de ROS2 (sin error)
```

Si los tres comandos funcionan sin error, tu instalación está lista.

## Ejercicio rápido

1. Abre una terminal **nueva** (sin escribir nada) y corre `printenv ROS_DISTRO`. ¿Te imprime
   `humble` sin que hicieras `source` manualmente? (Debería, gracias al `~/.bashrc`.)
2. Corre `printenv | grep -i ROS` y anota qué variables ves. ¿Reconoces todas de la tabla de
   arriba?
3. Corre `ros2 pkg list | wc -l` — ¿cuántos paquetes tienes instalados?

➡️ Siguiente: **02 — Entorno, turtlesim y rqt** (próximo módulo)
