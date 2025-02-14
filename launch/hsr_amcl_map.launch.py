import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    # Define map file path
    map_file_path = os.path.join(
        get_package_share_directory('hsr_navigation'),
        'map',
        'suturo_kitchen',
        'final_projectroom_map.yaml'
    )

    # Declare map file launch argument
    map_name_arg = DeclareLaunchArgument(
        'map_name',
        default_value=map_file_path,
        description='Full path to the map YAML file'
    )

    # Map server node
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        parameters=[{'yaml_filename': map_file_path}],
        output='screen'
    )

    # TF buffer server node
    tf_buffer_node = Node(
        package='tf2_ros',
        executable='buffer_server',
        name='tf_buffer'
    )

    # AMCL node
    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        parameters=[{
            'odom_model_type': 'omni-corrected',
            'gui_publish_rate': 10.0,
            'laser_max_beams': 180,
            'min_particles': 500,
            'max_particles': 10000,
            'kld_err': 0.05,
            'kld_z': 0.95,
            'odom_alpha1': 1.0,
            'odom_alpha2': 1.0,
            'odom_alpha3': 1.0,
            'odom_alpha4': 1.0,
            'odom_alpha5': 0.2,
            'laser_z_hit': 0.85,
            'laser_z_short': 0.05,
            'laser_z_max': 0.05,
            'laser_sigma_hit': 0.2,
            'laser_z_rand': 0.05,
            'laser_lambda_short': 0.1,
            'laser_model_type': 'beam',
            'laser_likelihood_max_dist': 2.0,
            'update_min_d': 0.01,
            'update_min_a': 0.01,
            'resample_interval': 1,
            'transform_tolerance': 0.1,
            'recovery_alpha_slow': 0.001,
            'recovery_alpha_fast': 0.1,
            'initial_cov_aa': 0.2,
            'laser_min_range': 0.1,
            'laser_max_range': 30.0,
            'odom_frame_id': 'odom',
            'base_frame_id': 'base_footprint'
        }],
        remappings=[
            ('scan', 'hsrb/base_scan'),
            ('initialpose', 'laser_2d_correct_pose')
        ]
    )

    # Service call to change odometry type
    change_odom_type_service = ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/hsrb/odometry_switch', 'std_msgs/msg/String', '"wheel_odom"'],
        output='screen'
    )

    # Global pose publisher node
    global_pose_publisher_node = Node(
        package='hsr_navigation',
        executable='global_pose_publisher.py',
        name='global_pose_publisher',
        output='screen'
    )

    return LaunchDescription([
        map_name_arg,
        map_server_node,
        tf_buffer_node,
        amcl_node,
        change_odom_type_service,
        global_pose_publisher_node
    ])
