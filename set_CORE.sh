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
    cp /etc/core/core.conf /etc/core/core.conf.backup
    sed -i "/custom_services_dir/ s/= .*/= $path/" /etc/core/core.conf
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
    sed -i "/_startup/ s/=(.*)/=(\'$path\/backservice.sh\',)/" $path/preload.py
    if [ $? != 0 ]
    then
        echo "preload.py modified failed. Try to maunally modifify."
        exit 5
    else
        chmod 755 $path/preload.sh
    fi
else
    echo "preload.py missing. Put this file to the current path and try again."
    exit 4
fi

if [ -e "$path/backservice.sh" ]
then
    sed -i "/ServiceHOME/ s/=.*/=$path\/framework/" $path/backservice.sh
    if [ $? != 0 ]
    then
        echo "backservice.sh modified failed. Try to maunally modifify."
        exit 6
    else
        chmod 755 $path/backsevice.sh
    fi
else
    echo "backservice.sh missing. Put this file to the current path and try again."
    exit 7
fi

if [ -e "$HOME/.core/nodes.conf" ]
then
    cp $HOME/.core/nodes.conf $HOME/.core/nodes.conf.backup
    sed -i "4 s/IPForward [A-Za-z]*}/IPForward MyService}/" $HOME/.core/nodes.conf
    if [ $? != 0 ]
    then
        mv $HOME/.core/nodes.conf.backup $HOME/.core/nodes.conf
        echo "$HOME/.core/nodes.conf modified failed. Try to maunally modifify."
        exit 8
    fi
else
    echo "$HOME/.core/nodes.conf missing. Reinstall CORE and try again."
    exit 9
fi

chmod 755 __init__.py

service restart core-daemon restart

# The following modification is for maze file

if [ -e "$path/maze.xml" ]
then
    sed -i "/name=\"icon\"/ s/value=\".*\/icons\//value=\"$path\/icons\//" $HOME/.core/nodes.conf
    sed -i "/wallpaper/ s/{.*\/mazes/{$path\/mazes/" $HOME/.core/nodes.conf
    if [ $? != 0 ]
    then
        echo "$path/maze.xml modified failed. Try to maunally modifify."
        exit 10
    fi
else
    echo "$path/maze.xml missing. Try again."
    exit 11
fi

if [ -e "$path/framwork/core_demo.py" ]
then
    sed -i "/readFromFile/ s/(\'.*\/mazes/(\'$path\/mazes/" $path/framework/core_demo.py
    if [ $? != 0 ]
    then
        echo "$path/framework/core_demo.py modified failed. Try to maunally modifify this line:\n\tmazeMap.readFromFile('<the current path>/maze/2012japan-ef.txt')"
        exit 12
    fi
else
    echo "$path/framework/core_demo.py missing. Try again."
    exit 13

# gethostname() used in the python file sometimes not working if there are no address resolution in /etc/hosts
cp /etc/hosts /etc/hosts.backup
for i in 1 2 3 4
do
    echo "10.0.0.$i\tn$i" >> /etc/hosts
done

echo "The environment is successfully set up for running core_demo.py."
echo "Open maze.xml and click Start Session button to demo."

