# This file is for setting up the env of running Micromouse core_demo.py
# The configurations file modified in this script will be backuped.
# Author: Zhiwei Luo
# Email: eniacsimon@gmail.com

pri=`whoami`

if [ $pri != "root" ]
then
    echo "Run the script using sudo."
    exit 1
fi

path=`pwd`
echo "The current folder is $path."

if [ -e "/etc/core/core.conf" ]
then
    if [ ! -e "/etc/core/core.conf.backup" ]
    then
        cp /etc/core/core.conf /etc/core/core.conf.backup
    fi
    sed -i "/custom_services_dir/ s@= .*@= $path@" /etc/core/core.conf
    sed -i "/custom_services_dir/ s@[# ]*@@" /etc/core/core.conf
    sed -i "/listenaddr/ s/= .*/= 0.0.0.0/" /etc/core/core.conf
    if [ $? != 0 ]
    then
        echo "CORE configuration file modified failed. Try to maunally modifify."
        exit 2
    fi
else
    echo "The CORE configuration file '/etc/core/core.conf' does not exist. Reinstall CORE and try again."
    exit 3
fi

if [ -e "$path/preload.py" ]
then
    sed -i "/_startup/ s@(.*)@(\'$path\/backservice.sh\',)@" $path/preload.py
    if [ $? != 0 ]
    then
        echo "preload.py modified failed. Try to maunally modifify."
        exit 5
    else
        chmod 755 "$path/preload.py"
    fi
else
    echo "preload.py missing. Put this file to the current path and try again."
    exit 4
fi

if [ -e "$path/backservice.sh" ]
then
    sed -i "/ServiceHOME/ s@=.*@=$path\/framework@" $path/backservice.sh
    if [ $? != 0 ]
    then
        echo "backservice.sh modified failed. Try to maunally modifify."
        exit 6
    else
        chmod 755 "$path/backservice.sh"
    fi
else
    echo "backservice.sh missing. Put this file to the current path and try again."
    exit 7
fi

if [ -e "$HOME/.core/nodes.conf" ]
then
    if [ ! -e "$HOME/.core/nodes.conf.backup" ]
    then
        cp $HOME/.core/nodes.conf $HOME/.core/nodes.conf.backup
    fi
    sed -i "6 s/IPForward[ A-Za-z]*}/IPForward MyService}/" $HOME/.core/nodes.conf
    if [ $? != 0 ]
    then
        mv $HOME/.core/nodes.conf.backup $HOME/.core/nodes.conf
        echo "$HOME/.core/nodes.conf modified failed. Try to maunally modifify."
        exit 8
    fi
else
    echo "$HOME/.core/nodes.conf missing. Open core-gui and it may generate this file. Otherwise, reinstall CORE and try again."
    exit 9
fi

if [ -e "$path/__init__.py" ]
then
    chmod 755 __init__.py
else
    echo "__init__.py is missing. Try again later."
    exit 14
fi

echo "Completed setting up the CORE configuration files. Restart daemon now."
service core-daemon restart
if [ $? != 0 ]
then
    echo "service restart failed. Did you start core-daemon service? Start manually: sudo service core-daemon start. You can also reinstall CORE and try again."
    exit 15
fi

# The following modification is for maze file

if [ -e "$path/maze.xml" ]
then
	version=$(core-daemon -h | grep "CORE daemon" | cut -f3 -d' ')
	echo "Your CORE daemon version is $version."
	if { [ $version = "v.4.6" ] || [ $version = "v.4.7" ] ;} && [ -e "maze_v4.6.xml" ]
	then
		mv maze.xml maze_v4.8.xml
		mv maze_v4.6.xml maze.xml
		sed -i "/icon/ s@value=\".*\/icons\/@value=\"$path\/icons\/@" "$path/maze.xml"
		sed -i "/wallpaper/ s@wallpaper {.*\/mazes@wallpaper {$path\/mazes@" "$path/maze.xml"
	elif [ $version = "v.4.8" ]
	then
		sed -i "/icon/ s@icon=\".*\/icons\/@icon=\"$path\/icons\/@" "$path/maze.xml"
    	sed -i "/wallpaper/ s@wallpaper {.*\/mazes@wallpaper {$path\/mazes@" "$path/maze.xml"
	else
		echo "The CORE daemon is too old. You may need to install >= v4.6."
	fi
    if [ $? != 0 ]
    then
        echo "$path/maze.xml modified failed. Try to maunally modifify."
        exit 10
    fi
else
    echo "$path/maze.xml missing. Try again."
    exit 11
fi

if [ -e "$path/framework/core_demo.py" ]
then
    sed -i "/readFromFile/ s@(.*\/mazes@(\'$path\/mazes@" "$path/framework/core_demo.py"
    if [ $? != 0 ]
    then
        echo "$path/framework/core_demo.py modified failed. Try to maunally modifify this line:\n\tmazeMap.readFromFile('<the current path>/maze/2012japan-ef.txt')"
        exit 12
    fi
else
    echo "$path/framework/core_demo.py missing. Try again."
    exit 13
fi

# gethostname() used in the python file sometimes not working if there are no address resolution in /etc/hosts
if [ ! -e "/etc/hosts.backup" ]
then
    cp /etc/hosts /etc/hosts.backup
fi

if [ -z "`cat /etc/hosts | grep 10.0.0.1`" ]
then
    for i in 1 2 3 4
    do
        echo "10.0.0.$i\tn$i" >> /etc/hosts
    done
fi

echo "The environment is successfully set up for running core_demo.py."
echo "Open maze.xml and click Start Session button to demo."

