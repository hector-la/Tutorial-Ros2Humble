import rclpy
from rclpy.node import Node


class NodoParametros(Node):
    def __init__(self):
        super().__init__('nodo_parametros')
        # declarar un parámetro con valor por defecto
        self.declare_parameter('saludo', 'Hola desde un parámetro')
        self.timer = self.create_timer(1.0, self.callback_timer)

    def callback_timer(self):
        # leer el valor actual del parámetro en cada ciclo (puede cambiar en caliente)
        valor = self.get_parameter('saludo').get_parameter_value().string_value
        self.get_logger().info(valor)


def main(args=None):
    rclpy.init(args=args)
    nodo = NodoParametros()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
