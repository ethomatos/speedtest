#!/usr/bin/python3
import os
import re
import subprocess
import time
from datadog import initialize, api, statsd

"""
The CLI utility speedtest-cli produces this output:
Ping: 10.464 ms
Download: 93.23 Mbit/s
Upload: 92.10 Mbit/s
"""

options = {
	'api_key':'get_your_own',
	'app_key':'get_your_own'
}

initialize(**options)

statsd.namespace = 'et.statsd'
statsd.constant_tags = ['owner', 'et']

response = subprocess.Popen('/usr/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
response = response.decode()
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
statsd.gauge('ping', ping[0])
statsd.gauge('download', download[0])
statsd.gauge('upload', upload[0])


