import random
import rclpy
from rclpy.node import Node
from ejemplos_interfaces.msg import Sensor


class PublicadorSensor(Node):
    def __init__(self):
        super().__init__('publicador_sensor')
        self.publisher_ = self.create_publisher(Sensor, 'datos_sensor', 10)
        self.timer = self.create_timer(1.0, self.callback_timer)

    def callback_timer(self):
        msg = Sensor()
        msg.nombre = 'temperatura_1'
        msg.valor = round(random.uniform(18.0, 30.0), 2)
        msg.activo = True
        self.publisher_.publish(msg)
        self.get_logger().info(f'{msg.nombre} = {msg.valor} (activo={msg.activo})')


def main(args=None):
    rclpy.init(args=args)
    nodo = PublicadorSensor()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
