from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            output='screen',
        ),
        Node(
            package='reto_final_robot',
            executable='controlador_tortuga',
            name='controlador_tortuga',
            parameters=[{
                'velocidad_lineal': 3.0,
                'velocidad_angular': 1.5,
            }],
            output='screen',
        ),
        Node(
            package='reto_final_robot',
            executable='monitor_pose',
            name='monitor_pose',
            parameters=[{'margen': 1.5}],
            output='screen',
        ),
    ])
