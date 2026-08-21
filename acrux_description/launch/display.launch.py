import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    desc_pkg_share = get_package_share_directory('acrux_description')
    gazebo_pkg_share = get_package_share_directory('acrux_gazebo')

    default_model_path = os.path.join(desc_pkg_share, 'urdf/acrux.xacro')
    default_rviz_config_path = os.path.join(desc_pkg_share, 'rviz/display.rviz')
    default_world = os.path.join(gazebo_pkg_share, 'worlds/room2.sdf')

    use_sim_time = LaunchConfiguration('use_sim_time')
    model = LaunchConfiguration('model')
    rvizconfig = LaunchConfiguration('rvizconfig')
    world = LaunchConfiguration('world')

    state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(desc_pkg_share, 'launch', 'state_publisher.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'model': model
        }.items()
    )

    rviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(desc_pkg_share, 'launch', 'rviz.launch.py')
        ),
        launch_arguments={
            'rvizconfig': rvizconfig
        }.items()
    )

    gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg_share, 'launch', 'gazebo.launch.py')
        ),
        condition=IfCondition(use_sim_time),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'world': world
        }.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='True',
            description='Flag to enable use_sim_time'
        ),
        DeclareLaunchArgument(
            name='model',
            default_value=default_model_path,
            description='Absolute path to robot urdf file'
        ),
        DeclareLaunchArgument(
            name='rvizconfig',
            default_value=default_rviz_config_path,
            description='Absolute path to rviz config file'
        ),
        DeclareLaunchArgument(
            name='world',
            default_value=default_world,
            description='World SDF file for Gazebo Harmonic'
        ),

        state_publisher_cmd,
        rviz_cmd,
        gazebo_cmd,
    ])