#!/bin/dash
# Demo 1: for loops, globbing, external commands, read, exit
# Tests subset 1 features

echo Counting to five:
for i in 1 2 3 4 5
do
    echo $i
done

echo
echo Days of the working week:
for day in Monday Tuesday Wednesday Thursday Friday
do
    echo $day
done

echo
echo Creating test directories:
for dir in alpha beta gamma
do
    mkdir $dir
    chmod 755 $dir
    echo Created directory: $dir
done

echo
echo Shell scripts in current directory:
for f in *.sh
do
    echo $f
done

echo
echo What is your name:
read username
echo Hello $username

echo
echo Listing current directory:
ls -1 .

echo
echo Cleaning up:
for dir in alpha beta gamma
do
    chmod 700 $dir
done

echo All done
exit 0
