import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ClienteSuma(Node):
    def __init__(self):
        super().__init__('cliente_suma')
        self.cli = self.create_client(AddTwoInts, 'sumar_dos_enteros')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando a que el servicio esté disponible...')
        self.req = AddTwoInts.Request()

    def enviar_peticion(self, a, b):
        self.req.a = a
        self.req.b = b
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    nodo = ClienteSuma()
    respuesta = nodo.enviar_peticion(a, b)
    nodo.get_logger().info(f'Resultado: {a} + {b} = {respuesta.sum}')

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
