#!/usr/bin/env python3
"""
 sharpie.py - A simple translator from Shell to Python
 Usage: sharpie.py <input.sh >output.py
 written by Jiawen Lin(z5647814)
"""

import sys
import re

def expand_dollar(s):
	"""
	Expand $VAR and ${VAR} in the string s, handle $# and $@.
	Return the expanded string and a boolean indicating if any
	expansion was done.
	"""
	had = [False]
	def replacer(m):
		if m.group('lb'):
			return '{{'
		if m.group('rb'):
			return '}}'
		if m.group('arith') is not None:
			had[0] = True
			return '{' + arith_to_py(m.group('arith')) + '}'
		if m.group('backtick') is not None:
			had[0] = True
			return '{' + cmd_subst_to_py(m.group('backtick')) + '}'
		if m.group('dolparen') is not None:
			had[0] = True
			return '{' + cmd_subst_to_py(m.group('dolparen')) + '}'
		if m.group('argc'):
			had[0] = True
			return '{len(sys.argv) - 1}'
		if m.group('argv'):
			had[0] = True
			return "{' '.join(sys.argv[1:])}"
		var = m.group('bvar') or m.group('var')
		had[0] = True
		if var.isdigit():
			return '{sys.argv[' + var + ']}'
		return '{' + var + '}'
	# Match shell variable expansions and command substitutions:
	# arith: $((...)) arithmetic operations
	# backtick / dolparen: `...` or $(...)
	# bvar / var: ${VAR} or $VAR variables
	# argc / argv: $# argument count, $@/$* all arguments
	# lb / rb: handle literal curly braces { and } to prevent f-string parsing errors
	pattern = (r'\$\(\((?P<arith>[^)]*)\)\)'
			   r'|`(?P<backtick>[^`]*)`'
			   r'|\$\((?P<dolparen>[^)]*)\)'
			   r'|\$\{(?P<bvar>\w+)\}|\$(?P<var>\w+)'
			   r'|\$(?P<argc>\#)|\$(?P<argv>[@*])'
			   r'|(?P<lb>\{)|(?P<rb>\})')
	expanded = re.sub(pattern, replacer, s)
	return expanded, had[0]


_TOK = r"'[^']*'|\"(?:[^\"\\]|\\.)*\"|`[^`]*`|\$\(\([^)]*\)\)|\$\([^)]*\)|\S+"


def arith_to_py(expr):
	"""
	Convert the inner part of $((...)) to a Python arithmetic expression.
	"""
	expr = expr.strip()
	# Strip $ and {} from variables
	expr = re.sub(r'\$\{?(\w+)\}?', lambda m: m.group(1), expr)
	# Wrap standalone variables in int() since shell variables are strings by default
	expr = re.sub(r'\b([a-zA-Z_]\w*)\b', lambda m: f'int({m.group(1)})', expr)
	# Convert single slash / (division) to double slash //
	expr = re.sub(r'(?<![/<>=!*])/(?![/=])', '//', expr)
	return expr


def cmd_subst_to_py(cmd):
	"""
	Convert a command substitution body to a Python subprocess expression.
	"""
	cmd = cmd.strip()
	tokens = re.findall(_TOK,cmd)
	if not tokens:
		return "subprocess.run([], capture_output=True, text=True).stdout.strip()"
	args = ', '.join(shell_str_sq(t) for t in tokens)
	return f'subprocess.run([{args}], capture_output=True, text=True).stdout.strip()'


def shell_str_sq(token):
	"""
	Like shell_str but always produces single-quoted Python strings (safe inside f\"...\").
	"""
	s = shell_str(token)
	if s.startswith('"') and s.endswith('"') and not s.startswith('f"'):
		return "'" + s[1:-1].replace("'", "\\'").replace('\\\\"', '"') + "'"
	return s


def dquote(s):
	"""Wrap s in double quotes, escaping only what's necessary."""
	return ('"' + s
			.replace('\\', '\\\\')
			.replace('"', '\\"')
			.replace('\n', '\\n')
			.replace('\r', '\\r')
			+ '"')


def shell_str(token):
	"""
	Convert a shell token to a python string
	"""
	if not token:
		return '""'
	# handle simple quoted strings
	if token.startswith("'") and token.endswith("'") and len(token) >= 2:
		return dquote(token[1:-1])
	# handle double-quoted strings with possible $ expansions
	if token.startswith('"') and token.endswith('"') and len(token) >= 2:
		inner = token[1:-1]
		content, had = expand_dollar(inner)
		return f'f"{content}"' if had else dquote(inner)
	m = re.fullmatch(r'\$\(\(([^)]*)\)\)', token)
	if m:
		return arith_to_py(m.group(1))
	m = re.fullmatch(r'`([^`]*)`', token)
	if m:
		return cmd_subst_to_py(m.group(1))
	m = re.fullmatch(r'\$\(([^)]*)\)', token)
	if m:
		return cmd_subst_to_py(m.group(1))
	m = re.fullmatch(r'\$\{?(\w+)\}?', token)
	if m:
		var = m.group(1)
		if var.isdigit():
			return f'sys.argv[{var}]'
		return var
	if '$' in token or '`' in token:
		content, had = expand_dollar(token)
		return f'f"{content}"' if had else dquote(token)
	return dquote(token)


def _token_content(token):
	"""
	Return (content_str, had_vars) for use inside a merged f-string.
	"""
	# check for simple quoted strings first, which should not be treated as f-strings
	if token.startswith("'") and token.endswith("'") and len(token) >= 2:
		inner = token[1:-1]
		return inner.replace('{', '{{').replace('}', '}}'), False
	# handle double-quoted strings with possible $ expansions
	if token.startswith('"') and token.endswith('"') and len(token) >= 2:
		return expand_dollar(token[1:-1])
	m = re.fullmatch(r'\$\(\(([^)]*)\)\)', token)
	if m:
		return '{' + arith_to_py(m.group(1)) + '}', True
	m = re.fullmatch(r'`([^`]*)`', token)
	if m:
		return '{' + cmd_subst_to_py(m.group(1)) + '}', True
	m = re.fullmatch(r'\$\(([^)]*)\)', token)
	if m:
		return '{' + cmd_subst_to_py(m.group(1)) + '}', True
	m = re.fullmatch(r'\$\{?(\w+)\}?', token)
	if m:
		var = m.group(1)
		if var.isdigit():
			return '{sys.argv[' + var + ']}', True
		return '{' + var + '}', True
	if '$' in token or '`' in token:
		return expand_dollar(token)
	return token.replace('{', '{{').replace('}', '}}'), False


def _is_glob(token):
	# bool: does this token look like an unquoted glob pattern
	return (any(c in token for c in '*?[')
			and not (token.startswith('"') or token.startswith("'")))


def echo_arg(rest):
	"""
	Merge the arguments of echo into a Python print() argument string.

	When any token is an unquoted glob, use comma-separated args so globs
	can be unpacked:  print('prefix', *sorted(glob.glob('?.py')))
	Otherwise build a single f-string:  print(f"hello {name}")
	"""
	# split rest into tokens, respecting quotes
	tokens = re.findall(_TOK,rest)
	if not tokens:
		return ''
	# if any token is an unquoted glob pattern, we need to handle them separately
	if any(_is_glob(t) for t in tokens):
		if len(tokens) == 1:
			return f'" ".join(sorted(glob.glob("{tokens[0]}")))'
		args = []
		for t in tokens:
			if _is_glob(t):
				args.append(f'*sorted(glob.glob("{t}"))')
			else:
				args.append(shell_str(t))
		return ', '.join(args)
	# if no globs, we can merge everything into a single f-string
	if len(tokens) == 1:
		return shell_str(tokens[0])
	# merge tokens into a single string, tracking if any variable expansions were done
	parts, any_var = [], False
	for t in tokens:
		content, had = _token_content(t)
		parts.append(content)
		any_var = any_var or had
	joined = ' '.join(parts)
	if any_var:
		return f'f"{joined}"'
	return dquote(joined.replace('{{', '{').replace('}}', '}'))


def strip_comment(s):
	"""
	Split a shell line into (code, comment).
	A '#' only starts a comment when it appears outside quotes and is
	preceded by whitespace
	Returns (code_part_stripped, '  # ...' or '').
	"""
	in_single = in_double = False
	# scan through the string to find the first unquoted '#' that starts a comment
	for i, c in enumerate(s):
		if c == "'" and not in_double:
			in_single = not in_single
		elif c == '"' and not in_single:
			in_double = not in_double
		elif c == '#' and not in_single and not in_double:
			if i == 0 or s[i - 1] in (' ', '\t'):
				return s[:i].rstrip(), '  ' + s[i:]
	return s, ''

# all test operators supported by the 'test' builtin
_UNARY_OPS = {
	'-z': '{} == ""',
	'-n': '{} != ""',
	'-f': 'os.path.isfile({})',
	'-d': 'os.path.isdir({})',
	'-e': 'os.path.exists({})',
	'-r': 'os.access({}, os.R_OK)',
	'-w': 'os.access({}, os.W_OK)',
	'-x': 'os.access({}, os.X_OK)',
	'-s': 'os.path.getsize({}) > 0',
	'-L': 'os.path.islink({})',
}

_BINARY_OPS = {
	'=': '==', '!=': '!=',
	'-eq': '==', '-ne': '!=',
	'-lt': '<',  '-le': '<=',
	'-gt': '>',  '-ge': '>=',
}


def test_val(token):
	"""
	Convert a shell test token to a Python expression for use in test translations
	"""
	# loop through patterns for variable tokens first, which should be treated as variables in test expressions
	for pat in (r'\$\{?(\w+)\}?', r'"\$\{?(\w+)\}?"'):
		m = re.fullmatch(pat, token)
		if m:
			var = m.group(1)
			if var.isdigit():
				return f'sys.argv[{var}]'
			return var
	if re.fullmatch(r'-?\d+', token):
		return token
	return shell_str(token)


def translate_test(args):
	"""
	Translate the arguments of a 'test' command or [ ... ] condition into a Python expression
	"""
	if not args:
		return 'True'
	# handle nested [ ... ] by stripping outer brackets
	if args[0] == '[' and args[-1] == ']':
		args = args[1:-1]
	if not args:
		return 'True'
	# handle !, -a, -o for logical operations
	if args[0] == '!':
		return f'not ({translate_test(args[1:])})'
	if '-o' in args:
		i = args.index('-o')
		return f'({translate_test(args[:i])}) or ({translate_test(args[i+1:])})'
	if '-a' in args:
		i = args.index('-a')
		return f'({translate_test(args[:i])}) and ({translate_test(args[i+1:])})'
	# handle unary and binary operators
	if len(args) == 2 and args[0] in _UNARY_OPS:
		return _UNARY_OPS[args[0]].format(test_val(args[1]))
	if len(args) == 3 and args[1] in _BINARY_OPS:
		left, op, right = test_val(args[0]), args[1], test_val(args[2])
		py_op = _BINARY_OPS[op]
		if op in ('-eq', '-ne', '-lt', '-le', '-gt', '-ge'):
			# Shell arithmetic comparison. If the value is not a pure numeric literal, 
			# it might be a variable, so we wrap it in int()
			def _int(v):
				return v if re.fullmatch(r'-?\d+', v) else f'int({v})'
			return f'{_int(left)} {py_op} {_int(right)}'
		if op in ('=', '!='):
			# shell string comparison — numeric literals must stay as Python strings
			def _str(v):
				return f'"{v}"' if re.fullmatch(r'-?\d+', v) else v
			return f'{_str(left)} {py_op} {_str(right)}'
		return f'{left} {py_op} {right}'
	return ' '.join(args)


def translate_condition(cond):
	"""
	Translate a shell condition into a Python expression
	"""
	cond = cond.strip()
	# handle simple true/false conditions and test/[ ... ]
	if cond in ('true', ':'):
		return 'True'
	if cond == 'false':
		return 'False'
	if cond.startswith('test ') or cond == 'test':
		inner = cond[4:].strip()
		args = re.findall(_TOK,inner)
		return translate_test(args)
	if cond.startswith('['):
		inner = re.sub(r'^\[\s*', '', re.sub(r'\s*\]\s*$', '', cond))
		args = re.findall(_TOK,inner)
		return translate_test(args)
	return cond


def make_for_iter(items_s):
	"""
	Convert the shell for-loop item list to a Python iterable expression.
	"""
	tokens = re.findall(_TOK,items_s)
	if not tokens:
		return '[]'
	# handle $@ and $* specially to expand to sys.argv[1:]
	if tokens in (['$@'], ['$*']):
		return 'sys.argv[1:]'
	# check if any token is an unquoted glob pattern 
	if len(tokens) == 1 and any(c in tokens[0] for c in '*?['):
		return f'sorted(glob.glob({dquote(tokens[0])}))'
	# if no globs, we can just return a list of the tokens
	if len(tokens) == 1:
		return shell_str(tokens[0])
	return '[' + ', '.join(shell_str(t) for t in tokens) + ']'


def translate_line(line, indent=0):
	"""
	Translate a single line of shell script to Python
	"""
	s = line.strip()
	pad = '    ' * indent

	if not s or s.startswith('#!'):
		return None

	if s.startswith('#'):
		return pad + s

	s, comment = strip_comment(s)
	if not s:
		return pad + comment.strip() if comment else None
	# x = ... 
	m = re.match(r'^(\w+)=(.*)', s)
	if m:
		var, val = m.group(1), m.group(2).strip()
		return pad + f'{var} = {shell_str(val) if val else "\"\""}{comment}'
	# handle echo ...
	if re.match(r'^echo\b', s):
		rest = s[4:].strip()
		end = ''
		if rest.startswith('-n'):
			rest = rest[2:].strip()
			end = ', end=""'
		arg = echo_arg(rest)
		if arg:
			return pad + f'print({arg}{end}){comment}'
		elif end:
			return pad + f'print(end=""){comment}'
		else:
			return pad + f'print(){comment}'
	# handle exit [code]
	if re.match(r'^exit\b', s):
		rest = s[4:].strip()
		code = rest.split()[0] if rest.strip() else '0'
		return pad + f'sys.exit({code}){comment}'
	# handle cd ...
	if re.match(r'^cd\b', s):
		rest = s[2:].strip()
		tokens = re.findall(_TOK, rest)
		path = shell_str(tokens[0]) if tokens else 'os.path.expanduser("~")'
		return pad + f'os.chdir({path}){comment}'
	# handle read var
	if re.match(r'^read\b', s):
		rest = s[4:].strip()
		var = rest.split()[0] if rest.strip() else '_'
		return pad + f'{var} = input(){comment}'
	# handle for var in items
	m = re.match(r'^for\s+(\w+)\s+in\s+(.*)', s)
	if m:
		var, items_s = m.group(1), m.group(2).strip()
		return pad + f'for {var} in {make_for_iter(items_s)}:{comment}'
	# handle if condition
	m = re.match(r'^if\s+(.*)', s)
	if m:
		return pad + f'if {translate_condition(m.group(1).strip())}:{comment}'
	# handle while condition
	m = re.match(r'^while\s+(.*)', s)
	if m:
		return pad + f'while {translate_condition(m.group(1).strip())}:{comment}'

	# external command via subprocess
	tokens = re.findall(_TOK,s)
	if tokens:
		args = []
		for t in tokens:
			if any(c in t for c in '*?[') and not (t.startswith('"') or t.startswith("'")):
				args.append(f'*sorted(glob.glob({dquote(t)}))')
			else:
				args.append(shell_str(t))
		return pad + f'subprocess.run([{", ".join(args)}]){comment}'

	return None


def main():
	# check for the correct number of arguments
	if len(sys.argv) != 2:
		print("Usage: sharpie.py <input.sh> > <output.py>")
		sys.exit(1)

	with open(sys.argv[1], 'r') as f:
		raw_lines = f.readlines()

	# loop through lines and join them if there is an unclosed quote
	# to handle multi-line strings properly
	lines = []
	buf, in_s, in_d = '', False, False
	for line in raw_lines:
		buf += line
		for c in line:
			# toggle single quote state if we are not inside double quotes
			if c == "'" and not in_d:
				in_s = not in_s
			# toggle double quote state if we are not inside single quotes
			elif c == '"' and not in_s:
				in_d = not in_d
		# if the line ends and we are not inside any quotes, save it as a complete command
		if not in_s and not in_d:
			lines.append(buf)
			buf = ''
	if buf:
		lines.append(buf)

	python_lines = []
	indent = 0
	pending = None  # pending Python header line (if/elif/while/for) waiting for then/do
	# process each line, handling constructs like 'if cond; then' and 'for i in 1 2 3; do'
	for raw_line in lines:
		if not raw_line.strip():
			if indent == 0:
				python_lines.append('')
			continue
		# split 'if cond; then' or 'for i in 1 2 3; do' into parts
		parts = raw_line.strip().split(';')
		for part in parts:
			s = part.strip()
			if not s:
				continue
			# strip inline comment to get the bare keyword
			keyword = strip_comment(s)[0].strip()
			if keyword in ('do', 'then'):
				if pending is not None:
					python_lines.append(pending)
					pending = None
				indent += 1
			elif keyword in ('done', 'fi'):
				indent = max(0, indent - 1)
			elif keyword == 'else':
				indent = max(0, indent - 1)
				python_lines.append('    ' * indent + 'else:')
				indent += 1
			elif re.match(r'^elif\b', keyword):
				indent = max(0, indent - 1)
				cond = keyword[4:].strip()
				pending = '    ' * indent + f'elif {translate_condition(cond)}:'
			else:
				translated = translate_line(part, indent)
				if translated is not None:
					python_lines.append(translated)

	body = '\n'.join(python_lines)
	# scan the translated python code to generate necessary import statements
	needed = sorted(m for m in ('sys', 'os', 'glob', 'subprocess', 'fnmatch', 'stat')
					if re.search(r'\b' + m + r'\.', body))
	# print the Python script header and imports
	print("#!/usr/bin/python3 -u")
	if needed:
		print('import ' + ', '.join(needed))
	for line in python_lines:
		print(line)

if __name__ == "__main__":
	main()