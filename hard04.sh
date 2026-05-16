#!/bin/dash
# hard04: output redirection with >
# Shell writes echo output to file instead of stdout
# A naive translator passes > and filename as arguments to subprocess
echo hello > /tmp/sharpie_hard04_out.txt
cat /tmp/sharpie_hard04_out.txt
