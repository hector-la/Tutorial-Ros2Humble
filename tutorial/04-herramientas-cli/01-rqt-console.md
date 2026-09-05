# rqt_console — ver logs

Referencia oficial: [Using rqt_console to view logs](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html).

## Teoría

Cada nodo de ROS2 puede emitir **mensajes de log** (igual que un `print` pero con más
contexto) para informar de eventos, avisar de problemas, o depurar. Cada mensaje tiene un
**nivel de severidad**, de menor a mayor:

| Nivel | Cuándo se usa |
|---|---|
| `DEBUG` | Detalle interno, solo útil mientras depuras |
| `INFO` | Información normal de funcionamiento |
| `WARN` | Algo raro pasó, pero el nodo puede seguir |
| `ERROR` | Algo falló, probablemente afecta el resultado |
| `FATAL` | El nodo no puede continuar |

Por defecto solo ves `INFO` para arriba en la terminal. **`rqt_console`** te da una interfaz
gráfica para ver, filtrar y buscar en todos los logs del sistema, y **`rqt_logger_level`** te
deja subir/bajar el nivel de log de un nodo **mientras corre**, sin reiniciarlo.

## Ejemplo práctico

Abre en terminales separadas:

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtlesim turtle_teleop_key

# Terminal 3
ros2 run rqt_console rqt_console

# Terminal 4
ros2 run rqt_logger_level rqt_logger_level
```

En la ventana de `rqt_console` verás los mensajes `INFO` que `turtlesim_node` emitió al
arrancar. Ahora, en la terminal de teleop, mueve la tortuga contra un borde de la ventana —
aparecerá un mensaje `WARN` en `rqt_console` avisando que la tortuga tocó el límite.

### Filtrar mensajes

En `rqt_console` puedes:
- Ordenar por columna (severidad, nodo, tiempo)
- Escribir texto en el filtro de "Exclude" para **ocultar** mensajes que contengan ese texto
  (ej. excluye todo lo que diga "Spawning" si ya no te interesa)
- Guardar el log completo a un archivo con el botón de guardar, para revisarlo después

### Cambiar el nivel de log de un nodo

En `rqt_logger_level`, selecciona el nodo `/turtlesim` en el dropdown, y cambia su nivel a
`Debug`. Vuelve a mover la tortuga — ahora vas a ver muchísimos más mensajes en
`rqt_console` (los de nivel `DEBUG`, que antes estaban ocultos).

## Ejercicio

1. Sube el nivel de log de `/turtlesim` a `Debug` y cuenta cuántos mensajes nuevos aparecen
   al mover la tortuga un solo paso.
2. Usa el filtro de "Exclude" en `rqt_console` para ocultar un tipo de mensaje específico.
3. Piensa un caso real: si estuvieras depurando un nodo que falla intermitentemente en un
   robot, ¿por qué te conviene `rqt_console` en vez de solo leer la terminal?

➡️ Siguiente: [ros2 launch](02-launch.md)
