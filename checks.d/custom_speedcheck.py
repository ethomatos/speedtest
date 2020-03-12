# the following try/except block will make the custom check compatible with any Agent version
try:
	# first, try to import the base class from old versions of the Agent...
	from checks import AgentCheck

except ImportError:
	# ...if the above failed, the check is running in Agent version 6 or later
	from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.2.0"

import os
import re
import subprocess
import time

"""
The CLI utility speedtest-cli produces this output:
Ping: 10.464 ms
Download: 93.23 Mbit/s
Upload: 92.10 Mbit/s
"""

class SpeedCheck(AgentCheck):
	def check(self, instance):
		#statsd.namespace = 'et.pi.statsd'
		#statsd.constant_tags = ['owner', 'et']
		
		response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
		response = response.decode()
		ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
		download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
		upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

		self.gauge('system.net.ping', ping[0], tags=["owner:et"])
		self.gauge('system.net.download', download[0], tags=["owner:et"])
		self.gauge('system.net.upload', upload[0], tags=["owner:et"])


