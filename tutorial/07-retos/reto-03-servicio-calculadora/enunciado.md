# Reto 3 — Servicio calculadora

## Enunciado

Crea un servicio propio (interfaz `.srv` custom, como en el módulo 06 archivo 3) que funcione
como una calculadora con **varias operaciones**, no solo suma.

## Requisitos

1. Crea un paquete de interfaces (`ament_cmake`) con un servicio `Calculadora.srv`:
   ```
   float64 a
   float64 b
   string operacion
   ---
   float64 resultado
   bool exito
   string mensaje
   ```
   (`operacion` será un string: `"sumar"`, `"restar"`, `"multiplicar"` o `"dividir"`)

2. Crea un nodo servidor que:
   - Según el valor de `operacion`, haga la cuenta correspondiente.
   - Ponga el resultado en `response.resultado`.
   - Si `operacion` no es ninguna de las 4 válidas, ponga `exito = false` y un
     `mensaje` explicando el error (y `resultado` en `0.0`).
   - **Caso especial**: si `operacion == "dividir"` y `b == 0`, también debe fallar
     controladamente (`exito = false`, mensaje tipo "no se puede dividir por cero"), **sin
     que el nodo se caiga**.

3. Crea un nodo cliente que reciba `a`, `b` y `operacion` como argumentos de línea de
   comandos y muestre el resultado (o el mensaje de error).

## Criterios de éxito

- Compila sin errores (`ejemplos_interfaces`-style: paquete de interfaces + paquete de nodos).
- `ros2 interface show <tu_paquete>/srv/Calculadora` muestra la estructura correcta.
- Probar las 4 operaciones válidas da resultados correctos.
- Probar con una operación inválida (ej. `"potencia"`) da `exito: false` sin tumbar el nodo.
- Probar `dividir` con `b: 0` da `exito: false` sin tumbar el nodo (el servidor **sigue
  corriendo** después, listo para la siguiente petición).

## Pistas (si te trabas)

<details>
<summary>Pista 1 — estructura del proyecto</summary>

Repasa módulo 06, archivo 3, completo: es exactamente el mismo patrón (paquete de interfaces
+ paquete de nodos que las usa), solo que ahora tú decides los campos y la lógica.
</details>

<details>
<summary>Pista 2 — decidir la operación</summary>

Un `if`/`elif`/`else` encadenado sobre `request.operacion` es suficiente — no hace falta nada
sofisticado.
</details>

<details>
<summary>Pista 3 — evitar que el nodo se caiga</summary>

El truco es **nunca dejar que Python lance una excepción sin capturarla** dentro del
callback. Antes de dividir, pregunta explícitamente `if b == 0:` en vez de dejar que Python
lance `ZeroDivisionError`.
</details>

➡️ Siguiente: [Reto 4 — Launch file completo](../reto-04-launch-completo/enunciado.md)
