# Micromouse Maze Coop-Search 

Target: Using micromouses to discover a maze in a cooperated way. Both in software emulation and also hardware implementation.

## Runtime Environment

### Software

1. Installation of CORE

$ sudo apt-get install core-network

$ sudo apt-get install quagga

This project needs wireless mesh network, please also install quagga-mr:

$ wget https://downloads.pf.itd.nrl.navy.mil/ospf-manet/quagga-0.99.21mr2.2/quagga-mr_0.99.21mr2.2_amd64.deb

$ sudo dpkg -i quagga-mr_0.99.21mr2.2_amd64.deb

2. Installation of Python3

If you have not set up Python Environment, please install it via Python official webpage. Generally with a Linux system, it is installed by default.

https://www.python.org/about/gettingstarted/

3. Installation of python3 tkinter

$ sudo apt-get install python3-tk

### Hardware

1. LEGO EV3 robot ensemble:

Please have a LEGO EV3 micromouse robot ensembled. To make the main function which is Right.py work, you need to put the Gyro sensor in a stable place to avoid viberations, and make the side ultrasonic sensors as low as possible, while not touching the ground. You can also have your own design of sensors you want to use, and the structure of the robot, but the major concerns are where Gyro and ultrasonic sensors are put.

2. Hardware runtime preparation:

Please make sure the robot is with EV3dev. You can find instructions on installing EV3dev and using this system from your computer on their official website:

http://www.ev3dev.org/docs/getting-started/

3. Please copy all files from ./Hardware into a custom folder in EV3. SCP is a convenient command in this situation.

4. If you want to run the codes directly from the brick, make sure to give full privilege to the file you want to use by this command.

$ chmod +x "filename"

For example, if you want to run rightwall follower, please run 

$ chmod +x Right.py

And click the Right.py while finding this file on the screen of the brick.

5. If you want to run the codes on an ssh connection, please use

$ python3 "filename"

Extra caution: For any codes using Gyro sensor, please make sure that it is started from complete still. Don't move the robot while starting the codes.

## Decentralized CORE and Code Set Up

Change mazefile parameter in config.ini soft section and change the wallpaper to the maze you want to use. For example: if you want to run on 2010japan maze, then change the parameter specified to 

mazefile: "Your full path of this folder"/mazes/2010japan.txt

#### Setting up CORE

$ sudo nano /etc/core/core.conf

change the line of custom_services_dir to: custom_services_dir = "full path of this folder"

$ sudo nano ./preload.py
 
_startup = ('"full path of this folder"/backservice.sh',) 

$ sudo nano /home/student/.core/nodes.conf

change line: 4 { mdr mdr.gif mdr.gif {zebra OSPFv3MDR vtysh IPForward MyService}  netns {built-in type for wireless routers} }

$ sudo nano ./backservice.sh

change export ServiceHOME="full path of this folder"

$ sudo nano ./config.ini

change mazefile location to: "full path of this folder"/mazes/2012japan-ef.txt

$ sudo nano ./maze.xml

change all file locations to "full path of this folder".

#### Set file permission

$ chmod 755 __init__.py

$ chmod 755 preload.py

$ chmod 755 backservice.sh

You don't need to re-set this setting every time you run this demo once set.

$ sudo service core-daemon restart

$ core-gui

Then open maze.xml, edit all icon, wallpaper file paths into your own full path (CORE won't recognize), finally open the edited xml file in your core-gui.

## How to Run This Project:

### Decentralized Software

$ python3 host.py soft

Then click "Start the session" button of CORE.

You will see 1 window showing the total exploration.

### Hardware

To test all sensors, you can run the test files by running these commands in ssh environment:

$ python3 "filename"

You can see a full list of testing files and main files in ./Hardware

To run the Rightwall follower, please run Right.py directly from the brick.

To run the decentralized DFS, please run DDFS.py from the terminals, and you can also run host.py to see a visualization of explorations.

$ python3 DDFS.py

For both of the micromouses.

If you want to see the gui, please run host.py on host machine before running DDFS.

$python3 host.py hard

## Videos for Demo:
Full Hardware-based demo: https://drive.google.com/file/d/0B44CsSBStR5PU052SXZsMGpiaU0/view 

3-minute Hardware-based Demo: https://youtu.be/_PrOHVuoXyI

Full CORE-based demo: https://youtu.be/AusQtYacz70

Hardware-based demo for two agents:
https://drive.google.com/open?id=0B44CsSBStR5PdS0tUTJuSENnaUE
