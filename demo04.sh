#!/bin/dash
# Demo 4: $(()) arithmetic, $() substitution, [ ] test conditions
# Tests subset 4 features

a=10
b=3

echo "Arithmetic with a=$a and b=$b:"
echo "  $a + $b = $((a + b))"
echo "  $a - $b = $((a - b))"
echo "  $a * $b = $((a * b))"
echo "  $a / $b = $((a / b))"
echo "  $a % $b = $((a % b))"

echo
echo "Squares from 1 to 8:"
i=1
while [ $i -le 8 ]
do
    sq=$((i * i))
    echo "  $i * $i = $sq"
    i=$((i + 1))
done

echo
echo "Working directory via command substitution:"
cwd=$(pwd)
echo "  $cwd"

echo
echo "Even numbers from 2 to 20:"
n=2
while [ $n -le 20 ]
do
    echo -n "$n "
    n=$((n + 2))
done
echo

echo
echo "Fibonacci sequence (first 10):"
p=0
q=1
i=0
while [ $i -lt 10 ]
do
    echo -n "$p "
    next=$((p + q))
    p=$q
    q=$next
    i=$((i + 1))
done
echo

echo "Done"
