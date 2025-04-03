import os 
import sys
import json


# First of all you need to modify the config.json file if you want to render online or offline the simulation:
# 'renderer_onscreen': True to activate online rendering to visualize the simulation
# 'has_offscreen_renderer': True to save the video offline 
# 'use_camera_obs': True to take images from obs
# 'render_camera': None to have the central camera that see all the robot (otherwise use another camera name from the list "Available Cameras")
  


import warnings
import logging
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("glfw").setLevel(logging.ERROR)

# Adjust this path to where your robocasa directory is
current_dir = os.path.dirname(os.path.abspath(__file__)) 
repo_dir = os.path.abspath(os.path.join(current_dir, '..'))
env_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
robocasa_path = env_dir + "/robocasa"
robosuite_path = env_dir + "/robosuite"
saving_path = repo_dir + '/simulations'
video_name = 'trial.mp4'
os.makedirs(saving_path, exist_ok=True)
sys.path.append(robocasa_path)
sys.path.append(robosuite_path)

with open(repo_dir+"\\config.json", "r") as f:
    config = json.load(f)

#from robocasa.environments import ALL_KITCHEN_ENVIRONMENTS
#from robocasa.environments.kitchen.kitchen import Kitchen
from robocasa.environments.kitchen.multi_stage.washing_dishes.pre_soak_pan import PreSoakPan
from robocasa.utils.env_utils import create_env
import numpy as np
import imageio
import matplotlib.pyplot as plt

# You can put True/False for video_saving flag to save or not a video of your simulation
if sys.platform.startswith("win"):
    print("\nOS: Windows!\n")
    video_saving = True # For Windows systems tested and works!
elif sys.platform == "darwin":
    print("\nOS: MacOS\n")
    video_saving = True  # For M1 systems tested and works!
elif sys.platform == "linux":
    print("\nOS: Linux\n")
    video_saving = True # For Linux systems tested and works!

'''
controller_config = {
    "type": "BASIC",
    "input_max": 1.0,
    "input_min": -1.0,
    "output_max": [0.1] * 6,
    "output_min": [-0.1] * 6,
    "kp": 150,
    "damping": 1.0,
    "control_delta": True,
    "interpolation": None,
    "policy_freq": 20,
}
'''

'''
# set the camera parameters
renderer_configuration={
    "lookat":[0,0,0],
    "azimuth":180,
    "elevation":-30,
    "distance":22.5
    }
'''

env = PreSoakPan(
    robots="GR1FixedLowerBody", #type of the robot ["GR1", "GR1FixedLowerBody", "GR1FloatingBase", ""]
    #controller_configs=controller_config,
    has_renderer=config['has_render'], 
    has_offscreen_renderer=config['has_offscreen_renderer'], 
    use_camera_obs=config['use_camera_obs'], 
    render_camera=config['render_camera'], 
    #control_freq=20,
    #renderer_config=renderer_configuration,
    seed=1, # the seed to change kitchen form
    init_robot_base_pos="sink", # where to start the robot
    layout_ids=-3, # island in the kitchen
    style_ids=9,# color and style on the kithen
    camera_names=["robot0_robotview"], # Camera for the camera_obs
)

# reset the environment
obs_0 = env.reset() 

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
print("\nThe action space dim is:", len(env.action_spec[0]))

# Print of the minimum values of actions
print("\nMinimum values of actions:\n")
print(env.action_spec[0].tolist())

# Print of the maximum values of actions
print("\nMinimum values of actions:\n")
print(env.action_spec[1].tolist())

 
# Loop of sampling-action
for i in range(50):
    action = np.random.randn(*env.action_spec[0].shape) * 0.1

    obs, reward, done, info = env.step(action)  # take action in the environment

    #obs['robot0_robotview_image']
    if config['has_render']:
        env.render()  # render on display
    
    if video_saving:
        frame = env.sim.render(
            camera_name = "robot0_robotview",
            width=640, height=480,
            depth=False
        )
        video_writer.append_data(frame)

# Another loop for saving a video
if video_saving:
    print("Saving the video")
    video_writer.close()
    print(f"Video saved in {saving_path} as {video_name}")
