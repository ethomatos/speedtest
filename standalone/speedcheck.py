#!/usr/bin/python3
import os
import re
import subprocess
import time
import math
from datadog import initialize, api, statsd
from argparse import ArgumentParser
import json

debug = False

# Main routine of the program
def main(keys):
	initialize(**keys)

	statsd.namespace = 'system.net'
	statsd.constant_tags = ['owner', 'et']

	"""
		The CLI utility speedtest-cli produces this output:
		{
		"type":"result",
		"timestamp":"2020-12-30T01:42:29Z",
		"ping":{"jitter":0.99199999999999999,"latency":3.7320000000000002},
		"download":{"bandwidth":100605454,"bytes":587987912,"elapsed":5815},
		"upload":{"bandwidth":116780821,"bytes":1165946928,"elapsed":10300},
		"isp":"Verizon Fios",
		"interface":{"internalIp":"192.168.1.249","name":"eno1","macAddr":"64:00:6A:5B:21:2C","isVpn":false,"externalIp":"108.6.247.138"},
		"server":{"id":5029,"name":"AT&T","location":"New York, NY","country":"United States","host":"nyc.speedtest.sbcglobal.net","port":8080,"ip":"99.24.18.25"},
		"result":{"id":"d4dbebe4-275f-47f9-8637-589e87021daf","url":"https://www.speedtest.net/result/c/d4dbebe4-275f-47f9-8637-589e87021daf"}
		}
	"""

	# Run the Speedtest CLI and get JSON output format
	response = subprocess.Popen('/usr/bin/speedtest -f json-pretty -P 3', shell=True, stdout=subprocess.PIPE).stdout.read()
	data = json.loads(response.decode())
	latency = data['ping']['latency']
	statsd.gauge('ping', latency)
	download = round((data['download']['bytes'] * 8) / data['download']['elapsed'])
	upload = round((data['upload']['bytes'] * 8) / data['upload']['elapsed'])
	statsd.gauge('download', download)
	statsd.gauge('upload', upload)
	if (debug): print(str(latency) + ", " + str(download) + ", " + str(upload))

if __name__ == "__main__":
	parser = ArgumentParser(description='Use Ookla Speedtest CLI.')
	helpText = "Enter a file to read in the Datadog API keys.\n"
	parser.add_argument('-i', help=helpText, required=True)
	args = parser.parse_args()
	tokenfile = args.i if args.i else 'dd.keys'
	# acquire api keys
	dir = '/home/et/dev/speedtest/standalone'
	initfile = dir + "/" + tokenfile
	keys = json.load(open(initfile))
	main(keys)
