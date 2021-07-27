import time
import argparse
import logging
from random import choice, randint

import requests


logging.basicConfig(format='%(levelname)s/%(asctime)s/%(message)s',
					level=logging.DEBUG)

parser = argparse.ArgumentParser()

parser.add_argument('-rps', type=float, default=1,
					help='Requests per second to load the app with')
					
parser.add_argument('--redos', action='store_true',
					help='Send a killer regular expression after 90 seconds')

regexes = ('^[a-zA-Z]+2$', '^asdf$', '^H*d$', '^[0-9]$',)
killer_not_sent = True
X = 90
RegExp = '(a+)*$'
string = 'a' * 22 + '!'


def send_regexp(regexp: str) -> None:
	resp = requests.post(
		url='http://localhost:4567/filters',
		json={'pattern': regexp}
	)
	if resp.status_code != 200:
		logging.warning('Failed to send regex %s', regex)


def send_rps(rps: int, redos: bool) -> None:
	global killer_not_sent, X, RegExp, string
	time_to_sleep = 1 / rps
	start_time = time.monotonic()
	for regex in regexes:
		send_regexp(regex)
	while True:
		if redos and killer_not_sent and time.monotonic() - start_time >= X:
			logging.info('Killer regex is sent')
			killer_not_sent = False
			send_regexp(RegExp)
		body = string
		resp = requests.post(
			url='http://localhost:4567/send',
			json={'body': body}
		)
		if resp.status_code != 202:
			logging.warning('String "%s" is rejected: %s', body, resp.json())
		time.sleep(time_to_sleep)


if __name__ == '__main__':
	args = parser.parse_args()
	send_rps(args.rps, args.redos)
	# resp = requests.post(url='http://localhost:4567/filters', json={'pattern': '(a+)*$'})
	# print(resp.status_code, resp.json())
	# i = 1
	# for na in (15, 20, 22, 24, 26):
	# 	for i in range(20):
	# 		resp = requests.post(url='http://localhost:4567/send', json={'body': 'a' * na + '!'})
	# 		print(na, i, resp.status_code)
	# 		time.sleep(0.1)
	# 	print('sleep(5)...')
	# 	time.sleep(5)
