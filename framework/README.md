## Module Description
    Micromouse
    ├── backservice.sh          //starting program in MyService
    ├── __init__.py             //module automatically read by CORE when core-gui opens
    ├── preload.py              //MyService class as an extra service that can be added into CORE, pointered by __init__.py
    │                             and it specifies the starting program. Here it's the backservice.sh
    │                             Calling Relations: CORE -> __init__.py -> preload.py -> backservice.sh -> core_demo.py
    ├── framework               //framework written in Python3
    │   ├── controller.py       //Control Layer: MotorController, SensorController, COREController, 
    │   │                                        EV3MotorController, EV3SensorController
    │   ├── core_demo.py        //Example of demonstrating multi-agent DFS in CORE
    │   ├── demo.py             //Example of demonstrating multi-agent DFS in EV3-Lego robot
    │   ├── display.py          //GUI program showing the discovery of micromouse in real maze
    │   ├── map_painter.py      //The painting tool for presenting the maze written
    │   ├── map.py              //Active Layer: MazeMap, which contains the classes of Map and Cell
    │   ├── mouse.py            //The Micromouse class for managing all the modules
    │   ├── README.md
    │   ├── strategy.py         //Active Layer: Various of testing cases of Strategy
    │   └── task.py             //Task Layer: TaskLoader, Task, WallDetector, CommandTranslator, NetworkInterface
    ├── icons                   //folder for icons of mice shown in CORE
    │   ├── robotblu.png
    │   └── (...png files...)
    ├── mazes                   //folder for maze examples that png files are pictures for backgrounds and txt files 
    │   │                         are corresponding maze presented in (*, |, etc) which should be parsed by a function. 
    │   │                         See map.py -> readFromFile as a parser example.
    │   ├── 2009japan-b.png
    │   ├── 2009japanb.txt
    │   ├── 2010japan.png
    │   ├── 2010japan.txt
    │   └── (...png file and txt file...)
    ├── maze.xml                //layout file opened and saved by CORE
    └── old_version             //deprecated code, please ignore it
        ├── stop.py
        └── (...other code files...)


## Tutorial
To make a new algorithm for running a micromouse, you need to do the following steps:
1. Write your own strategy inheriting from class Strategy and overrides the function checkFinished() and function go().
2. Write your own motor controller inheriting from class Motor Controller and sensor controller inheriting from class Sensor Controller for your hardware - robot. You need to overrides the functions: turnLeft(), turnRight(), turnAround(), goStraight() in Motor Controller and senseLeft(), senseRight(),  senseFront(), senseBack() from Sensor Controller
3. Write a starting class or function to create a micromouse to run.

## Example
DFS algorithm for one mouse traversing the maze
 
For a basic DFS algorithm for only one mouse running in the maze, you can write a Strategy called ‘StrategyDFS’ which inherits the Strategy class and overrides the function ‘checkFinished’ and function ‘go’. The function ‘checkFinished’ is called because the Task Loader repeatedly check whether the task applying the strategy has finished after calling function ‘go’. The main structure of function ‘run’ of Task Loader is as follows:

    def run():
        while not strategy.checkFinished():
            strategy.go()

**Step 1**: Write your own strategy inheriting from class Strategy and overrides the function checkFinished() and function go().

Let’s suppose we write a class inherits from Strategy as follows: (copied from strategy.py -> StrategyTestDFS)

    class StrategyTestDFS(Strategy):
        mouse = None    # It is necessary to keep a mouse instance as a member variant of Strategy class
        isVisited = []  # The isVisited is a two-dimensional array marking which cell has been visited by itself or other robots
        path = []       # The path is a stack to track the path that mouse goes through
        isBack = False  # Use a flag to mark whether the mouse has gone back to the origin
        network = None  # The instance of NetworkInterface

        def __init__(self, mouse):  # Called when Micromouse add a task with this strategy and it passes instance of itself as the second argument
            self.mouse = mouse
            self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
            self.isVisited[self.mouse.x][self.mouse.y] = 1  # 1 marks that isVisited[x][y] has been visited

        def checkFinished(self):
            return self.isBack      # The terminating condition is that isBack = 1

        def go(self):
            # Sequentially check four directions, go if there is no wall and has not been visited before
            if not self.mouse.canGoLeft() and not self.isVisited[self.mouse.x-1][self.mouse.y]:
                self.path.append([self.mouse.x, self.mouse.y])
                self.isVisited[self.mouse.x-1][self.mouse.y] = 1
                self.mouse.goLeft()
            elif not self.mouse.canGoUp() and not self.isVisited[self.mouse.x][self.mouse.y-1]:
                self.path.append([self.mouse.x, self.mouse.y])
                self.isVisited[self.mouse.x][self.mouse.y-1] = 1
                self.mouse.goUp()
            elif not self.mouse.canGoRight() and not self.isVisited[self.mouse.x+1][self.mouse.y]:
                self.path.append([self.mouse.x, self.mouse.y])
                self.isVisited[self.mouse.x+1][self.mouse.y] = 1
                self.mouse.goRight()
            elif not self.mouse.canGoDown() and not self.isVisited[self.mouse.x][self.mouse.y+1]:
                self.path.append([self.mouse.x, self.mouse.y])
                self.isVisited[self.mouse.x][self.mouse.y+1] = 1
                self.mouse.goDown()
            else:
            # When four directions are either wall or visited, go back one step by popping up path stack
                if len(self.path) != 0:
                    x, y = self.path.pop()
                    if x < self.mouse.x:
                        self.mouse.goLeft()
                    elif x > self.mouse.x:
                        self.mouse.goRight()
                    elif y < self.mouse.y:
                        self.mouse.goUp()
                    elif y > self.mouse.y:
                        self.mouse.goDown()
                else:
                # The stack being empty means that mouse has gone back to the origin 
                    self.isBack = True

            sleep(0.5) # Delay for better demonstration

**Step 2**: Write your own motor controller inheriting from class Motor Controller and Sensor Controller inheriting from class Sensor Controller for your hardware - robot. You need to overrides the functions: turnLeft(), turnRight(), turnAround(), goStraight() in Motor Controller and senseLeft(), senseRight(),  senseFront(), senseBack() from Sensor Controller.

If you are going to demonstrate in CORE or EV3, you can directly utilize the *COREController* and *EV3MotorController*, *EV3SensorController* in *controller.py* and skip this step. The mentioned functions are atomic procedures for Task Layer to call so that when writting a strategy, you can just call senseWalls(), goLeft(), goRight(), goUp() or goDown() in Micromouse class without considering the direction it faces and writing code of manipulating the hardware.

**Step 3**: Write a starting function to create a micromouse to run.

    from map import Map;
    from mouse import Micromouse;
    from strategy import StrategyTestDFS;

    def myMouse():
        mazeMap = Map(16, 16, 40, 40)                   # Specify the size of maze map, ignore the last two arguments.
        micromouse = Micromouse(mazeMap)                # Create a micromouse with the empty map
        micromouse.setInitPoint(0, 0)                   # Tell the micromouse the origin coordinate
        micromouse.addTask(StrategyTestDFS(micromouse)) # Use the created Strategy with this micromouse instance to add a Task
        micromouse.run()                                # The TaskLoader will run the tasks you have added

## Demonstrations

Please read core_demo.py and demo.py to see how to use the framework. 
core_demo.py is used for running the DFS in CORE. The set-up steps are as follows:

### Run in CORE

First make sure that CORE has been installed. If you have not installed CORE, follow https://docs.google.com/document/d/1LPkPc2lbStwFtiukYfCxhcW7KewD028XzNfMd20uFFA/ to install.

Download the Micromouse framework from https://github.com/eniacluo/Micromouse. DO NOT only download the framework folder because the maze file examples are not included.

Replace some lines of following files corresponding to the path. DO NOT make your path of Micromouse framework too long and sometimes it does not work if there are *special characters* like underscore or slash in the full path. 

    $ cd "path you downloaded"/Micromouse

    $ sudo nano /etc/core/core.conf

Uncomment the line of custom_services_dir and set:

custom_services_dir = **"full path of this folder"**  
listenaddr = **0.0.0.0**

    $ nano ./preload.py
 
_startup = ('**"full path of this folder"**/backservice.sh',) 

    $ nano $HOME/.core/nodes.conf

change line: 4 { mdr mdr.gif mdr.gif {zebra OSPFv3MDR vtysh IPForward **MyService**}  netns {built-in type for wireless routers} }

    $ nano ./backservice.sh

export ServiceHOME=**"full path of this folder"**/framework

    $ nano ./maze.xml

change paths of 4 icons:

name="icon" value="**"full path of this folder"**/icons/robot\*\*\*.png"

change path of wallpaper:

wallpaper {**"full path of this folder"**/mazes/2012japan-ef.png}

#### Set file permission

    $ chmod 755 \_\_init\_\_.py

    $ chmod 755 preload.py

    $ chmod 755 backservice.sh

You don't need to re-set this setting every time you run this demo once set.

    $ sudo service core-daemon restart

    $ core-gui

Then open maze.xml, click the **Start session** button.

### Run in EV3

    $ nano demo.py

Change the size to match your maze:

    mazeMap = Map(8, 8, 40, 40)

Specify the direction it faces at the beginning, *UP* is default:

    micromouse.setInitDirection("UP")

Set the initial coordinate x, y:

    micromouse.setInitPoint(2, 7)

Add the task with written Strategy instance:

    micromouse.addTask(StrategyTestMultiDFS(micromouse))

Download the framework folder into the EV3 robot.

Press the center button of EV3 to boot and wait until the main menu appears. Choose File *browser->demo.py*. Click the center button to start. The light may turn orange if everything is good. It is not necessarily that two mice start at exact the same time.

## Documentation for framework

The detailed descriptions including the architecture are provided in https://docs.google.com/document/d/1im-nFw-iO0sKvpq5XH-agR5obBuFwbSLMbefUWsbebQ/edit?usp=sharing. If you have any questions, please mail to eniacsimon@gmail.com to get help.
