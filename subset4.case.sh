#!/bin/dash

case $# in
    0)
        echo no arguments
        ;;
    1)
        echo one argument
        ;;
    2|3|4)
        echo some arguments
        ;;
    *)
        echo many arguments
        ;;
esac
