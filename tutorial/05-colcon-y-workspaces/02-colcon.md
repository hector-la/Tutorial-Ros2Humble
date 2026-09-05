# colcon en detalle

Referencia oficial: [Using colcon to build packages](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html).

## Teoría

**`colcon`** ("collective construction") es la herramienta de build oficial de ROS2. Su
trabajo es: mirar todo lo que hay en `src/`, entender de qué tipo es cada paquete
(Python o C++/CMake), compilarlo/prepararlo, e instalarlo en `install/`.

Soporta dos tipos de paquete principales (ya los verás en el siguiente archivo):
- **`ament_python`** — paquetes en Python puro (lo que usaremos en este tutorial)
- **`ament_cmake`** — paquetes en C++ (compilados con CMake)

`colcon` compila **todos los paquetes de `src/` en el orden correcto** según sus dependencias
declaradas (si el paquete B depende del A, compila A primero).

## Comandos que vas a usar seguido

Siempre desde la **raíz del workspace** (`~/ros2humble_ws`):

```bash
colcon build                              # compila TODOS los paquetes de src/
colcon build --packages-select <nombre>   # compila solo un paquete específico (más rápido)
colcon build --symlink-install            # usa symlinks en vez de copiar archivos Python
```

### `--symlink-install`

Sin esta bandera, cada vez que edites un archivo `.py` de tu nodo, tienes que volver a hacer
`colcon build` para que el cambio se refleje en `install/`. Con `--symlink-install`, los
archivos Python quedan **enlazados** (symlink) en vez de copiados, así que editas el `.py` en
`src/` y el cambio se ve inmediato sin recompilar. Se usa casi siempre mientras desarrollas:

```bash
colcon build --symlink-install
```

### Ver errores de compilación

Si algo falla, `colcon build` te muestra el error en la terminal, y además lo guarda en:

```bash
cat log/latest_build/<paquete>/stdout_stderr.log
```

## Ejemplo práctico

Ya compilaste algo en este workspace en el archivo anterior (o lo harás en el siguiente).
Prueba ahora mismo:

```bash
cd ~/ros2humble_ws
colcon build --packages-select mi_primer_paquete --symlink-install
```

Debería terminar con `Summary: 1 package finished`. Si te da error de que el paquete no
existe todavía, sigue primero al archivo 3 y vuelve aquí.

## Ejercicio

1. Corre `colcon build` sin `--packages-select` (compila todo `src/`) y observa cuánto tarda.
2. Vuelve a correrlo inmediatamente después, sin cambiar nada — ¿tarda lo mismo o menos?
   (colcon detecta qué no cambió y no lo vuelve a compilar).
3. Revisa `ls log/` — ¿qué información guarda ahí cada build?

➡️ Siguiente: [Crear tu primer paquete](03-crear-paquete.md)
