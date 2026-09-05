import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from reto_final_interfaces.srv import CambiarModo

MODOS_VALIDOS = ('avanzar', 'girar', 'detener')


class ControladorTortuga(Node):
    def __init__(self):
        super().__init__('controlador_tortuga')

        self.declare_parameter('velocidad_lineal', 2.0)
        self.declare_parameter('velocidad_angular', 1.0)

        self.modo = 'detener'
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.srv = self.create_service(CambiarModo, 'cambiar_modo', self.callback_cambiar_modo)
        self.timer = self.create_timer(0.2, self.callback_timer)

        self.get_logger().info('Controlador listo. Modo inicial: detener')

    def callback_cambiar_modo(self, request, response):
        if request.modo not in MODOS_VALIDOS:
            response.exito = False
            response.mensaje = f'Modo inválido. Usa uno de: {MODOS_VALIDOS}'
            return response

        self.modo = request.modo
        response.exito = True
        response.mensaje = f'Modo cambiado a: {self.modo}'
        self.get_logger().info(response.mensaje)
        return response

    def callback_timer(self):
        vel_lineal = self.get_parameter('velocidad_lineal').get_parameter_value().double_value
        vel_angular = self.get_parameter('velocidad_angular').get_parameter_value().double_value

        msg = Twist()
        if self.modo == 'avanzar':
            msg.linear.x = vel_lineal
        elif self.modo == 'girar':
            msg.angular.z = vel_angular
        # 'detener' deja msg en 0.0 en todos los campos (valor por defecto)

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    nodo = ControladorTortuga()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
