from setuptools import find_packages, setup

package_name = 'ejemplos_uso_custom'

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
            'publicador_sensor = ejemplos_uso_custom.publicador_sensor:main',
            'servidor_suma3 = ejemplos_uso_custom.servidor_suma3:main',
        ],
    },
)
