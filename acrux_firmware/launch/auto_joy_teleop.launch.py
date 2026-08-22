import launch
import launch_ros.actions
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    joy_dev = LaunchConfiguration('joy_dev')

    return launch.LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='False',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'joy_dev',
            default_value='/dev/input/joy',
            description='Path to joystick device'
        ),

        # Joy node
        launch_ros.actions.Node(
            package='joy', executable='joy_node', name='acrux_joy_node',
            parameters=[
                {'dev_ff': '/dev/input/haptics'},
                {'dev': joy_dev},
                {'use_sim_time': use_sim_time},
                {'deadzone': 0.05},
                {'autorepeat_rate': 20.0}
            ],
            output='screen',
            respawn=True
        ),

        # Auto joy teleop node
        launch_ros.actions.Node(
            package='auto_joy_teleop', executable='auto_joy_teleop', name='auto_joy_teleop',
            parameters=[{
                'use_sim_time': use_sim_time,
                'scale_linear': 0.5,
                'scale_angular': 1.0,
                'axis_linear': 1,
                'axis_angular': 0,
                'deadman_axis': 2,
                'enable_button': -1,
            }],
            output='screen'
        )
    ])