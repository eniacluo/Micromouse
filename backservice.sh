#!/bin/bash
export ServiceHOME=/home/zhiwei/Micromouse
homefolder="$(pwd)"
#homefolder="/tmp/pycore.55045-n1.conf"
nodeid=`echo "$homefolder" | grep -Eo "[[:digit:]]+" | tail -n1`

#sleep certain period to wait for routing complete
#sleep 8

#monitor traffic through upd port 50000 for 10 seconds
#duration=10

#-E ntime
#    Terminate after ntime seconds
#-c npacket
#    Terminate program after reading npacket packets. 

# -p prot[,port..][:prot[,port..]..
#    Only dump packets with specific protocols and ports. For example, -p1:6:17 dumps only packets with protocols 1 (icmp), 6 (tcp) and 17 (udp). You can also break down udp and tcp packets by port numbers - for example -p1:6,21,23 will only dump icmp packets, ftp packets (protocol 6, port 21) and telnet packets (protocol 6, port 23). 
# however, it has a big difference from -f "  ", see http://ipaudit.sourceforge.net/documentation/manpages/ipaudit.html. Thus we do not use it.

# For UDP broadcast, all packet headers have total size 42 bytes, to get real payload size, use packetsize-42 
#  ipaudit -p17 -E $duration -t -S -m eth0 -o traffic.log &

# ipaudit -f "udp 50000" -E $duration -t -S -m eth0 -o traffic.log &

# stdbuf -oL nohup is used to enable redirect flush once per line

cp $ServiceHOME/config.ini .
echo $ServiceHOME/DDFS.py >> tmp.log
stdbuf -oL nohup $ServiceHOME/DDFS.py soft >> send.log



# sleep duration time  + 1 seconds until ipaudit completes
#sleep $((duration+2))


#if [ ! -d $CoreHOME/trafficlog ]; then
#  mkdir $CoreHOME/trafficlog
#fi

# add nodeid in the beginning of each line
#sed "s/^/$nodeid /" traffic.log > modtraffic.log
# merge and copy log file to one permanent location
#cat modtraffic.log >> $CoreHOME/trafficlog/traffic.log

