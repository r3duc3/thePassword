#!/usr/bin/python3

banner = '''############ beta ###########
#                           #
# author: _Reduce           #
# made with hand by _Reduce #
# dibuat dikala gabut       #
#                           #
#############################
'''

# modules
try:
	import readline
	from random import choices
	from sys import argv
	from time import sleep as sl
	from os import get_terminal_size as gts, name, system, mkdir
	from os.path import exists as exs
	from string import ascii_lowercase as asl, ascii_uppercase as asu, digits as dgt, punctuation as pnc
	from pyperclip import copy, PyperclipException

	if 'com.termux' in readline.__file__:
		from sh import termux_clipboard_set as copy
except Exception as ex:
	print(ex)
	exit(f'install: python3 -m pip install {ex.name}')

# modules;

# -------------------------
# 
# AutoComplete on tab with readline
# source: https://pymotw.com/2/readline/
# 
# -------------------------

class SimpleCompleter(object):
	def __init__(self, options):
		self.options = sorted(options)
		return

	def complete(self, text, state):
		response = None
		if state == 0:
			if text:
				self.matches = [s for s in self.options if s and s.startswith(text)]
			else:
				self.matches = self.options[:]

		try:
			response = self.matches[state]
		except IndexError:
			response = None

		return response

class Password:
	def __init__(self):
		# color
		self.clr = tuple([chr(27)+'[1;0m'] + list(chr(27)+'[1;3'+str(x)+'m' for x in range(1,7)))

		# prompt
		self.prompt = '{w[1]}_Reduce {w[4]}$ {w[0]}'.format(w=self.clr)

		# list command & helper
		self.cmds = (
			{
			'cmd': 'help',
			'desc': 'butuh bantuan?'
			},
			{
			'cmd': 'quit',
			'desc': 'keluar dari program'
			},
			{
			'cmd': 'sandi',
			'desc': '''buat sandi dengan huruf, angka dan tanda baca
			\rcommand: sandi (panjang) (format)
			\rex: sandi 999
			\rdefault:
			\r\tpanjang = 12
			\r\tformat = aA1!
			\r
			\rformat:
			\r\t- a = huruf kecil
			\r\t- A = huruf besar
			\r\t- 1 = angka
			\r\t- ! = tanda baca'''
			},
			{
			'cmd': 'pin',
			'desc': '''buat pin pastinya
			\rcommand: pin (panjang)
			\rex: pin 100
			\rdefault panjang 6'''
			}
		)

	def gen(self, *args):
		self.debug('g', 'membuat password...')
		args = args[0]
		len_args = len(args)
		path = f'.history/.{args[0]}'

		# set len pwd
		lgth = int(args[1]) if len_args >= 2 else 12 if args[0] == 'sandi' else 6

		# set prefix
		pre = ''
		if args[0] == 'sandi':
			if len_args == 3:
				if 'a' in args[2]:
					pre += asl
				if 'A' in args[2]:
					pre += asu
				if '1' in args[2]:
					pre += dgt
				if '!' in args[2]:
					pre += pnc

			else:
				pre = asl+asu+dgt+pnc

		elif args[0] == 'pin':
			pre = dgt

		# check existence before generate
		if not exs('.history'):
			mkdir('.history')

		if not exs(path):
			open(path, 'w')

		# generating & checking 
		while 1:
			rhty = open(path, 'r').read()
			out = ''.join(choices(pre, k = lgth))
			if out not in rhty:
				break

		# save password to history
		shty = open(path, 'w')
		shty.write(out+'\n')
		shty.close()

		# copy password to clipboard
		self.debug('g', f'{args[0]}: {out}')
		self.debug('g', 'menyalin...')
		try:
			copy(out)
		except PyperclipException:
			self.debug('r', 'gagal menyalin')
		else:
			self.debug('g', 'tersalin')

	def cli(self, term=''):
		if term == '':
			self.cmd = input(self.prompt)
		else:
			self.cmd = term

		self.cmd = self.cmd.split()
		if len(self.cmd) == 0:
			return False

		if self.cmd[0] == 'help':
			self.hlp()
		elif self.cmd[0] == 'quit':
			exit()
		elif self.cmd[0] in ('sandi', 'pin'):
			self.gen(self.cmd)
		else:
			self.debug('r', f'{self.cmd[0]}: command gak ketemu')

	def debug(self, clr, txt):
		d = self.clr[0]
		if clr == 'r':
			a, b, c = self.clr[1], self.clr[3], '!'
		elif clr == 'g':
			a, b, c = self.clr[2], self.clr[6], '*'

		print(f'{d}[{a}{c}{d}] {b}{txt}{d}')

	def hlp(self):
		for cmd in self.cmds:
			print('='*round(gts().columns/3+2))
			print(f'command: {cmd["cmd"]}')
			print('description'.center(round(gts().columns/4), '+'))
			print(cmd['desc'])

		print('\n*Note: klik tab untuk autocomplete')

pwd = Password()
readline.set_completer(SimpleCompleter([x['cmd'] for x in pwd.cmds]).complete)
readline.parse_and_bind('tab: complete')

# inline
if len(argv) > 1 and len(argv) <= 4:
	pwd.cli(' '.join(argv[1:]))
	exit()

# prompt
system('clear' if name == 'posix' else 'cls')
for _ in banner:
	print(_, end='', flush=1)
	sl(0.005)

while 1:
	try:
		pwd.cli()
	except KeyboardInterrupt:
		exit('')
