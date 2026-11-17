# ROS 2 Workshop: Windows Installation Guide

Welcome to the ROS 2 Workshop! Since ROS 2 runs natively on Linux, we will use Windows Subsystem for Linux (WSL) to run a fully functional Ubuntu environment directly inside your Windows laptop. 

This guide will take you from a blank slate to running the workshop's `run.sh` script with Gazebo and `tmux`.

## Phase 1: Install WSL and Ubuntu 24.04

First, we need to enable WSL and install Ubuntu 24.04, which is the required operating system for ROS 2 Jazzy.

1. Click your Windows Start Menu, search for **PowerShell**, right-click it, and select **"Run as administrator"**.
2. Copy and paste the following command into PowerShell and press **Enter**:
   ```powershell
   wsl --install -d Ubuntu-24.04
   ```
3. **Restart your computer** if Windows prompts you.
4. After restarting, a Linux terminal window will open automatically. It will take a few minutes to initialize.
5. When prompted, create a **UNIX username** and **password**. 
   *(Note: When typing your password, nothing will appear on the screen. This is a normal security feature. Just type it and press Enter.)*

## Phase 2: Install ROS 2 (Jazzy) and Dependencies

Now that your Ubuntu terminal is open, copy and paste these commands one block at a time to install ROS 2 Jazzy, Gazebo Harmonic, and the required tools (`tmux`, `git`, and Python bindings).

1. **Set up your locale** (UTF-8 support):
   ```bash
   sudo apt update && sudo apt install locales -y
   sudo locale-gen en_US en_US.UTF-8
   sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
   export LANG=en_US.UTF-8
   ```

2. **Enable required repositories** and add the ROS 2 GPG key:
   ```bash
   sudo apt install software-properties-common -y
   sudo add-apt-repository universe -y
   sudo apt update && sudo apt install curl -y
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```

3. **Install ROS 2, Gazebo, Tmux, and Python tools**:
   *(This downloads a lot of data and will take several minutes.)*
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install ros-jazzy-desktop -y
   sudo apt install ros-jazzy-ros-gz -y
   sudo apt install python3-gz-harmonic tmux git -y
   ```

4. **Source your setup script** so your terminal recognizes ROS 2 commands:
   ```bash
   echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```

## Phase 3: Download and Run the Workshop

Finally, download the workshop files, fix the hardcoded paths, and launch the environment.

1. **Clone the workshop repository** to your local environment:
   ```bash
   git clone https://github.com/LimWeiJen/ros2-workshop.git
   cd ros2-workshop
   ```

2. **Fix the hardcoded path in `run.sh`**:
   The `run.sh` script looks for the robot model in `/home/devcontainers/workspace/`. Run this command to automatically replace it with your actual current directory:
   ```bash
   sed -i "s|/home/devcontainers/workspace|$PWD|g" run.sh
   ```

3. **Make the scripts executable**:
   ```bash
   chmod +x run.sh
   chmod +x scripts/main.py
   ```

4. **Launch the workshop!**
   ```bash
   ./run.sh
   ```

*(Note: The script will open a `tmux` session with multiple panes. You can exit tmux entirely at any time by pressing `Ctrl+b` and then typing `:kill-session` and pressing Enter).*
