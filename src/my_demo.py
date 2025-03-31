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

if sys.platform.startswith("win"):
    print("\nYou are on Windows!\n")
    video_saving = False # Not saving video
elif sys.platform == "darwin":
    print("\nYou are on MacOS\n")
    video_saving = True
elif sys.platform == "linux":
    print("\nYou are on Linux\n")
    video_saving = True # For Linux systems (To test?)

# choose random task
env_name = np.random.choice(list(ALL_KITCHEN_ENVIRONMENTS))  # name of the kitchen env

env = create_env(
    env_name=env_name, # Name of the env (Ex. ??)
    render_offscreen=video_saving, # If you want to save videos (a feature available only in MacOS and Linux probably)
    render_onscreen=True,      # To render live simulations
    camera_names=['robot0_eye_in_hand'] # ??
)

# reset the environment
env.reset()


# get task language (what is??)
lang = env.get_ep_meta()["lang"]
print("Instruction:", lang)

if video_saving:
    video_writer = imageio.get_writer(saving_path + "/trial.mp4", fps=20) # Create the video writer to save the video as /simulations/trial.mp4

for i in range(500):
    action = np.random.randn(*env.action_spec[0].shape) * 0.1
    obs, reward, done, info = env.step(action)  # take action in the environment
    env.render()  # render on display
    
    if video_saving:
        frame = env.sim.render(
            camera_name = "robot0_eye_in_hand",
            width=640, height=480,
            depth=False
        )
        video_writer.append_data(frame)

if video_saving:
    video_writer.close()
    print("Video saved as trial.mp4")
