import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, TimerAction, GroupAction
from launch_ros.actions import Node

def generate_launch_description():
    
    # paths used in executions
    home = os.path.expanduser('~')
    ardupilot_path = os.path.join(home, 'WAUV', 'ardupilot')
    gz_world = os.path.join(home, 'WAUV', 'WAUVSim', 'src', 'wauv_gz', 'worlds', 'wauv.world')
    qgc_path = os.path.join(home, 'WAUV', 'QGroundControl-x86_64.AppImage')

    # gather vars to launch gazebo first      
    gz_ev = [
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=os.path.join(home, 'WAUV', 'WAUVSim', 'src', 'wauv_gz', 'models')
        ),

        SetEnvironmentVariable(
            name='GZ_SIM_SYSTEM_PLUGIN_PATH',
            value=os.path.join(home, 'WAUV', 'ardupilot_gazebo', 'build')
        ),
    ]

    # launch it
    gz = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '3', '-r', gz_world],
        output='screen'
    )

    # start ArduSub SITL after waiting for Gazebo
    ardusub = TimerAction(
        period = 30.0,
        actions=[  
            ExecuteProcess(
                cmd=['bash', '-c',
                    f'source {home}/.profile && cd {ardupilot_path} && '
                    './Tools/autotest/sim_vehicle.py -v ArduSub -L CMAC --map --console '
                    '-f vectored_6dof --model JSON --out=udp:127.0.0.1:14551'],
                output='screen'
            ), 
        ]
    )

    # start MAVROS after ArduSub is ready
    mavros = TimerAction(
        period = 60.0,
        actions=[
            ExecuteProcess(
                cmd=['bash', '-c',
                    'source /opt/ros/humble/setup.bash && '
                    'ros2 run mavros mavros_node --ros-args '
                    '-p fcu_url:=udp://127.0.0.1:14551@127.0.0.1:14551'],
                output='screen'
            ),
        ]
    )

    # can optionally add QGC for simulation telemetry / GUI

    # start ROS stack after MAVROS
    ros_stack = TimerAction(
        period = 20.0,
        actions=[
            # ros-gazebo bridge
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                name='gz_ros_bridge',
                arguments=[
                    '/bluerov2_heavy/depth_camera/image@sensor_msgs/msg/Image@gz.msgs.Image',
                    '/bluerov2_heavy/depth_camera/depth_image@sensor_msgs/msg/Image@gz.msgs.Image',
                    '/bluerov2_heavy/depth_camera/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked',
                    '/bluerov2_heavy/depth_camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
                ],
                output='screen'
            ),

            # start ROS nodes
            Node(
                package='wauv_sim',
                executable='vehicle_manager',
                name='vehicle_manager',
                output='screen'
            ),

            Node(
                package='wauv_sim',
                executable='motion_controller',
                name='motion_controller',
                output='screen'
            ),

            Node(
                package='wauv_sim',
                executable='waypoint_detector',
                name='waypoint_detector',
                output='screen'
            ),

            Node(
                package='wauv_sim',
                executable='perception',
                name='perception',
                output='screen'
            ),
        ]
    )

    return LaunchDescription(gz_ev + [gz, ardusub, mavros, ros_stack])