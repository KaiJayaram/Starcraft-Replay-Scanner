# Starcraft-Replay-Scanner
A Daemon that periodically scans for new starcraft 2 replays and uploads them to a csv file based on user specified input

Replay scanning for this project makes use of the following libraries:
- https://github.com/eagleflo/mpyq
- https://github.com/GraylinKim/sc2reader

# CSV output
The result is output to a csv file with the following headers:
date,map,you,opponent,your race,opponent race,your mmr,opponent mmr,your apm,opponent apm,win,game length,details

Everything except details is autofilled (details is for you to list any notes you might have about the game)

# Installation
You can either clone (Don't download with zip otherwise the update script will fail to pull updates from github when the program launches) this repository and use the install script to install the necessary python libraries or download the installer here: https://github.com/KaiJayaram/Starcraft-Replay-Scanner-Installer


# Usage
Run the starcraft_replay_scanner.bat file
On first usage it will ask you to give it:
- the absolute path to your starcraft replays folder (it will scan subdirectories so you can give the accounts folder C:\Users\{$username}\Documents\StarCraft II\Accounts in windows)
- the name of the output csv file (this is where the output is palced
- your starcraft usernames (comma separated list of users to track (ignores case) EX: liqht,flume,dragongod)
- the races you want to track (comma separated list of races EX: z,t,p)

The script only records 1v1 ladder games in which the given username participated with the given race

If you want to update any of these settings feel free to edit the starcraft_replay_scanner.config file

# Scheduling
The bat file has a default to run the script every 30, you can change that by editing the replay scanner bat file (the first argument 30 is the # of seconds to wait between runs)

# Troubleshooting
- The script requires python 3 to run, you can download python 3 here: https://www.python.org/downloads/
- The script also assumes that python is in your windows path environment variable (how to add it: https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path)
- If you have the csv open in excel when the script runs it won't be able to update the spreadsheet. It will reset the scan date and try again after the specified sleep period.
- If you are facing other issues check your config file to make sure there are no issues
- Submit an issue if you have other problems or email me at kailash (dot) jayaram (at) outlook (dot) com


