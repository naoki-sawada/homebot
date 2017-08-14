#!/bin/bash

WORK_PATH=$(pwd)

deamon() {
    while true
    do
        trap 'kill $(jobs -p)' EXIT
        $1 $2 $3
        wait
    done
}

if [ $# -ne 1 ]; then
    echo "Please execute this script with argument"
    exit 1
fi

if [ $1 = "start" ] ; then
    cd ${WORK_PATH}/data
    deamon redis-server &

    cd ${WORK_PATH}/src
    deamon sudo python3 controller_server.py &
    deamon python3 homebot.py
fi

if [ $1 = "stop" ] ; then
    pkill -f 'auto.sh'
fi

if [ $1 = "deamon-start" ] ; then
    cd ${WORK_PATH}/data
    deamon redis-server &

    cd ${WORK_PATH}/src
    deamon python3 homebot.py
fi

if [ $1 = "deamon-start-nosudo" ] ; then
    cd ${WORK_PATH}/src
    deamon python3 controller_server.py &
fi
