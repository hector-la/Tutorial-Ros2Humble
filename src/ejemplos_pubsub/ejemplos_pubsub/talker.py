import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(String, 'saludo', 10)
        self.contador = 0
        timer_periodo = 0.5  # segundos -> publica a 2 Hz
        self.timer = self.create_timer(timer_periodo, self.callback_timer)

    def callback_timer(self):
        msg = String()
        msg.data = f'Hola desde ROS2, mensaje #{self.contador}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: "{msg.data}"')
        self.contador += 1


def main(args=None):
    rclpy.init(args=args)
    nodo = Talker()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
