#!/bin/bash

# source ROS2
source /opt/ros/humble/setup.bash

# remove the build install log artifacts
echo "Clearing old files..."
rm -rf build install log

# build the package (do not include bluerov2_gz)
echo "Building package..."
colcon build --packages-select wauv_sim --symlink-install

# source it
source install/setup.bash

echo "Ready ٩(◕‿◕)۶"