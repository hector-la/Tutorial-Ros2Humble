import rclpy
from rclpy.node import Node
from ejemplos_interfaces.srv import SumarTresEnteros


class ServidorSuma3(Node):
    def __init__(self):
        super().__init__('servidor_suma3')
        self.srv = self.create_service(
            SumarTresEnteros, 'sumar_tres_enteros', self.callback_sumar)

    def callback_sumar(self, request, response):
        response.suma = request.a + request.b + request.c
        self.get_logger().info(
            f'Petición: {request.a} + {request.b} + {request.c} = {response.suma}')
        return response


def main(args=None):
    rclpy.init(args=args)
    nodo = ServidorSuma3()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
