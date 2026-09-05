import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String,
            'saludo',
            self.callback_saludo,
            10)

    def callback_saludo(self, msg):
        self.get_logger().info(f'Escuché: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    nodo = Listener()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
