#!/usr/bin/python3

# -------------------------
#
# author: _Reduce
# made with hand by _Reduce
# dibuat dikala gabut
# 
# -------------------------

# modules
import string, pyperclip, readline
from random import choices
from sys import argv
from os import get_terminal_size as gts
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
		self.quit = False
		self.clr = tuple([chr(27)+'[1;0m'] + list(chr(27)+'[1;3'+str(x)+'m' for x in range(1,7)))
		self.prompt = '{w[1]}_Reduce{w[6]}@{w[1]}thePassword {w[4]}# {w[0]}'.format(w=self.clr)
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

	def cli(self):
		self.cmd = input(self.prompt)
		if self.cmd not in [x['cmd'] for x in self.cmds]:
			self.cli()

	def hlp(self):
		for cmd in self.cmds:
			print('='*round(gts().columns/3+2))
			print(f'command: {cmd["cmd"]}')
			print('description'.center(round(gts().columns/4), '+'))
			print(cmd['desc'])

pwd = Password()
readline.set_completer(SimpleCompleter([x['cmd'] for x in pwd.cmds]).complete)
readline.parse_and_bind('tab: complete')

while not pwd.quit:
	try:
		pwd.cli()
	except:
		break
