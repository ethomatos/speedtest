### MacOS
On MacOS install using brew the utility `speedtest-cli`. The command will be:
`brew install speedtest-cli`

After installing test it by running from a terminal the command:
`speedtest-cli --simple`

The output should look similar to this:
```
Ping: 8.5 ms
Download: 357.77 Mbit/s
Upload: 285.33 Mbit/s
```

### Linux
On Linux install the utility `speedtest-cli`. The command will vary on your version of Linux.
On Ubuntu the command will be:
`sudo apt-get install speedtest-cli`

On RedHat or CentOS use:
`sudo  yum install speedtest-cli`


### Installing the custom agent check
Step 1. Clone the repository

Step 2. Copy the files from the repository's ./speedcheck directory
  - Take the file in checks.d and copy it into your agent's checks.d directory
  - Take the file in conf.d and copy it into your agent's conf.d directory

Step 3. Update the Python script in `checks.d` to reference your own  tag of `owner:me` instead of `owner:et`


### Restart the agent and check results
- The agent needs to restart afterwards check for these metrics in whatever account your agent reports into.
  - system.net.ping
  - system.net.download
  - system.net.upload
