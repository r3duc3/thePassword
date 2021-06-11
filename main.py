#!/usr/bin/python3

banner = '''########### 7.3-A ###########
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
	from getpass import getuser
	from json import loads as jload, dumps as jdump
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
		self.prompt = '{w[1]}{who}@thePassword {w[4]}$ {w[0]}'.format(w=self.clr, who=getuser())

		# path
		self.path = f'.saved.json'

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
			},
			{
			'cmd': 'get',
			'desc': '''ambil password yang sudah disimpan
			\rcommand: get (site)
			\rdefault: list site untuk dipilih'''
			},
			{
			'cmd': 'clean',
			'desc': 'bersihin layar'
			}
		)

		self.clean()

	def clean(self):
		system('clear' if name == 'posix' else 'cls')
		for _ in banner:
			print(_, end='', flush=1)
			sl(0.005)

	def important(self, name):
		# to infinity and beyond
		var = ''
		while not bool(var):
			self.debug('c', f'*{name}: ')
			var = input()

		return var

	def auto(self, opt=[]):
		readline.set_completer(SimpleCompleter(opt).complete)
		readline.parse_and_bind(f'tab: {"complete" if opt else "nothing"}')

	def gen(self, *args):
		# disable autocomplete
		self.auto()

		self.debug('g', 'membuat password...\n')

		# site & uname is important
		site = self.important('Site')
		uname = self.important('Username')

		# var tambahan
		self.debug('c', 'tambahan: ')
		other = input()

		args = args[0]
		len_args = len(args)

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

		# get history
		if exs(self.path):
			hty = jload(open(self.path, 'r').read())
		else:
			hty = []

		# generating & checking
		while 1:
			rhty = [x['password'] for x in hty] if hty else []
			out = ''.join(choices(pre, k = lgth))
			if out not in rhty:
				self.debug('g', f'{args[0]}: {out}\n')
				self.debug('c', 'Konfirmasi[Y/n] ')
				yes = input().lower()
				if yes not in ['y', 'n']:
					yes = 'y'
				
				if yes == 'n':
					continue

				break

		# save password to history
		hty.append({
			'site': site,
			'username': uname,
			'password': out,
			'other': other
		})
		open(self.path, 'w').write(jdump(hty))

		# copy password to clipboard
		self.debug('g', f'menyalin {args[0]}...')
		try:
			copy(out)
		except PyperclipException:
			self.debug('r', '\ngagal menyalin\n')
		else:
			self.debug('g', f'{args[0]} tersalin\n')

	def getter(self):
		# get history
		if exs(self.path):
			hty = jload(open(self.path, 'r').read())
		else:
			hty = []

		if not hty:
			self.debug('r', 'tidak ada password yang tersimpan\n')
			return

		self.auto([x['site'] for x in hty])
		site = input('Site: ')
		if not bool(site):
			return

		self.clean()
		for x in hty:
			if x['site'] == site:
				print('\x1b[1;0m='*round(gts().columns))
				for y, z in x.items():
					print('{w[2]}{name}     : {w[6]}{val}'.format(w=self.clr, name=y.title(), val=z))

		print('\x1b[1;0m='*round(gts().columns))

	def cli(self, term=''):
		if term == '':
			self.auto([x['cmd'] for x in self.cmds])
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
		elif self.cmd[0] == 'clean':
			self.clean()
		elif self.cmd[0] == 'get':
			self.getter()
		else:
			self.debug('r', f'{self.cmd[0]}: command gak ketemu\n')

	def debug(self, clr, txt):
		d = self.clr[0]
		if clr == 'r':
			a, b, c = self.clr[1], self.clr[3], '!'
		elif clr == 'g':
			a, b, c = self.clr[2], self.clr[6], '*'
		elif clr == 'c':
			a, b, c = self.clr[4], self.clr[5], '?'

		print(f'\r{" "*gts().columns}', end='')
		print(f'\r{d}[{a}{c}{d}] {b}{txt}{d}', end='', flush=1)

	def hlp(self):
		for cmd in self.cmds:
			print('='*round(gts().columns/3+2))
			print(f'command: {cmd["cmd"]}')
			print('description'.center(round(gts().columns/4), '+'))
			print(cmd['desc'])

		print('\n*Note: klik tab untuk autocomplete')

pwd = Password()

# inline
if len(argv) > 1 and len(argv) <= 4:
	pwd.cli(' '.join(argv[1:]))
	exit()

# prompt
while 1:
	try:
		pwd.cli()
	except KeyboardInterrupt:
		exit('')