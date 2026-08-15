import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'rover_assembly_description'
    
    # 1. Path to the URDF file
    urdf_path = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'rover_assembly_description.urdf')
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    # 2. Path to your custom house world
    default_world_path = os.path.join(
        os.path.expanduser('~'),
        'ros2_ws',
        'src',
        'my_rover',
        'world_files',
        'world_sim.world'
    )

    # Allow overriding the world via CLI if ever needed, but default to your house
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Full path to world model file to load'
    )

    # 3. Include Gazebo launch with the default world argument
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': LaunchConfiguration('world')}.items()
    )

    # 4. Robot State Publisher (TF broadcaster with use_sim_time enabled)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_desc},
            {'use_sim_time': True}
        ]
    )

    # 5. Spawn the rover into Gazebo
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'rover_assembly',
        '-x', '-3.400000', 
        '-y', '-3.400000',
        '-z', '0.033876',
        '-R', '-0.001036',
        '-P', '-0.050862',
        '-Y', '2.082935'],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node
    ])