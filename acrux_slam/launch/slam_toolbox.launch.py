import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    slam_dir = get_package_share_directory('acrux_slam')
    params_file_sim = os.path.join(slam_dir, 'config', 'slam_toolbox_params_sim.yaml')
    params_file_real = os.path.join(slam_dir, 'config', 'slam_toolbox_params.yaml')
    default_map_path = os.path.join(get_package_share_directory('acrux_navigation'), 'maps', 'nav2_test_map.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = PythonExpression([
        f"'{params_file_sim}' if str(", use_sim_time, ").lower() in ['true', '1'] else '{params_file_real}'"
    ])
    exploration  = LaunchConfiguration('exploration')
    map_file     = LaunchConfiguration('map_file')

    scan_topic = PythonExpression([
        "'/scan' if ", use_sim_time, " else '/scan_filtered'"
    ])
    map_file_name = PythonExpression([
        "'", map_file, "'.replace('.yaml', '')"
    ])
    node_executable = PythonExpression([
        "'async_slam_toolbox_node' if (", exploration, " == 'True' or ", exploration, " == True) else 'localization_slam_toolbox_node'"
    ])

    slam_mode = PythonExpression([
        "'mapping' if (", exploration, " == 'True' or ", exploration, " == True) else 'localization'"
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='False',
            description='Use simulation clock if true'
        ),
        DeclareLaunchArgument(
            name='exploration',
            default_value='True',
            description='Flag to enable exploration (mapping) vs localization'
        ),
        DeclareLaunchArgument(
            name='map_file',
            default_value=default_map_path,
            description='Map file path'
        ),

        Node(
            package='slam_toolbox',
            executable=node_executable,
            name='slam_toolbox',
            output='screen',
            parameters=[
                params_file,
                {
                    'use_sim_time': use_sim_time,
                    'mode': slam_mode,
                    'map_file_name': map_file_name,
                    'map_start_at_dock': False,
                    'scan_topic': scan_topic,
                }
            ],
            remappings=[
                ('scan', scan_topic)
            ]
        )
    ])