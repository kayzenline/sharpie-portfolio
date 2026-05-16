#!/bin/dash
# hard00: undefined variable expands to empty string in shell
# A naive translator produces a Python NameError instead
echo $undefined_variable
echo done
