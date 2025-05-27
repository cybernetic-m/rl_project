import h5py
import matplotlib.pyplot as plt
import numpy as np

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
