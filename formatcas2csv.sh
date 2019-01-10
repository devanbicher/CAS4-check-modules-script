#!/bin/bash

time=$(date +%m%d%y%H%M)

cp cas2modules.csv "modulelistbackups/cas2modules-$time.csv"

sed 's/  \+/,/g' cas2modules.txt | sed 's/,$//g' | grep -v "Package,Name,Status,Version" > cas2modules.csv
