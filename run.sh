#!/bin/bash

# Define the tmux session name
SESSION_NAME="gz_sim_session"

# Check if a tmux session with this name already exists. If so, kill it.
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? == 0 ]; then
  echo "Killing existing tmux session..."
  tmux kill-session -t $SESSION_NAME
fi

# 1. Start a new detached tmux session and launch the Gazebo world
tmux new-session -d -s $SESSION_NAME 'source /opt/ros/jazzy/setup.bash && gz sim -v 4 worlds/simple_gamefield.sdf'

# 2. Split the window horizontally and spawn the robot
# Use single quotes for the outer tmux send-keys argument to preserve the inner escaping
tmux split-window -h -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME 'source /opt/ros/jazzy/setup.bash && sleep 10 && gz service -s /world/simple_gamefield/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --req "sdf_filename: \"/home/devcontainers/workspace/robot/model.sdf\", name: \"robot\", pose: {position: {x: 4, y: 4, z: 2}}"' C-m

# 3. Split the right pane vertically and start the Python teleop script
tmux split-window -v -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME 'source /opt/ros/jazzy/setup.bash && sleep 12 && scripts/main.py' C-m

# 4. Attach your terminal to the new tmux session
tmux attach-session -t $SESSION_NAME
