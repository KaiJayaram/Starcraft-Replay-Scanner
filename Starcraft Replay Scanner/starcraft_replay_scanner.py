#needed libraries
import sc2reader
import time
import os.path
import os

#ask for user config info
def request_user_input():
    print("input the absolute path of your replay folder")
    replay_path = input()
    print("input the name of your desired output file (csv format)")
    output_file = input()
    print("input your starcraft 2 username")
    username = input().lower()
    return replay_path, output_file, username

#setup output
def init_output(output_file, headers):
    output = open(output_file, "w")
    output.write(headers)
    output.close()
    
def write_output(matches_to_append, output_file):
    with open(output_file, "a") as output:
        for line in matches_to_append:
            output.write(line)
            output.write("\n")
        
# update config file with new info
def update_config(scan_date, replay_path, output_file, username, config_file):
    config = open(config_file, "w") 
    config.write(str(scan_date))
    config.write('\n')
    config.write(replay_path) 
    config.write('\n')
    config.write(output_file)
    config.write('\n')
    config.write(username)
    config.write('\n')
    config.close() 
    
def read_config(config_file):
    # read config
    with open(config_file) as f:
        for i,line in enumerate(f):
            if (i==0):
                last_scan_date = float(line.strip())
            if (i==1):
                replay_path = line.strip()
            if (i==2):
                output_file = line.strip()
            if (i==3):
                username = line.strip().lower()
    return last_scan_date, replay_path, output_file, username

# filter out unwanted replays (only ladder and 1v1)
def parse_replay(replay, username):
    # constants for replay filtering
    ladder = "Ladder"
    ones = "1v1"
    if replay.category != ladder or replay.type != ones:
        return None
    p1 = replay.teams[0].players[0]
    p2 = replay.teams[1].players[0]
    if (p1.name.lower() == username):
        opponent = p2
        you = p1
        res = vars(replay.teams[0])['result']
    elif(p2.name.lower() == username):
        you = p2
        opponent = p1
        res = vars(replay.teams[1])['result']
    else:
        # filter out replays without wanted user playing
        return None
    if res == None :
        res = "Unknown"
    return ",".join([replay.end_time.strftime("%m-%d-%Y %H:%M"), replay.map_name, you.name, opponent.name, you.pick_race[0], opponent.pick_race[0], res, str(replay.game_length)])
                 
# run replay scanner daemon
def run_daemon():
    # get time of scan
    scan_date = time.time()
    # config file name
    config_file = "starcraft_replay_scanner.config"
    # headers for output csv
    headers = "date,map,you,opponent,player1 race,player2 race,win,game length,details\n"
    #check for existence
    if (not os.path.exists(config_file)):
        # get initialization info from user
        last_scan_date = 0
        replay_path, output_file, username = request_user_input()
    
        init_output(output_file, headers)
        update_config(scan_date, replay_path, output_file, username, config_file)
    else:    
        last_scan_date, replay_path, output_file, username = read_config(config_file)
        update_config(scan_date, replay_path, output_file, username, config_file)             

    # now replay_path is path to replays, last_scan_date is time of last scan, scan_date is time of this scan
    # output_file is name of output file
    matches_to_append = []

    directory = os.fsencode(replay_path)
    
    # iterate over replays
    for file in sorted(os.listdir(directory), key=lambda x: os.path.getmtime(replay_path + "\\" + os.fsdecode(x))):
        filename = os.fsdecode(file)
        absolute_replay_path = replay_path + "\\" + filename
        # last modified date of file
        lm = os.path.getmtime(absolute_replay_path)

        # only add new replays
        if lm > last_scan_date:
            replay = sc2reader.load_replay(absolute_replay_path, load_level=2)
            parsed = parse_replay(replay,username)
            # skip failed parses
            if parsed == None:
                continue
            matches_to_append.append(parsed)
            
    write_output(matches_to_append, output_file)

def main():
	run_daemon()

if __name__ == '__main__':
    main()