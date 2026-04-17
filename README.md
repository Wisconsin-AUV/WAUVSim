# WAUVSim

Simulation repo for WAUV.

Instructions

First time setup:
- Open a terminal in Ubuntu 22.04 (with WSL2)
- Clone this repo in a directory named 'WAUV'
- In the bash terminal, run the command './install.sh' (expect to wait at least 20 minutes)
- - Write "chmod +x build.sh" to enable ./build.sh

Every time you run the simulation:
- Rebuild by entering './build.sh' in the directory '~/WAUV/WAUVSim'
- Source it, 'source install/setup.bash'
- To launch the simulation to move in a circle, enter the command 'ros2 launch wauv_sim bluerov_sim.launch.py'
- to launch the keyboard control version run 'ros2 launch wauv_sim manual_sim.launch.py'
vehicle_manager.py doesnt work so for either so run the following commands in a seperate terminal after the above command:

ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'GUIDED'}"

ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: True}"

doc to run stuff: https://docs.google.com/document/d/1Oz7atfxz3A7vpXuPX55AzmUl-ptKhMm3jefa7II1z3g/edit?tab=t.0
