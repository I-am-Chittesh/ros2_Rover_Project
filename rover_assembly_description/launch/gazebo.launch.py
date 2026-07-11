import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'rover_assembly_description'
    pkg_share = get_package_share_directory(pkg_name)

    # Path to your SolidWorks exported URDF
    urdf_file = os.path.join(pkg_share, 'urdf', 'rover_assembly_description.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Robot State Publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Include default empty Gazebo world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # Spawn the robot (dropping it from Z = 0.1 meters so it doesn't clip the floor)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'rover',
                   '-z', '0.1'],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])