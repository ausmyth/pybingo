# general constants
SECS_IN_DAY = 86400
RECENT_DAYS_COUNT = 200
SLAYER_GOAL_XP = 8771558
AVERAGE_DAYS_COEFF = 14

# weights for scoring
EHP_T_W = 0.10 # ehp total weight
EHB_T_W = 0.25 # ehb total weight
EHP_A_W = 0.10 # ehp average for two week period over the last 200 days
EHB_A_W = 0.30 # ehb average for two week period over the last 200 days
TILE_W = 0.20 # Weight for "can u do all tiles" score (if hiscore kc, can do that tile)
SLAYER_W = 0.10 # Just off slayer level

# since irons will be gear and alt restricted, scale them down by a %
IRON_SCALING = 0.90

# names to score board ability
TILE_NAMES_LIST = [
    "Artio",
    "Callisto",
    "Vetion",
    "Calvarion",
    "Venenatis",
    "Spindel",
    "Chambers of Xeric",
    "Chambers of Xeric Challenge Mode",
    "Theatre of Blood",
    "Tombs of Amascut",
    # "Chaos Fanatic",
    # "Crazy Archaeologist",
    # "Scorpia",
    # "The Nightmare",
    # "Phosanis Nightmare",
    "Vorkath",
    "Nex",
    "Cerberus",
    "Grotesque Guardians",
    "Zalcano",
    "The Gauntlet",
    "The Corrupted Gauntlet",
    # "Alchemical Hydra",
    # "Corporeal Beast",
    # "Thermonuclear Smoke Devil",
    "Abyssal Sire",
    "Phantom Muspah",
    "Kraken",
    "Sarachnis",
    "Kalphite Queen",
    # "Dagannoth Rex",
    # "Dagannoth Prime",
    # "Dagannoth Supreme",
    "Zulrah",
    # dt bosses
    'Duke Sucellus',
    'The Leviathan',
    'The Whisperer',
    'Vardorvis',
]
