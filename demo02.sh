#!/bin/dash
# Demo 2: command-line args, if/elif/else, while, test, single quotes
# Tests subset 2 features

echo 'Script started'
echo Script name: $0

if test $# -eq 0
then
    echo 'No arguments given'
    exit 1
fi

n=$1

if test $n -lt 0
then
    echo 'Negative number'
elif test $n -eq 0
then
    echo 'Zero'
elif test $n -lt 10
then
    echo 'Single digit'
elif test $n -lt 100
then
    echo 'Two digits'
else
    echo 'Large number'
fi

echo
echo Counting up to $n:
i=1
while test $i -le $n
do
    echo $i
    i=$((i + 1))
done

echo
echo Counting down from $n:
i=$n
while test $i -ge 1
do
    echo $i
    i=$((i - 1))
done

echo 'Done'
