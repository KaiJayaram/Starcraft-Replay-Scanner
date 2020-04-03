#needed libraries
import sc2reader
import time
import os.path
import os
import sys
import datetime
from mpyq import MPQArchive
import json
import traceback

# ask for user config info
def request_user_input():
    print("input the absolute path of your replay folder")
    replay_path = input()
    print("input the name of your desired output file (csv format)")
    output_file = input()
    print("input your starcraft 2 usernames (as csv so user1,user2,user3)")
    usernames = input().lower().replace(" ", "")
    print("input the desired races you wish to record as a csv list (so t,z,p for terran zerg and protoss)")
    races = input().upper().replace(" ", "")
    return replay_path, output_file, usernames, races

# setup output
def init_output(output_file, headers):
    try:
        output = open(output_file, "w")
        output.write(headers)
        output.close()
    except:
        print("unable to write headers to output file, most likely in use")
        
# write output to csv file
def write_output(matches_to_append, output_file, last_scan_date, config_dict, config_file):
    try:
        with open(output_file, "a") as output:
            for line in matches_to_append:
                try:
                    output.write(line)
                    output.write("\n")
                except:
                    print("failed to write line " + str(line))
                    continue
    except:
        print("unable to update output file most likely in use. Resetting last scan date")
        config_dict['scanDate'] = last_scan_date
        update_config(config_dict, config_file)
        
# update config file with new info
def update_config(config_dict, config_file):
    with open(config_file, "w") as config:
        for key,value in config_dict.items():
            # join array
            if type(value) == type([]):
                value = ",".join(value)

            config.write(key+"="+str(value)+"\n")

# read config from file
def read_config(config_file):
    config_dict = {}
    with open(config_file) as f:
        for _,line in enumerate(f):
            key, value = line.strip().split("=")
            if "," in value:
                value = value.lower().split(",")
            config_dict[key] = value
    return config_dict#last_scan_date, replay_path, output_file, username

# get all sc2 replay files that have been modified since last scan date (recurse through directories)
def get_new_replay_file_paths(replay_path, last_scan_date):
    out = []
    directory = os.fsencode(replay_path)

    # iterate over replays
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        curr_path = replay_path + "\\" + filename
        # always scan directories
        if os.path.isdir(curr_path):
        	out += get_new_replay_file_paths(curr_path, last_scan_date)
        else:
        	# only look at files that have been modified since last scan
	        lm = os.path.getmtime(curr_path)
	        if last_scan_date < lm:
	            if curr_path.endswith(".SC2Replay"):
	                out.append(curr_path)
    return sorted(out,  key=os.path.getmtime)

# extract useful information from replay file
def parse_replay(replay, usernames, config_dict, filepath):
    # constants for replay filtering
    ladder = "Ladder"
    ones = "1v1"
    # filter out unwanted replays (only ladder and 1v1)
    if replay.category != ladder or replay.type != ones:
        return None
    # player 1 and player 2
    p1 = replay.teams[0].players[0]
    p2 = replay.teams[1].players[0]

    # find out who is you and who is your opponent
    if p1.name.lower() in usernames:
        opponent = p2
        you = p1
        res = vars(replay.teams[0])['result']
        your_id = 0
        opponent_id = 1
    elif p2.name.lower() in usernames:
        you = p2
        opponent = p1
        res = vars(replay.teams[1])['result']
        your_id = 1
        opponent_id = 0
    else:
        # filter out replays without wanted user playing
        return None
    # check race 
    if you.pick_race[0] not in config_dict["recordedRaces"]:
        return None
    # sometimes no result is found
    if res == None :
        res = "Unknown"
    apmmmr_dict = extract_mmr_apm(filepath, your_id, opponent_id)
    # format output for csv file
    return ",".join([replay.end_time.strftime("%m-%d-%Y %H:%M"), replay.map_name, you.name, opponent.name, you.pick_race[0], opponent.pick_race[0], apmmmr_dict['yourMMR'], apmmmr_dict['opponentMMR'], apmmmr_dict['yourAPM'], apmmmr_dict['opponentAPM'],res, str(replay.game_length)])
                 
def extract_mmr_apm(path, your_id, opponent_id):
	try:
		archive = MPQArchive(path)

		players = json.loads(archive.extract()[b'replay.gamemetadata.json'])['Players']
		
		if "MMR" not in players[opponent_id]:
			players[opponent_id]["MMR"] = "Unknown"
		if "MMR" not in players[your_id]:
			players[your_id]["MMR"] = "Unkown"

		return {"yourMMR":str(players[your_id]['MMR']), "opponentMMR":str(players[opponent_id]['MMR']), "yourAPM":str(players[your_id]['APM']),"opponentAPM":str(players[opponent_id]['APM'])}
	except Exception:
		traceback.print_exc()
		print("failed to parse mmr/apm for path {}".format(path))
		return {"yourMMR":"Unknown", "opponentMMR":"Unknown", "yourAPM":"Unknown","opponentAPM":"Unknown"}

# run replay scanner daemon
def run_daemon():
    # get time of scan
    scan_date = time.time()
    # config file name
    config_file = "starcraft_replay_scanner.config"
    # headers for output csv
    headers = "date,map,you,opponent,your race,opponent race,your mmr,opponent mmr,your apm,opponent apm,win,game length,details\n"
    # setup for first time running
    if not os.path.exists(config_file):
        last_scan_date = 0
        # get initialization info from user
        replay_path, output_file, usernames, races = request_user_input()
        config_dict = {"scanDate":scan_date, "replayPath":replay_path, "outputFile":output_file, "username":usernames, "recordedRaces":races}
        # init config and output
        init_output(output_file, headers)
        update_config(config_dict, config_file)
    else:    
        config_dict = read_config(config_file)
        last_scan_date = float(config_dict["scanDate"])
        config_dict["scanDate"] = scan_date
        # update latest scan date
        update_config(config_dict, config_file)             

    # now replay_path is path to replays, last_scan_date is time of last scan, scan_date is time of this scan
    # output_file is name of output file
    matches_to_append = []

    directory = os.fsencode(config_dict['replayPath'])
    
    # iterate over replays
    for path in get_new_replay_file_paths(config_dict["replayPath"], last_scan_date):
        # only add new replays
        print("found replay: {}".format(path))
        try:
            replay = sc2reader.load_replay(path, load_level=2)
        except:
            print("failed for file {}".format(path))
            # ignore failures for now
            continue
        parsed = parse_replay(replay,config_dict['username'], config_dict, path)
        # skip failed parses
        if parsed == None:
        	print("failed to parse replay {}".format(path))
        	continue

        matches_to_append.append(parsed)
    write_output(matches_to_append, config_dict['outputFile'], last_scan_date, config_dict, config_file)

def main():
    run_in_background = False
    if len(sys.argv) > 1:
        run_in_background = True
        sleep_duration = int(sys.argv[1]) # in seconds

    while True:
        print("Running Daemon")
        start_time = datetime.datetime.now()
        run_daemon()
        end_time = datetime.datetime.now()
        elapsed = end_time-start_time
        print("Finished ({} seconds)".format(elapsed.total_seconds()))

        if not run_in_background:
            break
        time.sleep(sleep_duration)

if __name__ == '__main__':
    main()
