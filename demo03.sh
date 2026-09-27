#!/bin/dash
# Demo 3: double quotes with $var, backtick substitution, echo -n, $# and $@
# Tests subset 3 features

echo "Number of arguments: $#"

echo -n "Hostname: "
hostname=`hostname`
echo "$hostname"

echo -n "Current directory: "
cwd=`pwd`
echo "$cwd"

echo -n "Today's date: "
today=`date`
echo "$today"

if test $# -gt 0
then
    echo "Arguments provided: $@"
    for arg in $@
    do
        echo "  - $arg"
    done
else
    echo "No arguments provided"
fi

user=`whoami`
echo "Running as: $user"

echo -n "Counting: "
for n in 1 2 3 4 5
do
    echo -n "$n "
done
echo

echo "All done"
