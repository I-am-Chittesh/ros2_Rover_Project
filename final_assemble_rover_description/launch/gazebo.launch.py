import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'final_assemble_rover_description'
    pkg_path = get_package_share_directory(package_name)
    
    # Parse the URDF/XACRO file
    xacro_file = os.path.join(pkg_path, 'urdf', 'final_assemble_rover.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = {'robot_description': robot_description_config.toxml()}
    
    # 1. Start the robot state publisher to broadcast the rover's "bones"
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_desc]
    )
    
    # 2. Boot up the empty Gazebo physics world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )
    
    # 3. Spawn the rover into the simulation
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_rover', '-z', '0.15'],
        output='screen'
    )
    
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity
    ])