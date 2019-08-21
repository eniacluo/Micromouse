## Module Description
    Micromouse
    ├── backservice.sh          //starting program in MyService
    ├── __init__.py             //module automatically read by CORE when core-gui opens
    ├── preload.py              //MyService class as an extra service that can be added into CORE, pointered by __init__.py
    │                             and it specifies the starting program - backservice.sh
    │                             Calling Relations: CORE -> __init__.py -> preload.py -> backservice.sh -> demo_core.py
    ├── framework               //framework written in Python3
    ├── icons                   //folder for icons of mice shown in CORE
    ├── mazes                   //folder for maze examples that png files are pictures for backgrounds and txt files 
    │                             are corresponding maze presented in (*, |, etc) which should be parsed by a function. 
    │                             See map.py -> readFromFile as a parser example.
    ├── maze.xml                //layout file opened and saved by CORE v4.8
    ├── maze_v4.6.xml           //layout file opened and saved by CORE v4.6
    ├── old_version             //deprecated code, please ignore it
    │   ├── stop.py
    │   └── (...other code files...)
    └── README.md

## Documentations
Refer to README.md of [framework](https://github.com/eniacluo/Micromouse/tree/master/framework).