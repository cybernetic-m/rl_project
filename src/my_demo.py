import os 
import sys
# Adjust this path to where your robocasa directory is
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.abspath(os.path.join(current_dir, '..'))
env_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
robocasa_path = env_dir + "/robocasa"
robosuite_path = env_dir + "/robosuite"
saving_path = repo_dir + '/simulations'
os.makedirs(saving_path, exist_ok=True)
sys.path.append(robocasa_path)
sys.path.append(robosuite_path)


from robocasa.environments import ALL_KITCHEN_ENVIRONMENTS
from robocasa.utils.env_utils import create_env
import numpy as np
import imageio

# choose random task
env_name = np.random.choice(list(ALL_KITCHEN_ENVIRONMENTS))

env = create_env(
    env_name=env_name,
    render_offscreen=True,     # required for camera obs
    render_onscreen=True,      # triggers viewer
    camera_names=['robot0_eye_in_hand']
)

# reset the environment
env.reset()

# get task language
lang = env.get_ep_meta()["lang"]
print("Instruction:", lang)

video_writer = imageio.get_writer(saving_path + "/my_rollout.mp4", fps=20)

for i in range(500):
    action = np.random.randn(*env.action_spec[0].shape) * 0.1
    obs, reward, done, info = env.step(action)  # take action in the environment
    env.render()  # render on display
    
    frame = env.sim.render(
    	camera_name = "robot0_eye_in_hand",
		width=640, height=480,
		depth=False
     )
    video_writer.append_data(frame)

video_writer.close()
print("Video saved as my_rollout.mp4")
