#!/bin/bash
set -e

# Check Ubuntu Version
if [[ $(lsb_release -rs) != "22.04" ]]; then
    echo "ERROR: This script requires Ubuntu 22.04"
    exit 1
fi

sudo apt update
sudo apt install -y curl gnupg lsb-release build-essential cmake git
sudo apt install -y python3-pip

python3 -m pip install --upgrade pip
python3 -m pip install pynput

# Clone ArduPilot
cd ~/WAUV

if [ ! -d "ardupilot" ]; then
    echo "Cloning ArduPilot..."
    git clone https://github.com/ArduPilot/ardupilot.git
fi

cd ~/WAUV/ardupilot

# Initialize submodules to have access to full tools
git submodule update --init --recursive

# Install ArduPilot dependencies
Tools/environment_install/install-prereqs-ubuntu.sh -y

# Source environment
echo "source ~/WAUV/ardupilot/Tools/completion/completion.bash" >> ~/.bashrc
echo "export PATH=\$PATH:~/WAUV/ardupilot/Tools/autotest" >> ~/.bashrc

# Install ROS2 Humble
if ! command -v ros2 &> /dev/null; then
    echo "Installing ROS2 Humble..."

    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
        -o /usr/share/keyrings/ros-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

    sudo apt update
    sudo apt install -y ros-humble-desktop \
                        python3-colcon-common-extensions \
                        python3-rosdep \
                        python3-vcstool
fi

# Source ROS
if ! grep -q "ros/humble/setup.bash" ~/.bashrc; then
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
fi

# Install ArduPilot Gazebo Plugin dependencies
sudo apt install libgz-sim8-dev rapidjson-dev
sudo apt install libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl

# Clone ArduPilot Gazebo Plugin
cd ~/WAUV

if [ ! -d "ardupilot_gazebo" ]; then
    git clone https://github.com/ArduPilot/ardupilot_gazebo.git
fi

# Build ArduPilot Gazeo Plugin
export GZ_VERSION=harmonic
cd ~/WAUV/ardupilot_gazebo
mkdir -p build && cd build
cmake ..
make -j$(nproc)

# Configure Gazebo environment
echo 'export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/WAUV/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}' >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$HOME/WAUV/ardupilot_gazebo/models:$HOME/WAUV/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}' >> ~/.bashrc

# Install Gazebo Harmonic
if ! command -v gz &> /dev/null; then
    echo "Installing Gazebo Harmonic..."

    sudo curl -fsSL https://packages.osrfoundation.org/gazebo.gpg \
        -o /usr/share/keyrings/gazebo-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gazebo-archive-keyring.gpg] \
    http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

    sudo apt update
    sudo apt install -y gz-harmonic \
                        libgz-sim8-dev \
                        libgz-math7-dev \
                        libgz-transport13-dev \
                        libgz-common5-dev \
                        rapidjson-dev
fi

# Install MAVROS
sudo apt install -y ros-humble-mavros \
                    ros-humble-mavros-extras \
                    geographiclib-tools # dependency

sudo geographiclib-get-geoids egm96-5 || true

# Create ROS2 Workspace
mkdir -p ~/WAUV/WAUVSim/src
cd ~/WAUV/WAUVSim

source /opt/ros/humble/setup.bash

# Clone BlueROV2 Gazebo model
cd ~/WAUV/WAUVSim/src

if [ ! -d "bluerov2_gz" ]; then
    git clone https://github.com/clydemcqueen/bluerov2_gz.git
fi

# Install Dependencies & Build
cd ~/WAUV/WAUVSim

source /opt/ros/humble/setup.bash

# Ensure rosdep is installed
sudo apt install -y python3-rosdep

# Initialize rosdep
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    echo "Initializing rosdep..."
    sudo rosdep init
fi

# Update rosdep
rosdep update

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Fix version issues
python3 -m pip install --upgrade pip

# CHange setuptools version
python3 -m pip install "setuptools<80"

# Build workspace
colcon build --symlink-install

# Ensure workspace is sourced properly
if ! grep -q "WAUV/WAUVSim/install/setup.bash" ~/.bashrc; then
    echo "source ~/WAUV/WAUVSim/install/setup.bash" >> ~/.bashrc
fi

echo "INSTALL COMPLETE (づ ◕‿◕ )づ"
