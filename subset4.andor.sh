#!/bin/dash

test -w /dev/null && echo /dev/null is writeable
test -x /dev/null || echo /dev/null is not executable
