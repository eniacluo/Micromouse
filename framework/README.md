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

Let’s suppose we write a class inherits from Strategy as follows:

    class StrategyTestDFS(Strategy):
        mouse = None
        isBack = False

        def __init__(self, mouse):
            self.mouse = mouse

        def checkFinished(self):
            return self.isBack

        def go(self):
            if not self.mouse.leftIsWall() and not self.mouse.visitedLeft():
                self.mouse.goLeft()
            elif not self.mouse.UpIsWall() and not self.mouse.visitedUp():
                self.mouse.goUp()
            elif not self.mouse.RightIsWall() and not self.mouse.visitedRight():
                self.mouse.goRight()
            elif not self.mouse.DownIsWall() and not self.mouse.visitedDown():
                self.mouse.goDown()
            else:
                if len(self.mouse.path) != 0:
                    x, y = self.mouse.path.pop()
                    self.mouse.goBack(x, y)
                else:
                    self.isBack = True

            print(self.mouse.x, self.mouse.y)


For starting a user defined micromouse, you can write a function to run like follows:

    def myMouse():
        mazeMap = Map(16, 16, 40, 40)
        mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/2009japanb.txt')
        micromouse = Micromouse(mazeMap)
        micromouse.setInitPoint(0, 0)
        micromouse.addTask(StrategyTestDFS(micromouse))
        micromouse.run()

## Sample file

Please read core_demo.py and demo.py to see how to use the framework. 
core_demo.py is used for running the DFS in CORE. The set-up steps are as follows:

### Run in CORE

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

demo.py is used for running in EV3 in real maze.

### Run in EV3

Set up wifi: 
SSID: [sensorwebprinter]
Password: [sensorweb] 

Two mice have been setup to automatically connect this wifi. Check their IP addresses, they will be 192.200.1.100 and 192.200.1.101.
Put mouse No.1 into the maze at (2, 0) and make it face to the LEFT. Put mouse No.2 into the maze at (2, 7) and make it face to UP. See the following demonstration:
    
Press the center button of EV3 to boot and wait until the main menu appears. Choose File browser->demo.py. Click the center button to start. The light may turn orange if everything is good. It is not necessarily that two mice start at the exact the same time.

## Documentation for framework

The detailed descriptions including the architecture are provided in https://docs.google.com/document/d/1im-nFw-iO0sKvpq5XH-agR5obBuFwbSLMbefUWsbebQ/edit?usp=sharing. If you have any questions, please mail to eniacsimon@gmail.com to get help.
