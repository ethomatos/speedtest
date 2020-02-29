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
	'api_key':'422d29499d5436d8f9db64f8b32870b8',
	'app_key':'dd88c2e85937d3cd0086c45ffda23b78d9b1920f'
}

initialize(**options)

statsd.namespace = 'et.pi.statsd'
statsd.constant_tags = ['owner', 'et']
#statsd.service_check('picheck', 'DogStatsd.WARNING', tags=["service:rasp"])

response = subprocess.Popen('/usr/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
response = response.decode()
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
statsd.gauge('ping', ping[0], tags=["host:raspberrypi"])
statsd.gauge('download', download[0], tags=["host:raspberrypi"])
statsd.gauge('upload', upload[0], tags=["host:raspberrypi"])


