#!/usr/bin/env python3

#Author: Zhiwei

# modify the /etc/core/core.conf 
# set the <custom_services_dir> to the current path
# CORE will first look for __init__.py to load user's service

import os

configFile = '/etc/core/core.conf'
# check for the permission to write configuration file of CORE
try:
	open(configFile, 'a')
except IOError:
	print('Cannot write '+ configFile +'. Maybe you are not using sudo to run?')
	quit()

# change two lines of configuration file
newstr = ''
# os.path.abspath(__file__) can get the <absolute path + filename> of a file
# os.path.dirname(file) can get the <absolute path> of a file
curdir = os.path.dirname(os.path.abspath(__file__))
with open(configFile, 'r') as file:
	for line in file:
		if line.find('custom_services_dir = ') != -1:
			newstr += 'custom_services_dir = ' + curdir + '\n'
			print('Set the <custom_services_dir> to ' + curdir)
		elif line.find('listenaddr = ') != -1:
			newstr += 'listenaddr = ' + '0.0.0.0' + '\n' 
			print('Set the <listenaddr> to ' + '0.0.0.0')
		else:
			newstr += line

# the new file content has been written to the 'newstr', write back to that file
with open(configFile, 'w') as file:
	file.write(newstr)
	print('Write '+ configFile +' successfully!')

# __init__.py ==> preload.py ==> backservice.sh ==> DDFS.py
# MyService class is defined in preload.py
# exactly the running code is in backservice.sh, it is bond in MyService
newstr = ''
with open('preload.py', 'r') as file:
	for line in file:
		if line.find('_startup = ') != -1:
			newstr += '    ' + '_startup = (\'' + curdir + '/backservice.sh\',)' + '\n'
			print('Set the <_startup> to ' + curdir + '/backservice.sh')
		else:
			newstr += line

with open('preload.py', 'w') as file:
	file.write(newstr)
	print('Write '+ 'preload.py' +' successfully!')

# $HOME/.core/nodes.conf
# add MyService to MDR nodes
homedir = os.getenv('HOME')
nodesFile = homedir + '/.core/nodes.conf'
newstr = ''
with open(nodesFile, 'r') as file:
	for line in file:
		if line.find('mdr') != -1:
			newstr += '4 { mdr mdr.gif mdr.gif {zebra OSPFv3MDR vtysh IPForward MyService}  netns {built-in type for wireless routers} }' + '\n'
			print('Add the \'MyService\' to MDR services')
		else:
			newstr += line

with open(nodesFile, 'w') as file:
	file.write(newstr)
	print('Write '+ nodesFile +' successfully!')

# change the ServiceHOME variable within the backservice.sh
# each node in the CORE should specify the location of where real service is at
homedir = os.getenv('HOME')
nodesFile = homedir + '/.core/nodes.conf'
newstr = ''
with open(nodesFile, 'r') as file:
	for line in file:
		if line.find('mdr') != -1:
			newstr += '4 { mdr mdr.gif mdr.gif {zebra OSPFv3MDR vtysh IPForward MyService}  netns {built-in type for wireless routers} }' + '\n'
			print('Add the \'MyService\' to MDR services')
		else:
			newstr += line

with open(nodesFile, 'w') as file:
	file.write(newstr)
	print('Write '+ nodesFile +' successfully!')
