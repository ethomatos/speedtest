import subprocess
import json
import sys
from datadog import initialize, statsd
import time

def initialize_datadog():
	"""
	Set up the Datadog connection using StatsD protocol.
	Using host.docker.internal allows reaching the host machine from inside Docker.
	"""
	options = {
		'statsd_host': 'datadog-agent',	# Special Docker DNS name for host machine
		'statsd_port': 8125	# Standard StatsD port
	}
	initialize(**options)
	print("Initialized Datadog connection")

def run_speed_test_and_report():
	"""
	Performs a speed test and reports results to both console and Datadog.
	The function uses speedtest-cli for measurements and StatsD for metric reporting.
	"""
	try:
		print("Starting speed test...")
			
		# Run speedtest-cli with JSON output for structured data
		print("Initiating speed test measurement...")
		result = subprocess.run(['speedtest-cli', '--json'], capture_output=True, text=True)
		
		# Parse the JSON output into a Python dictionary
		speed_data = json.loads(result.stdout)
		
		# Convert speeds to Mbps for readability
		download_mbps = speed_data['download'] / 1_000_000
		upload_mbps = speed_data['upload'] / 1_000_000
		ping = speed_data['ping']
		
		# Print human-readable results
		print("\nSpeed Test Results:")
		print(f"Download Speed: {download_mbps:.2f} Mbps")
		print(f"Upload Speed: {upload_mbps:.2f} Mbps")
		print(f"Ping: {ping:.2f} ms")
		print(f"Server: {speed_data['server']['sponsor']} ({speed_data['server']['name']})")
		
		# Send metrics to Datadog via StatsD
		print("\nSending metrics to Datadog...")
		statsd.gauge('system.net.download', download_mbps)
		statsd.gauge('system.net.upload', upload_mbps)
		statsd.gauge('system.net.ping', ping)
		
		# Add server information as tags for better metric organization
		tags = [
			f"server:{speed_data['server']['sponsor']}",
			f"server_name:{speed_data['server']['name']}",
			f"server_country:{speed_data['server']['country']}"
		]
		
		# Send an additional metric with all the tags
		statsd.gauge('system.net.test.completed', 1, tags=tags)
		print("Successfully sent metrics to Datadog")
			
	except subprocess.CalledProcessError as e:
		print(f"Error running speedtest-cli: {e}")
		print(f"Error output: {e.stderr}")
		# Send error metric to Datadog
		statsd.increment('system.net.test.errors', tags=['error_type:speedtest_cli'])
	except json.JSONDecodeError as e:
		print(f"Error parsing speedtest results: {e}")
		statsd.increment('system.net.test.errors', tags=['error_type:json_parse'])
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		statsd.increment('system.net.test.errors', tags=['error_type:unknown'])

if __name__ == "__main__":
	print(f"Python version: {sys.version}")
	initialize_datadog()
	run_speed_test_and_report()
