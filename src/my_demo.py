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
from robocasa.environments.kitchen.kitchen import Kitchen
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
# set the camera parameters
renderer_configuration={
    "lookat":[1.2,0.8,1.0],
    "azimuth":180,
    "elevation":-20,
    "distance":22.5}
env=Kitchen(
    robots="GR1FloatingBody",
    #robots="GR1",
    #controller_configs=controller_config,
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    render_camera=None,
    control_freq=20,
    renderer_config=renderer_configuration,
    seed=2,
    init_robot_base_pos="sink",
    style_ids=7,#color of the kitchen 3 is ok 6 is the best until now
)
# reset the environment
env.reset()
#env.sim.data.qpos[2] -= 0.25  # Raise z (height)
print(env.sim.data.qpos[:7])

# get task language (what is??)
lang = env.get_ep_meta()["lang"]
print("Instruction:", lang)
print("Available cameras:", env.sim.model.camera_names)

if video_saving:
    video_writer = imageio.get_writer(saving_path + "/trial.mp4", fps=20) # Create the video writer to save the video as /simulations/trial.mp4

for i in range(500):
    action = np.random.randn(*env.action_spec[0].shape) * 0
    if i == 0:
        print(action)
    obs, reward, done, info = env.step(action)  # take action in the environment
    if i == 0:
        for key in obs:
            print(key)
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
