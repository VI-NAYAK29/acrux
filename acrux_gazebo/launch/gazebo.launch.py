import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    acrux_gazebo_share = get_package_share_directory('acrux_gazebo')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    default_world = os.path.join(acrux_gazebo_share, 'worlds', 'nav2_test_world.sdf')
    default_bridge_config = os.path.join(acrux_gazebo_share, 'config', 'ros_gz_bridge.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')
    bridge_config = LaunchConfiguration('bridge_config')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='True',
        description='Use simulation time if true'
    )

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=default_world,
        description='Full path to world SDF file to load'
    )

    declare_bridge_config_cmd = DeclareLaunchArgument(
        name='bridge_config',
        default_value=default_bridge_config,
        description='Full path to ros_gz_bridge YAML configuration file'
    )

    gz_sim_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world]}.items()
    )

    spawn_robot_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'acrux', '-topic', 'robot_description'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    ros_gz_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config,
            'use_sim_time': use_sim_time,
        }],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_world_cmd,
        declare_bridge_config_cmd,
        gz_sim_cmd,
        spawn_robot_cmd,
        ros_gz_bridge_cmd
    ])