$ cd "path you downloaded"/Micromouse

Here gives the configurations of demonstrating core_demo.py which is an coordinated DFS. 

## Step 1: Let the MDR node runs Micromouse automatically by adding a customized service.

$ sudo nano /etc/core/core.conf

Uncomment the line of custom_services_dir and set:

custom_services_dir = **"full path of this folder"**  
listenaddr = **0.0.0.0**

$ nano ./preload.py
 
_startup = ('**"full path of this folder"**/backservice.sh',) 

$ nano ./backservice.sh

export ServiceHOME=**"full path of this folder"**/framework

$ nano ~/.core/nodes.conf

change line: 4 { mdr mdr.gif mdr.gif {zebra OSPFv3MDR vtysh IPForward **MyService**}  netns {built-in type for wireless routers} }

$ chmod 755 \_\_init\_\_.py preload.py backservice.sh

**To check whether the Micromouse service has been added, restart core-daemon and open CORE:**

$ sudo service core-daemon restart

$ core-gui

Add a MDR node into the canvas and right-click the node, click *Serivce*. Now you can see *MyService* is appearing in the column of *Utility* and it has been enabled. Click the tool icon on the right of *MyService* and click the *Startup/shutdown* tab, you can see the complete path of *backservice.sh* is shown in the middle *Startup Commands* list. That marks the correct configurations of CORE.

## Step 2: Modify paths within maze description file.

$ nano ./maze.xml

change paths of 4 icons:

name="icon" value="**"full path of this folder"**/icons/robot\*\*\*.png"

change path of wallpaper:

wallpaper {**"full path of this folder"**/mazes/2012japan-ef.png}

$ nano framework/core_demo.py

change path of maze file:

mazeMap.readFromFile('**"full path of this folder"**/mazes/2012japan-ef.txt')

#### Step 3: Open CORE to demonstrate:

$ core-gui

Then open maze.xml, click the **Start session** button.
