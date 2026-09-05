# Reto 2 — Sistema pub/sub múltiple

## Enunciado

Construye un sistema de **2 publishers y 1 subscriber** que simule dos sensores distintos de
un robot, con un nodo central que los combina.

## Requisitos

1. **Nodo `sensor_temperatura`**: publica en `/temperatura` (`std_msgs/msg/Float32`) cada 1s,
   valores aleatorios entre `15.0` y `35.0`.
2. **Nodo `sensor_bateria`**: publica en `/bateria` (`std_msgs/msg/Float32`) cada 1s, un valor
   que **empiece en 100.0 y vaya bajando** de a poco cada vez que publica (no aleatorio —
   simula descarga real), sin bajar de `0.0`.
3. **Nodo `monitor`**: se suscribe a **ambos** tópicos (`/temperatura` y `/bateria`) y:
   - Guarda el último valor recibido de cada uno (en atributos de la clase).
   - Cuando la batería baja de `20.0`, loguea una advertencia.
   - Cuando la temperatura sube de `30.0`, loguea una advertencia distinta.

## Criterios de éxito

- Los 3 nodos corren al mismo tiempo (en 3 terminales) sin errores.
- `ros2 node list` muestra los 3 nodos.
- `rqt_graph` muestra visualmente cómo `monitor` recibe de los otros dos (repasa módulo 03).
- Ves las advertencias de `monitor` aparecer cuando corresponde (batería baja o temperatura
  alta), sin que tengas que forzar nada manualmente — deben ocurrir solas con el tiempo.

## Pistas (si te trabas)

<details>
<summary>Pista 1 — dos suscripciones en el mismo nodo</summary>

Puedes llamar a `self.create_subscription(...)` dos veces en el mismo `__init__`, una por
cada tópico, cada una con su propio método callback.
</details>

<details>
<summary>Pista 2 — guardar el último valor</summary>

En el callback de temperatura: `self.ultima_temperatura = msg.data`. Luego puedes leer ese
atributo desde donde quieras dentro de la clase (otro callback, un timer, etc.).
</details>

<details>
<summary>Pista 3 — batería que baja sola</summary>

En el nodo de batería, guarda el nivel actual como atributo de instancia (`self.nivel = 100.0`
en `__init__`) y en cada ciclo del timer resta un poco (`self.nivel -= 0.5`) antes de publicar,
con un `max(self.nivel, 0.0)` para que no baje de cero.
</details>

<details>
<summary>Pista 4 — ¿un paquete o tres?</summary>

Puedes poner los 3 nodos en el **mismo paquete** (3 archivos `.py`, 3 entradas en
`entry_points`) — no hace falta un paquete por nodo. Así se hace normalmente en proyectos
reales.
</details>

➡️ Siguiente: [Reto 3 — Servicio calculadora](../reto-03-servicio-calculadora/enunciado.md)
