import requests as req
import random
import sys
import csv
import constants as const
from helpers import read_usernames, calculate_slayer_ability, calculate_tile_score, calculate_final_score


def create_players(player_names):
    failed_players = []
    players = []
    players.append(["Username", "EHB", "EHB avg", "EHP",
                    "EHP avg", "Slayer Ability", "Tile Score", "Manual Score", "Weighted Score", "Final Score"])
    for player in player_names:
        # try get data from Temple
        try:
            # make API calls
            print('Attemping to get {}\'s data...'.format(player))

            p_req = player.replace(" ", "+")

            cur_stats = req.get(
                "https://templeosrs.com/api/player_stats.php?player={}&bosses=1".format(p_req)).json()

            rec_stats = req.get(
                "https://templeosrs.com/api/player_gains.php?player={}&time={}&bosses=1".format(p_req, const.SECS_IN_DAY * const.RECENT_DAYS_COUNT)).json()

            slayer_ability = calculate_slayer_ability(
                cur_stats["data"]["Slayer"], const.SLAYER_GOAL_XP)

            ehp = cur_stats["data"]["Ehp"]

            ehb = cur_stats["data"]["Ehb"]

            ehp_avg = rec_stats["data"]["Ehp"] / \
                (const.RECENT_DAYS_COUNT / const.AVERAGE_DAYS_COEFF)

            ehb_avg = rec_stats["data"]["Ehb"] / \
                (const.RECENT_DAYS_COUNT / const.AVERAGE_DAYS_COEFF)

            tiles_score = calculate_tile_score(cur_stats)

            iron_bool = True if cur_stats["data"]["info"]["Game mode"] != 0 else False

            weighted_score = calculate_final_score(
                ehb, ehb_avg, ehp, ehp_avg, slayer_ability, tiles_score, 0, iron_bool)

            players.append([
                player,
                ehb,
                ehb_avg,
                ehp,
                ehp_avg,
                slayer_ability,
                tiles_score,
                0,
                weighted_score,
                0
            ])
        except Exception as e:
            print(e)
            failed_players.append(player)
            # still add a blank player class
            players.append([player, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return (players, failed_players)


def read_in_players(player_names_file):
    # read player names in
    player_names = read_usernames(player_names_file)

    # attempt to get data for players
    players_data, failed_players = create_players(player_names)

    print('Unable to get data for these players: {}'.format(failed_players))

    # print these players to an output csv
    with open("player_stats_rough.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(players_data)


def update_players_score(player_scored_file):

    with open(player_scored_file, newline='') as csvfile:
        old_data = list(csv.reader(csvfile))

    # delete headers
    del old_data[0]

    new_data = []
    new_data.append(["Username", "EHB", "EHB avg", "EHP",
                     "EHP avg", "Slayer Ability", "Tile Score", "Manual Score", "Weighted Score", "Final Score"])

    for player in old_data:
        # username,EHB,EHB avg,EHP,EHP avg,Slayer Ability,Tile Score,Manual Score,Final Score
        new_data.append(
            [player[0],
             float(player[1]), # ehb
             float(player[2]), # ehb avg
             float(player[3]), # ehp
             float(player[4]), # ehp avg
             float(player[5]), # slayer
             float(player[6]), # tile score
             float(player[7]), # manual
             float(player[8]), # weight
             float(
                player[7]) + float(player[8]) # final
             ])

    with open("player_stats_with_manual.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(new_data)

def read_pairs(txt_file_path):
    usernames = []
    with open(txt_file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            names = line.split(',')  # Split the line by comma
            cleaned_names = [name.strip() for name in names if name.strip()]  # Remove leading/trailing whitespaces and skip empty names
            if cleaned_names:
                usernames.append(cleaned_names)
    return usernames

def make_teams(player_scored_file, team_count, pairs=False):
    with open(player_scored_file, newline='') as csvfile:
        players_data = list(csv.reader(csvfile))

    # delete headers
    del players_data[0]
    # print("Number of players imported: {}".format(len(players_data)))

    dir = True
    count = 0
    teams = [[] for _ in range(team_count)]
    
    if pairs:
        # know we need to read in a player team csv to ensure there are together
        # first go through players and pair them up and sum their weight
        pairs = read_pairs(pairs)
        indexed_pairs = []
        people = players_data
        for pair in pairs:
            indexed_pair = []  # Start with the pair itself
            sum_9th_column = 0  # Initialize sum to 0
            for name in pair:
                found = False
                for person in people:
                    if name == person[0]:
                        sum_9th_column += float(person[9])  # Add the 3rd column value to the sum
                        found = True
                        break
                if not found:
                    indexed_pair.append(None)
                    print(name)
            indexed_pairs.append((pair, sum_9th_column)) 
            
        # print(indexed_pairs)
        players_rand = sorted(indexed_pairs, key=lambda x: (float(x[1]), random.randint(0,9)), reverse=True)
        # print(players_rand)
        # exit()
    else:
        players_rand = sorted(players_data, key=lambda x: (float(x[9]), random.randint(0,9)), reverse=True)

    for player in players_rand:

        # Ugly logic to not pair certain people together        
        # if "name1" in [player[0] for player in teams[count]] and player[0] == "name2":
        #     print('oop - run again')
        #     exit()
        
        teams[count].append(player)
        if (count == team_count - 1 and dir == True) or (count == 0 and dir == False):
            dir = not dir
            continue
        if dir:
            count += 1
        else:
            count -= 1

    team_members = [[] for _ in range(team_count)]
        
    for i in range(len(teams)):
        score = 0
        for player in teams[i]:
            team_members[i].append(player[0])
            # score += float(player[9])
            if pairs:
                score += float(player[1])
            else:
                score += float(player[9])
            
        # This is unshuffled teams printing with amount and scores
        print(team_members[i], len(team_members[i]), score)
    
    
    # Shuffle teams for printing
    [random.shuffle(team_members[i]) for i in range(len(teams))]
    
    # Printing player by player
    # input()
    # for i in range(len(teams)):
    #     print("------ Team {} ------".format(i+1))
    #     input()
    #     for player in team_members[i]:
    #         if pairs:
    #             player = player[0] + "  | " + player[1]
    #         print("      ", player)
    #         input()
    
    # Print whole teams
    # for i in range(len(teams)):
    #     print("------ Team {} ------".format(i+1))
    #     print(*team_members[i], sep=', ')
    #     print()

def main():

    # python3 pybingo.py read-in-players names.txt
    if (sys.argv[1] == 'read-in-players'):
        read_in_players(sys.argv[2])

    # python3 pybingo.py update-players-score player_stats_rough.csv
    if (sys.argv[1] == 'update-players-score'):
        update_players_score(sys.argv[2])

    # python3 pybingo.py make-teams player_stats_with_manual.csv 13
    if (sys.argv[1] == 'make-teams'):
        make_teams(sys.argv[2], int(sys.argv[3]))
    
    # python3 pybingo.py make-teams-pairs player_stats_with_manual.csv 14 names_pairs.txt
    if (sys.argv[1] == 'make-teams-pairs'):
        make_teams(sys.argv[2], int(sys.argv[3]), sys.argv[4])

if __name__ == "__main__":
    main()
