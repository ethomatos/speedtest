#!/usr/bin/python3
import subprocess
import math
from datadog import initialize, statsd
import json

debug = True

# Main routine of the program
def main(options):
	initialize(**options)

	statsd.namespace = 'system.net'
	statsd.constant_tags = ['owner', 'et']

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
	# setup host and port
	options = {
		'statsd_host':'127.0.0.1',
		'statsd_port':8125
	}
	main(options)
