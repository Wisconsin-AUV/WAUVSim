#!/bin/bash

# source ROS2
source /opt/ros/humble/setup.bash

# remove the build install log artifacts
echo "Clearing old files..."
rm -rf build install log

# build the package
echo "Building package..."
colcon build --symlink-install

# source it
source install/setup.bash

echo "Ready ٩(◕‿◕)۶"