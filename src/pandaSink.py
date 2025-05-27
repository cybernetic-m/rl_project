import os 
import sys

# Adjust this path to where your robocasa directory is
current_dir = os.path.dirname(os.path.abspath(__file__)) 
repo_dir = os.path.abspath(os.path.join(current_dir, '..'))
env_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
robocasa_path = env_dir + "/robocasa"
robosuite_path = env_dir + "/robosuite"
saving_path = repo_dir + '/simulations'
utils_path = repo_dir + '/utils'
sys.path.append(robocasa_path)
sys.path.append(robosuite_path)
sys.path.append(utils_path)

import json
#import pprint
#from robocasa.environments import ALL_KITCHEN_ENVIRONMENTS
#from robocasa.environments.kitchen.kitchen import Kitchen
from robocasa.environments.kitchen.single_stage.kitchen_sink import TurnOnSinkFaucet
from robocasa.utils.env_utils import create_env
import numpy as np
import imageio
import matplotlib.pyplot as plt

# Import of ours functions
from inspData import inspData

# First of all you need to modify the config.json file if you want to render online or offline the simulation:
# 'renderer_onscreen': True to activate online rendering to visualize the simulation
# 'has_offscreen_renderer': True to save the video offline 
# 'use_camera_obs': True to take images from obs
# 'render_camera': None to have the central camera that see all the robot (otherwise use another camera name from the list "Available Cameras")
#  'video_saving': to save the video as trial.mp4 inside the simulations directory

# Description of the action space and observation space for GR1 Robot:
# Action Space
# Ex. action = [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# First 12 values can go from (-inf, +inf) because they are the 

# Name of the video to save
video_name = 'trial.mp4'
os.makedirs(saving_path, exist_ok=True)

# Dataset path
dataset_path = robocasa_path + ('/datasets/v0.1/single_stage'
                                '/kitchen_sink/TurnOnSinkFaucet/2024-04-25'
                                '/demo_gentex_im128_randcams.hdf5')

print("Dataset path:", dataset_path)

inspData(dataset_path)  # Inspect the dataset structure

'''
# Reading of the json config file
with open(repo_dir+"/config.json", "r") as f:
    config = json.load(f)


# You can put True/False for video_saving flag to save or not a video of your simulation
if sys.platform.startswith("win"):
    print("\nOS: Windows!\n")
    video_saving = config["video_saving"] # For Windows systems tested and works!
    mac_os_flag = False
elif sys.platform == "darwin":
    print("\nOS: MacOS\n")
    video_saving = config["video_saving"]  # For M1 systems tested and works!
    mac_os_flag = True
elif sys.platform == "linux":
    print("\nOS: Linux\n")
    video_saving = config["video_saving"] # For Linux systems tested and works!
    mac_os_flag = False


env = TurnOnSinkFaucet(
    robots="PandaOmron", #type of the robot 
    has_renderer=config['has_render'], 
    has_offscreen_renderer=config['has_offscreen_renderer'], 
    use_camera_obs=config['use_camera_obs'], 
    render_camera=config['render_camera'] if not mac_os_flag else "robot0_frontview", 
    seed=1, # the seed to change kitchen form
    init_robot_base_pos="sink", # where to start the robot
    layout_ids=-3, # island in the kitchen
    style_ids=9,# color and style on the kithen
    camera_names=["robot0_robotview"], # Camera for the camera_obs,
)

# reset the environment
obs_0 = env.reset() 
robot = env.robots[0]

# Only for MacOS users, for problem in offscreen rendering (M1 tested)
if mac_os_flag:
    cam_id = env.sim.model.camera_name2id("robot0_frontview")  # Take the camera ID from the camera name
    # Set custom position and orientation (example: looking at robot from above)
    env.sim.model.cam_pos[cam_id] = [2.0, 0.0, 0.5]  # x, y, z
    env.sim.model.cam_quat[cam_id] = [0.5, 0.5, 0.5, 0.5] # quaternion values

# Print of the obs space dim
# obs is an ordered dictionary of the type "sensor": "value"
print("\nThe observation space dim is:", len(obs_0))
print("\nList of all sensors:\n")
for key, value in obs_0.items(): 
    print(f"{key}: shape = {value.shape}, dtype = {value.dtype}")

# get task language
lang = env.get_ep_meta()["lang"]
print("\nTask:\n", lang)

# This is a list of all available cameras depending on the robot
print("\nAvailable cameras:\n", env.sim.model.camera_names)

# Create the video writer to save the video as /simulations/trial.mp4
if video_saving:
    video_writer = imageio.get_writer(saving_path + "/" + video_name, fps=20) 

# env.action_spec is a tuple (action_low, action_high) 
# where action_low is the minimum value of an action, action high is the maximum value
print("\nThe action space dim is:", robot.action_dim)

# Print of the minimum values of actions
print("\nMinimum values of actions:\n")
print(env.action_spec[0].tolist())

# Print of the maximum values of actions
print("\nMaximum values of actions:\n")
print(env.action_spec[1].tolist())

# 
# Loop of sampling-action
for i in range(500):
    
    #action = np.array([0, 0, 0, 0, 0, 0, 0]) 
    action = np.zeros(env.action_spec[0].shape)

    obs, reward, done, info = env.step(action)  # take action in the environment
    
    
    if i==0:
        img_flipped = np.flipud(obs["robot0_robotview_image"]) #we need to flip the observation from the camera
        plt.imshow(img_flipped)#256,256,3
        plt.show()
    

    if config['has_render']:
        env.render()  # render on display
    
    if video_saving:
        frame = env.sim.render(
            camera_name = "robot0_robotview",
            width=640, height=480,
            depth=False
        )
        frame = np.flipud(frame) #we need to flip the image
        video_writer.append_data(frame)

# Another loop for saving a video
if video_saving:
    print("Saving the video")
    video_writer.close()
    print(f"Video saved in {saving_path} as {video_name}")

    '''