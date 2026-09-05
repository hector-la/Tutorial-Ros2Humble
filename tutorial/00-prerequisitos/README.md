# 00 — Prerrequisitos

Antes de empezar, esto es lo mínimo que conviene manejar. No hace falta ser experto en nada
de esto, solo lo básico:

## Terminal / Linux
- Moverte entre carpetas (`cd`, `ls`, `pwd`)
- Crear carpetas y archivos (`mkdir`, `touch`)
- Editar un archivo (con `nano`, `code`, o el editor que prefieras)
- Variables de entorno (`export VAR=valor`, `echo $VAR`) — las vas a usar mucho en ROS2

## Python básico
- Variables, funciones, clases (los nodos de ROS2 en Python son clases)
- Imports de módulos (`import`)

## Git (opcional pero recomendado)
- `git clone`, `git add`, `git commit`, `git push` — para versionar tu propio código

## Conceptos generales (no técnicos)
- Qué es un **robot** en términos de software: sensores (entradas) → procesamiento → actuadores (salidas)
- ROS2 no es un sistema operativo real, es un **framework/middleware** que corre sobre Ubuntu
  y te da herramientas para que distintas partes de un robot (o de un programa distribuido)
  se comuniquen entre sí

## Verifica tu sistema

Antes de seguir, confirma que tienes Ubuntu 22.04:

```bash
lsb_release -a
```

Debe mostrar `Release: 22.04` y `Codename: jammy`. Si no es así, ROS2 Humble no es la
distribución recomendada para tu sistema (Humble está soportada oficialmente en Ubuntu 22.04).

### ¿No tienes Ubuntu 22.04 instalado?

Si estás en Windows y necesitas instalar Ubuntu 22.04 primero (dual boot), sigue esta guía
antes de continuar con este tutorial:

➡️ [widegonz/Ubuntu-Installation](https://github.com/widegonz/Ubuntu-Installation) — instalación
de Ubuntu 22.04 en dual boot con Windows (USB booteable + particionamiento + instalación).

Una vez que tengas Ubuntu 22.04 arrancando correctamente, vuelve aquí y sigue con el
[Módulo 01 — Instalación de ROS2](../01-instalacion/README.md).

➡️ Siguiente: [01 — Instalación](../01-instalacion/README.md)
