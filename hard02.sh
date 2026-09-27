#!/bin/dash
# hard02: while read loop reads lines from stdin until EOF
# Shell: reads each line into var, loop exits at EOF
# A naive translator produces invalid Python for the while condition
while read line
do
    echo got: $line
done
