import h5py
import matplotlib.pyplot as plt
import numpy as np
import json


def inspData(path, demo_name='demo_7'):
    with h5py.File(path, 'r') as file:
        demo_group = f"data/{demo_name}"
        if demo_group in file:
            print(f"Contents of '{demo_group}':")
            file[demo_group].visititems(print_structure)
        else:
            print(f"Demo '{demo_group}' not found in file.")


def print_structure(name, obj):
    print(name)

def showImage(img,flip=False):
    if flip:
        img = np.flipud(img)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def getObs(dataset_path, obs_dict, demo_name='demo_7'):
    
    f = h5py.File(dataset_path, 'r')
    demo = f['data'][demo_name]

    # Read the observations
    obs = demo['obs']

    # Extracting images
    left_image = obs['robot0_agentview_left_image'][:]
    right_image = obs['robot0_agentview_right_image'][:]
    hand_image = obs['robot0_eye_in_hand_image'][:]

    # Extracting joint positions and velocities
    joint_pos = obs['robot0_joint_pos'][:]
    joint_pos_sin = obs['robot0_joint_pos_sin'][:]
    joint_pos_cos = obs['robot0_joint_pos_cos'][:]
    joint_vel = obs['robot0_joint_vel'][:] 

    # Extracting gripper positions and velocities
    gripper_pos = obs['robot0_gripper_qpos'][:]
    gripper_vel = obs['robot0_gripper_qvel'][:] 

    # Extracting base data
    base_pos = obs['robot0_base_pos'][:]
    base_quat = obs['robot0_base_quat'][:]
    base2eef_pos = obs['robot0_base_to_eef_pos'][:]
    base2eef_quat = obs['robot0_base_to_eef_quat'][:]

    # Extracting end effector data
    eef_pos = obs['robot0_eef_pos'][:]
    eef_quat = obs['robot0_eef_quat'][:]

    return left_image