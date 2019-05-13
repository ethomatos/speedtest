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
	'api_key':'fc2e8f7e96275667061a287a1f934d7e',
	'app_key':'d0217cb86082c8816232eb3647816fca6cfb39bc'
}

initialize(**options)

statsd.namespace = 'et.raspi1.statsd'
statsd.constant_tags = ['owner', 'et']
statsd.service_check('raspstatcheck', 'DogStatsd.WARNING', tags=["service:rasp1"])

response = subprocess.Popen('/usr/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
response = response.decode()
with open('/var/log/router.log', 'w') as logfile:
	logfile.write(response)
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
statsd.gauge('ping', ping[0], tags=["ping:rasp1"])
statsd.gauge('download', download[0], tags=["download:rasp1"])
statsd.gauge('upload', upload[0], tags=["upload:rasp1"])
