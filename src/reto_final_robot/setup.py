from setuptools import find_packages, setup

package_name = 'reto_final_robot'

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
            'controlador_tortuga = reto_final_robot.controlador_tortuga:main',
            'monitor_pose = reto_final_robot.monitor_pose:main',
        ],
    },
)
