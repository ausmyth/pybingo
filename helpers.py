import constants as const


def read_usernames(txt_file_path):
    # read in txt, return a list of strings of player names
    player_names = [line.rstrip() for line in open(txt_file_path)]
    return player_names


def make_players(player_scored_file):
    # try open csv file of player scores and return a list of player objects
    try:
        player_data = pd.read_csv(player_scored_file)
    except:
        print('Failed to create players from player scores file given.')
        exit()


def calculate_slayer_ability(xp, goal_xp):
    if xp < goal_xp:
        return xp / goal_xp * 100
    else:
        return 100


def calculate_tile_score(player_data):
    count = 0
    for tile in const.TILE_NAMES_LIST:
        try:
            if player_data["data"][tile] > 0:
                count += 1
        except:
            print("Couldn't find kc for {}".format(tile))
    return count / len(const.TILE_NAMES_LIST)


def calculate_final_score(ehb, ehb_avg, ehp, ehp_avg, slayer_ability, tiles_score, manual_score, iron_bool):
    score = ehp / 100.0 * const.EHP_T_W + \
        ehb / 100.0 * const.EHB_T_W \
        + tiles_score / 10.0 * const.TILE_W \
        + slayer_ability / 10.0 * const.SLAYER_W \
        + ehp_avg * const.EHP_A_W \
        + ehb_avg * const.EHB_A_W \
        + manual_score

    if (iron_bool):
        print('This fuck head is an iron?!')
        score *= const.IRON_SCALING

    print('Auto weight:', int(round(score, 0)))

    if score > 15.0:
        score = 15

    return int(round(score, 0))
