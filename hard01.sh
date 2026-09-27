#!/bin/dash
# hard01: glob pattern with no matches
# Shell keeps the literal pattern as the loop word;
# Python glob.glob returns [], so the loop body never runs
for f in *.no_file_has_this_extension_xyz
do
    echo $f
done
echo done
