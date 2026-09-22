# Sharpie — Shell-to-Python Translator

**Jiawen Lin · Individual COMP2041 coursework · 2026 T1**

A Python program that translates a restricted subset of Shell syntax into Python source code. This public portfolio summary describes the project at a high level; assignment solutions and teaching materials are not included.

## Skills demonstrated

Python, regular expressions, Shell syntax, source-to-source translation, command-line processing and handling differences between language semantics.

## My implementation

- Translated variable assignments, output statements, conditionals and loops into Python.
- Used regular-expression tokenisation and variable expansion to handle quoting, positional parameters and arithmetic expressions.
- Distinguished numeric and string comparisons in conditional expressions.
- Mapped external commands and command substitution to Python subprocess operations.
- Used filename-pattern expansion and generated required module imports.

## Scope and limitations

This is a translator for a Shell **subset**, not a complete POSIX shell implementation. The source review identified edge cases involving unset variables, unmatched filename patterns, while-read loops and redirection. No claim is made that the course autotests all pass or that all Shell semantics are preserved.

## Source availability

The original implementation remains in a private coursework repository. This summary does not reproduce assignment solutions, test scripts, marking materials or student identifiers. Any source sharing is subject to course permission.

## 中文简介

COMP2041个人课程项目：用 Python 和正则表达式实现 Shell 语法子集到 Python 的源码转译，涉及变量展开、条件与循环、命令调用及文件名模式处理。该展示页用于说明项目范围和技术实践，不公开课程解答，不声称完整兼容 Shell 或全部测试通过。
