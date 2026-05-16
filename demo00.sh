#!/bin/dash
# Demo 0: variable assignment, echo, and comments
# Tests basic subset 0 features

greeting=Hello
name=World
course=COMP2041
year=2026

echo $greeting $name
echo Welcome to $course
echo Year: $year

# Variable reassignment
x=first
echo x is $x
x=second
echo x is now $x

# Multiple variables in one echo
a=foo
b=bar
c=baz
echo $a $b $c

# Variable reused multiple times
word=repeat
echo $word
echo $word $word
echo $word $word $word

# Empty echo produces a blank line
echo

# Show adjacent variable and text works
prefix=pre
suffix=suf
echo ${prefix}fix
echo pre${suffix}

echo Done
