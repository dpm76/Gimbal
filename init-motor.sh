#!/bin/bash

#cpufreq-set -g performance

echo cape-universaln > /sys/devices/bone_capemgr.*/slots
config-pin P8.19 pwm
config-pin P8.13 pwm
config-pin P9.16 pwm
config-pin P9.14 pwm

echo 3 > /sys/class/pwm/export
echo 4 > /sys/class/pwm/export
echo 5 > /sys/class/pwm/export
echo 6 > /sys/class/pwm/export
