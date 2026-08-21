#!/bin/bash

# Package installation
echo -e "\nChecking for dependencies, installing if necessary..."

DISTRO="${ROS_DISTRO:-jazzy}"

sed "s/ros-[a-z]*/ros-${DISTRO}/g" "$(dirname "$0")/requirements.txt" | xargs sudo apt-get install -y

# If required add a new on boot service
