import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable # used to start processes
from launch_ros.actions import Node

def generate_launch_description():
    
    # paths used in executions
    home = os.path.expanduser('~')
    ardupilot_path = os.path.join(home, 'WAUV', 'ardupilot')
    gz_world = os.path.join(home, 'WAUV', 'WAUVSim', 'src', 'bluerov2_gz', 'worlds', 'bluerov2_heavy_underwater.world')
    qgc_path = os.path.join(home, 'WAUV', 'QGroundControl-x86_64.AppImage')

    return LaunchDescription([
        # set the environment variables so Gazebo locates them
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=os.path.join(home, 'WAUV', 'WAUVSim', 'src', 'bluerov2_gz', 'models')
        ),

        SetEnvironmentVariable(
            name='GZ_SIM_SYSTEM_PLUGIN_PATH',
            value=os.path.join(home, 'WAUV', 'ardupilot_gazebo', 'build')
        ),

        # start Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', '-v', '3', '-r', gz_world],
            output='screen'
        ),

        # start ArduSub SITL
        ExecuteProcess(
             cmd=['bash', '-c',
                 f'source {home}/.profile && cd {ardupilot_path} && '
                 './Tools/autotest/sim_vehicle.py -v ArduSub -L CMAC --map --console '
                 '-f vectored_6dof --model JSON --out=udp:127.0.0.1:14551'],
            output='screen'
        ),

        # start mavros
        ExecuteProcess(
            cmd=['bash', '-c',
                'source /opt/ros/humble/setup.bash && ros2 run mavros mavros_node --ros-args -p fcu_url:=udp://:14551@'],
            output='screen'
        ),

        # can optionally add QGC for simulation telemetry / GUI

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
    ])

