# Starcraft-Replay-Scanner
A Daemon that scans for new starcraft 2 replays and uploads them to a csv file based on user specified input

# CSV output
The result is output to a csv file with the following format:
date,map,your name,opponents name,your race,opponents race,win,game length,details

Everything except details is autofilled (details is for you to list any notes you might have about the game)

# Installation
Run the install script (.bat file for windows)

# Usage
Run the starcraft_replay_scanner.bat file
On first usage it will ask you to give it:
- the absolute path to your starcraft replays folder (it will scan subdirectories so you can give the accounts folder C:\Users\{$username}\Documents\StarCraft II\Accounts in windows)
- the name of the output csv file (this is where the output is palced
- your starcraft usernames (comma separated list of users to track (ignores case) EX: liqht,protossop,dragongod)
- the races you want to track (comma separated list of races EX: z,t,p)

The script only records 1v1 ladder games in which the given username participated with the given race

If you want to update any of these settings feel free to edit the starcraft_replay_scanner.config file

# Scheduling
The bat file has a default to run the script every 10 minutes, you can change that by editing the bat file (the first argument 600 is the # of seconds to wait between runs)
# Trouble shooting
- The script requires python 3 to run, you can download python 3 here: https://www.python.org/downloads/
- The script also assumes that python is in your windows path environment variable (how to add it: https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path)
- If you have the csv open in excel when the script runs it won't be able to update the spreadsheet. It will reset the scan date and try again after the specified sleep period.