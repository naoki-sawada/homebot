#!/bin/bash

WORK_PATH=$(pwd)

if [ $# -ne 1 ]; then
    echo "Please execute this script with argument"
    exit 1
fi

if [ $1 = "start" ] ; then
    cd ${WORK_PATH}/data && redis-server &
    cd ${WORK_PATH}/src
    sudo python3 controller_server.py &

    while true
    do
        python3 homebot.py
        wait
    done
fi

if [ $1 = "stop" ] ; then
    sudo killall python3 &
    killall auto.sh &
    killall redis-server
fi
