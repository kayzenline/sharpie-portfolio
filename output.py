#!/usr/bin/python3 -u
import subprocess




subprocess.run(["touch", "test_file.txt"])
subprocess.run(["ls", "-l", "test_file.txt"])

for course in ["COMP1511", "COMP1521", "COMP2511", "COMP2521"]:  # keyword
subprocess.run(["do"])  # keyword
print(course)  # builtin
subprocess.run(["mkdir", course])  # external command
subprocess.run(["chmod", "700", course])  # external command
