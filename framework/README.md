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

Please read and run sample.py to see how to use the framework. The detailed descriptions including the architecture are provided in https://docs.google.com/document/d/1im-nFw-iO0sKvpq5XH-agR5obBuFwbSLMbefUWsbebQ/edit?usp=sharing. If you have any questions, please mail to eniacsimon@gmail.com to get help.
