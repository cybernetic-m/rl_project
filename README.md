# ADD Title

<img src="" alt="Description" width="300" height = "300" />


## ENVIRONMENT INSTALLATION (Robocasa and Robosuite)


1. Install MiniConda: 

Firstly, to install the Robocasa Environment you need to have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html), in order to create a conda environment. These are all the instructions to install conda (if you have conda, you can go to step 2).

(On MacOS): 

In MacOS you need to pay attention to the processor architecture!

If you have INTEL processor, run:
 ```sh 
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
 ```
If you have AppleSilicon processor, run:
 ```sh 
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
 ```
 Refreshing the terminal using:
  ```sh 
 source ~/miniconda3/bin/activate
  ```
Initialize conda for all available shells running the command:
  ```sh 
 conda init --all
  ```

(On Windows):

Open the command prompt and run:

  ```sh 
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
start /wait "" .\miniconda.exe /S
del .\miniconda.exe
  ```

(On Linux):

Open the shell and run:

  ```sh 
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
  ```

Refreshing the terminal using:

  ```sh 
 source ~/miniconda3/bin/activate
  ```

Initialize conda for all available shells running the command:

  ```sh 
 conda init --all
  ```

2. Install Robocasa Environment:

Then you need to install the Robocasa Environment as described in the official [documentation](link1).

The first passage is to create the conda environment

  ```sh 
 conda create -c conda-forge -n robocasa python=3.10
  ```

Then you need to activate the conda env:

 ```sh 
 conda activate robocasa
  ```

Create a directory (you can change the name "robot_at_home") on which you will clone both the environment and this repository:

 ```sh 
 mkdir robot_at_home
 cd robot_at_home
  ```

Clone the robosuite repository:

 ```sh 
git clone https://github.com/ARISE-Initiative/robosuite
cd robosuite
pip install -e .
```

Clone the robocasa repository:

 ```sh 
cd ..
git clone https://github.com/robocasa/robocasa
cd robocasa
pip install -e .
```

Install the package and download the assets:

 ```sh 
python robocasa/scripts/download_kitchen_assets.py   # Caution: Assets to be downloaded are around 5GB.
python robocasa/scripts/setup_macros.py              # Set up system variables.
```

Clone this repository:

 ```sh 
cd ..
git clone https://github.com/cybernetic-m/rl_project.git
```

To run the simulation:

 ```sh 
cd src
python my_demo.py
```

If the simulation does not start, you may need to do ONE of these two commands:
```sh 
pip install imageio[ffmpeg]
```
```sh 
pip install imageio[pyav]
```









## USAGE


## Authors
Massimo Romano (2043836) (https://github.com/cybernetic-m) 

Luca Del Signore (2096442) (https://github.com/Puaison)

## References

[1] [NOME_PAPER1](link1)

[2] [NOME_PAPER2](link2)



