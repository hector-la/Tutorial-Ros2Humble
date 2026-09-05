import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServidorSuma(Node):
    def __init__(self):
        super().__init__('servidor_suma')
        self.srv = self.create_service(AddTwoInts, 'sumar_dos_enteros', self.callback_sumar)

    def callback_sumar(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Petición: {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    nodo = ServidorSuma()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
