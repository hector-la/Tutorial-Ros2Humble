import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

LIMITE_VENTANA = 11.0  # turtlesim usa una ventana ~11x11


class MonitorPose(Node):
    def __init__(self):
        super().__init__('monitor_pose')
        self.declare_parameter('margen', 1.0)
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.callback_pose, 10)

    def callback_pose(self, msg):
        margen = self.get_parameter('margen').get_parameter_value().double_value
        cerca_del_borde = (
            msg.x < margen or msg.x > (LIMITE_VENTANA - margen) or
            msg.y < margen or msg.y > (LIMITE_VENTANA - margen)
        )
        if cerca_del_borde:
            self.get_logger().warn(
                f'¡Tortuga cerca del borde! x={msg.x:.2f}, y={msg.y:.2f}')


def main(args=None):
    rclpy.init(args=args)
    nodo = MonitorPose()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
