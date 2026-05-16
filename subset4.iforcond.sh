#!/bin/dash

if test -w /dev/null && test -x /dev/null
then
    echo /dev/null is writeable and executable
fi

if grep -Eq $(whoami) enrolments.tsv
then
    echo I am enrolled in COMP2041/9044
fi

