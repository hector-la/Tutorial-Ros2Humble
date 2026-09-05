from setuptools import find_packages, setup

package_name = 'mi_primer_paquete'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hectorros',
    maintainer_email='hectorros@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hola_ros2 = mi_primer_paquete.hola_ros2:main',
            'nodo_parametros = mi_primer_paquete.nodo_parametros:main',
        ],
    },
)
