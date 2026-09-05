import rclpy
from rclpy.node import Node


class HolaRos2(Node):
    def __init__(self):
        super().__init__('hola_ros2')
        self.get_logger().info('¡Hola ROS2! Este nodo arrancó y está funcionando.')


def main(args=None):
    rclpy.init(args=args)
    nodo = HolaRos2()
    rclpy.spin_once(nodo, timeout_sec=0.5)  # deja procesar un ciclo antes de cerrar
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
