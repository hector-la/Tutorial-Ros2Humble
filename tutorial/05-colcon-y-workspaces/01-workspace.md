# Qué es un workspace

Referencia oficial: [Creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html).

## ⏱️ Orden real de los pasos (duda típica)

Es normal confundirse con **cuándo** se crea el workspace y **cuándo** se corre `colcon
build` — no es lo mismo momento. El orden es:

1. **Crear el workspace, una sola vez** — una carpeta con una subcarpeta `src/` vacía:
   ```bash
   mkdir -p ~/ros2humble_ws/src
   ```
   
2. **Compilar con colcon aunque `src/` esté vacío** — parece inútil, pero es el paso que
   confirma que colcon reconoce el workspace y genera `build/`, `install/`, `log/`:
   ```bash
   cd ~/ros2humble_ws
   colcon build
   ```

3. **Hacer `source` del overlay** (una vez por terminal nueva, de aquí en adelante):
   ```bash
   source ~/ros2humble_ws/install/setup.bash
   ```

4. **Recién ahora creas paquetes** dentro de `src/` (ej. `mi_primer_paquete`, visto en el
   archivo 3 de este módulo) — **esto sí lo haces una vez por cada paquete nuevo que quieras**.

5. **Vuelves a compilar** cada vez que creas un paquete nuevo o modificas su código (sin
   `--symlink-install`) — con `--packages-select <nombre>` para ir más rápido:
   ```bash
   colcon build --packages-select mi_primer_paquete
   ```

En resumen: **el workspace (pasos 1-2) se crea una sola vez**; **`colcon build` (paso 5) lo
repites constantemente**, cada vez que agregas o cambias un paquete. No hay que "recrear" el
workspace cada vez — solo re-compilar.

## Teoría

Un **workspace** (espacio de trabajo) es una carpeta donde desarrollas, compilas e instalas
**tus propios paquetes** de ROS2. `~/ros2humble_ws` (donde vive este tutorial) es exactamente
eso: un workspace.

### Estructura estándar

```
ros2humble_ws/
├── src/       # AQUÍ escribes tu código — el código fuente de tus paquetes
├── build/     # Archivos intermedios de compilación (los genera colcon, no lo tocas a mano)
├── install/   # Los paquetes ya compilados e "instalados", listos para usar
└── log/       # Logs de cada compilación (útil para depurar errores de build)
```

Solo `src/` es tuyo — `build/`, `install/` y `log/` los genera `colcon build` automáticamente
y **no deberías editarlos a mano** (ni versionarlos en git, se regeneran siempre).

Puedes confirmarlo en tu propio workspace ahora mismo:

```bash
ls ~/ros2humble_ws
```

### Overlay y underlay

ROS2 mismo (`/opt/ros/humble/`) es, conceptualmente, **otro workspace** — ROS2 lo llama el
**underlay** (la capa de abajo, ya instalada por `apt`). Tu `~/ros2humble_ws/install/` es un
**overlay** (una capa encima) que **extiende** al underlay con tus propios paquetes.

Por eso, cuando trabajas en tu workspace, tienes que hacer `source` de **ambos**, en este
orden:

```bash
source /opt/ros/humble/setup.bash              # underlay: ROS2 base
source ~/ros2humble_ws/install/setup.bash       # overlay: tus paquetes
```

Si solo haces `source` del underlay, `ros2 run` no va a encontrar los paquetes que tú creaste
— por eso este segundo `source` es el paso que más se le olvida a un principiante.

> 💡 Puedes tener **varios overlays encadenados** (workspace A sobre workspace B sobre ROS2
> base) — típico cuando un proyecto grande separa dependencias en distintos workspaces. Por
> ahora, con un solo workspace nos alcanza.

## Ejercicio

1. Corre `ls ~/ros2humble_ws` y confirma que existen `src/`, `build/`, `install/`, `log/`
   (ya deberían existir porque compilamos algo en este módulo — si no, sigue al siguiente
   archivo primero).
2. Abre una terminal **nueva**, y antes de hacer nada, corre:
   ```bash
   ros2 pkg list | grep mi_primer_paquete
   ```
   ¿Aparece? (No debería — falta el `source` del overlay.) Ahora corre
   `source ~/ros2humble_ws/install/setup.bash` y repite el comando — ¿aparece ahora?

➡️ Siguiente: [colcon en detalle](02-colcon.md)
