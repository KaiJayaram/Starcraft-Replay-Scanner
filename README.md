# Starcraft-Replay-Scanner
A Daemon that scans for new starcraft 2 replays and uploads them to a csv file based on user specified input

# Installation
Run the install script (.bat file for windows)

# Usage
Run the starcraft_replay_scanner.bat file
On first usage it will ask you to give it:
- the absolute path to your starcraft replays folder
- the name of the output csv file
- your starcraft username
The script only records 1v1 ladder games in which the given username participated
If you want to update any of these settings feel free to edit the starcraft_replay_scanner.config file

# Config File
the first entry is the last scan date - this is used to determine which new replays to add
the second entry is the path to the replays folder
the third entry is the output file path
the fourth entry is the player username

# Trouble shooting
The script requires python 3 to run, you can download python 3 here: https://www.python.org/downloads/
The script also assumes that python is in your windows path environment variable (how to add it: https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path)
