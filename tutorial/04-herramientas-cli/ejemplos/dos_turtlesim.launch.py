"""
Ejemplo de módulo 04: lanza DOS turtlesim_node al mismo tiempo, cada uno con su propio
namespace, para no chocar de nombres entre sí.

Uso:
    ros2 launch dos_turtlesim.launch.py
(ejecútalo desde esta misma carpeta, o pásale la ruta completa al archivo)
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            namespace='tortuga1',
            output='screen',
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            namespace='tortuga2',
            output='screen',
        ),
    ])
