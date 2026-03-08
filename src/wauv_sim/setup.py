from setuptools import find_packages, setup

package_name = 'wauv_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/bluerov_sim.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ktoriumi',
    maintainer_email='keijitoriumi89@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'motion_controller = wauv_sim.motion_controller:main',
            'waypoint_detector = wauv_sim.waypoint_detector:main',
        ],
    },
)