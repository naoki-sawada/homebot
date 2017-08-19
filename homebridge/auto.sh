#!/bin/bash

while true
do
    trap 'kill $(jobs -p)' EXIT
    homebridge
    wait
done
