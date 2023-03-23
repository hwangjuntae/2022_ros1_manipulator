#!/usr/bin/env python
import os
import sys
import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    urdf_file = os.path.join(get_package_share_directory('ros1_manipulator'), 'urdf', 'manipulator.urdf')
    robot_name = 'ros1_manipulator'

    # Use xacro to convert the URDF file to a string parameter
    robot_description = launch.substitutions.LaunchConfiguration('robot_description')
    xacro_command = [ 'xacro', ' ', urdf_file, ' ', '--inorder']
    xacro = launch.actions.ExecuteProcess(
        cmd=xacro_command,
        output='screen',
        )

    return launch.LaunchDescription([
        # Pass the robot description parameter to the spawn node
        launch.actions.DeclareLaunchArgument(
            'robot_description',
            default_value=robot_description,
            description='Unparsed robot description',
        ),
        launch.actions.ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'),
        launch_ros.actions.Node(
            package='gazebo_ros',
            node_executable='spawn_model',
            arguments=['-urdf', '-param', robot_description, '-model', robot_name],
            output='screen'
        ),
        launch_ros.actions.Node(
            package='rviz2',
            node_executable='rviz2',
            arguments=['-d', os.path.join(get_package_share_directory('ros1_manipulator'), 'rviz', 'ros1_manipulator.rviz')],
            output='screen'
        )
    ])
