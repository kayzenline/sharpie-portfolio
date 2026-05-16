#!/bin/dash

date=$(date +%Y-%m-%d)

echo Hello $(whoami), today is $date

echo "command substitution still works in double quotes: $(hostname)"

echo 'command substitution does not work in single quotes: $(not a command)'

echo "The groups I am part of are $(groups $(whoami))"
