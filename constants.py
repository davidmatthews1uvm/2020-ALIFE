databaseTableBuyRequests        = "BuyRequests(Id INT, Date TIMESTAMP, RobotID INT, UserID INT, Successful INT)"

databaseTableChatEntries        = "ChatEntries(Id Int, Entry TEXT, Date TIMESTAMP, UserID INT)"

databaseTableChatHelp           = "ChatHelp(Id Int, Entry TEXT, Date TIMESTAMP, UserID INT)"

databaseTableChatUniqueCommands = "UniqueCommands(Command TEXT, commandEncoding BLOB, Date TIMESTAMP, Votes INT, UserID INT)"

databaseTableCommands           = "Commands(Id INT, Entry TEXT, Date TIMESTAMP, UserID INT)"

databaseTableEnvironments       = "Environments(Id INT, Locked INT)"

databaseTableEvaluations        = "Evaluations(Id INT, RobotId INT, RobotColor CHAR, command CHAR, Date TIMESTAMP, Speed INT, EnvironmentId INT, SimulationType INT)"

databaseTableMessages           = "Messages(Id INT, message CHAR, Date TIMESTAMP)"

databaseTableReinforcements     = "Reinforcements(Id INT, EvaluationId INT, RobotId INT, Reinforcement TEXT, Date TIMESTAMP, UserID INT, Digested INT)"

databaseTableRobots             = "Robots(Id INT, colorIndex INT, parentID INT, BirthDate TIMESTAMP, DeathDate TIMESTAMP, alive INT, OwnerID INT, Locked INT)"

databaseTableShowAllRequests    = "ShowAllRequests(Id INT, Date TIMESTAMP, UserID INT, Honored INT)"

databaseTableShowBestRequests   = "ShowBestRequests(Id INT, Date TIMESTAMP, UserID INT, Honored INT)"

databaseTableSpeedChanges       = "SpeedChanges(Id INT, FasterOrSlower TEXT, Date TIMESTAMP, UserID INT, Honored INT)"

databaseTableStealRequests      = "StealRequests(Id INT, Date TIMESTAMP, RobotID INT, UserID INT, Successful INT)"

databaseTableUsers              = "Users(Id INT, Name TEXT, PosReinforcements INT,  NegReinforcements INT, CommandCount INT, DateAdded TIMESTAMP, Points REAL, PointsPerSec REAL, StartInfoClaims INT, EndInfoClaims INT)"

# ------------- Environment parameters ------------

ENVIRONMENT_NUMBERS_AS_CHARS = ['1','2','3','4','5','6','7','8','9']

NUM_ENVIRONMENTS_AVAILABLE = 9

# --------------- Simulation parameters -------------

ACCURACY = 1 # minimum is 1. Higher numbers mean more accuracy.

SIMULATE_BIRTH_DE_NOVO = 0

SIMULATE_BIRTH_FROM_AGGRESSOR = 1

SIMULATE_DEATH = 2

SIMULATE_SURVIVAL = 3

SIMULATE_ALL = 4

SIMULATE_ALL_ORIGINAL_BOTS = 5

SIMULATE_BEST = 6

SIMULATE_DEATH_FROM_OLD_AGE = 7

SIMULATE_BIRTH = SIMULATE_BIRTH_DE_NOVO or SIMULATE_BIRTH_FROM_AGGRESSOR

MINIMUM_SPEED = 1

MAXIMUM_SPEED = 4

DEFAULT_SPEED = 2 

# ------------- Visualization parameters ------------

DRAW_PHYLO_TREE = 0

DRAW_PARETO_FRONT = 1

DRAW_CUMULATIVE_YES_VOTES = 2

VISUALIZATION_TYPES = 3

# ------------- Visual parameters -------------------

colors = ['r', 'g', 'b', 'y', 'o', 'p', 'w', 'j', 'c', 's']

colorsUppercase = ['R', 'G', 'B', 'Y', 'O', 'P', 'W', 'J', 'C', 'S']

upperToLowerCaseColors = {
    'R': 'r',
    'G': 'g',
    'B': 'b',
    'Y': 'y',
    'O': 'o',
    'P': 'p',
    'W': 'w',
    'J': 'j',
    'C': 'c',
    'S': 's'
}

upperToLowerCaseReinforcements = {'Y': 'y', 'N': 'n'}

reinforcements = ['y', 'n']
reinforcementsUppercase = ['Y', 'N']


colorNames = [
    '[r]ed   ',
    '[g]reen ',
    '[b]lue  ',
    '[y]ellow',
    '[o]range',
    '[p]urple',
    '[w]hite ',
    '[j]ade  ',
    '[c]yan  ',
    '[s]ilver'
]

colorNamesNoParens = [
    'red',
    'green',
    'blue',
    'yellow',
    'orange',
    'purple',
    'white',
    'jade',
    'cyan',
    'silver'
]

colorNameDict = {
    'r': 'red',
    'g': 'green',
    'b': 'blue',
    'y': 'yellow',
    'o': 'orange',
    'p': 'purple',
    'w': 'white',
    'j': 'jade',
    'c': 'cyan',
    's': 'silver'
}

colorNameDictWithParens = {
    'r': '[r]ed',
    'g': '[g]reen',
    'b': '[b]lue',
    'y': '[y]ellow',
    'o': '[o]range',
    'p': '[p]urple',
    'w': '[w]hite',
    'j': '[j]ade',
    'c': '[c]yan',
    's': '[s]ilver'
}

colorLetterToEscapeCode = {
    'r': '\u001b[38;5;196m',
    'g': '\u001b[38;5;47m',
    'b': '\u001b[38;5;27m',
    'y': '\u001b[38;5;11m',
    'o': '\u001b[38;5;208m',
    'p': '\u001b[38;5;201m',
    'w': '\u001b[38;5;231m',
    'j': '\u001b[38;5;121m',
    'c': '\u001b[38;5;87m',
    's': '\u001b[38;5;7m',
}

colorLetterToColorIndex = {
    'r': 0,
    'g': 1,
    'b': 2,
    'y': 3,
    'o': 4,
    'p': 5,
    'w': 6,
    'j': 7,
    'c': 8,
    's': 9 
}


colorLetterToPygameColor = {
    'r': (255,0,0),
    'g': (0,255,0),
    'b': (75,75,255),
    'y': (255,255,0),
    'o': (255,128,0),
    'p': (255,131,250),
    'w': (255,255,255),
    'j': (193,255,193),
    'c': (151,255,255),
    's': (150,150,150)
}

colorRGBs = [
    [1, 0, 0],  # red
    [0, 1, 0],  # green
    [0, 0, 1],  # blue
    [1, 1, 0],  # yellow
    [1, 0.65, 0],  # orange
    [0.5, 0, 0.5],  # purple
    [1, 1, 1],  # white
    [0.5, 1, 0.5],  # light green
    [0, 1, 1],  # cyan
    [0.5, 0.5, 0.5]  # silver
]

noFade = 0

fadeOut = 1

fadeIn = 2

swarmPositionOffsets = {
    0: [0, 0, 0],
    1: [-10, 10, 0],
    2: [-20, 20, 0],
    3: [-30, 30, 0],
    4: [-40, 40, 0],
    5: [-50, 50, 0],
    6: [-60, 60, 0],
    7: [-70, 70, 0],
    8: [-80, 80, 0],
    9: [-90, 90, 0]
}

# Minimal occlusion
swarmDrawOffsets = {
    0: [0 + 0, 0 + 0, 0],
    1: [10 - 1, -10 + 1, 0],
    2: [20 - 2, -20 + 2, 0],
    3: [30 - 3, -30 + 3, 0],
    4: [40 - 3, -40 + 1, 0],
    5: [50 + 0, -50 + 2, 0],
    6: [60 - 1, -60 + 3, 0],
    7: [70 + 0, -70 + 4, 0],
    8: [80 - 2, -80 + 4, 0],
    9: [90 + 0.5, -90 + 1, 0]
}

# One behind the other
#swarmDrawOffsets = {
#    0: [0     ,   0 + 0, 0],
#    1: [10 - 1, -10 + 1, 0],
#    2: [20 - 2, -20 + 2, 0],
#    3: [30 - 3, -30 + 3, 0],
#    4: [40 - 4, -40 + 4, 0],
#    5: [50 - 5, -50 + 5, 0],
#    6: [60 - 6, -60 + 6, 0],
#    7: [70 - 7, -70 + 7, 0],
#    8: [80 - 8, -80 + 8, 0],
#    9: [90 - 9, -90 + 9, 0]
#}


# Event types --------------------------------------

EVENT_SPAWN_DE_NOVO = 0

EVENT_SPAWN_FROM_BOT = 1

EVENT_DEATH = 2

EVENT_SURVIVAL = 3

# Evolutionary parameters --------------------------

popSize = len(colors)

playBlind = False

# Command parameters -------------------------------

defaultCommands = [
    'moving',
    'being interesting'
]

# ------------------ Robot parameters --------------

maximizeLight = 0
maximizePos = 1
evaluationTime = 1500

JOINT_ANGLE_MAX = -3.14159 / 2.0 # 4.0 # 8.0

MAX_HEAD_ROTATION = 3.14159 / 2.0

maxDepth = 4

maxChildren = 2

length = 1.5 * (0.5 / 4.0)

radius = 1.5 * (0.05 / 4.0)

eyeRadius = radius * 2

pupilRadius = eyeRadius * 0.5

deathAge = 5 #In Days

minimumAmountOf3Dness = 0.0

maximumAmountOf3Dness = 2.0

newRobotInitial3Dness = 0.0

newRobotFinal3Dness   = 0.5

# ----------- Neural network parameters ------------

SENSOR_NEURON = 0

AUDITORY_NEURON = 1

HIDDEN_NEURON = 2

MOTOR_NEURON = 3

NUM_HIDDEN_NEURONS = 5

TAU_MAX = 0.5

TAU_MIN = 0.1

# -------------- School parameters ----------------

NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS = 3 

# ------------------- Help responses can be no longer than this -------------------------------------v"
validHelpRequests = {

'?'           : "",

'?body'       : "Each robot is made up of different parts. They're connected together with joints.",

'?birth'      : "When a robot is born, it hears the current command and then starts moving.",

'?brain'      : "Each robot's brain determines how it moves in response to a command and its sensors.",

'?commands'   : "Type in any command you like, but try to issue ones the bots might evolve to obey.",

'?death'      : "Periodically, less obedient robots (many losses and few wins) are deleted.",

'?disobey'    : "Robots that collect lots of losses are considered disobedient.",

'?evolution'  : "Disobedient robots can be killed by obedient robots and replaced by their offspring.",

'?goal'       : "Help us discover which commands the bots can evolve to obey.",

'?graphs'     : "Three graphs help you understand the robots' progress: ?robotStats ?familyTree ?shadow.",

'?joints'     : "Pairs of robot body parts are connected with joints that rotate like your knee.",

'?killing'    : "A robot with more wins and less losses than another robot can kill it.",

'?learning'   : "These robots do not learn. They simply act, and if they tend to obey, they live.",

'?life'       : "Periodically, more obedient robots (many wins and few losses) spawn offspring.",

'?movement'   : "At each time step, the bot's brain receives info about the angle of each joint.",

'?muscles'    : "A robot's brain sends forces to each joint in a robot's body.",

'?mybots'     : "",

'?obey'       : "Robots that collect lots of wins and few losses are considered obedient.",

'?spawning'   : "Robots spawn offspring that have similar, yet not identical, bodies and brains.",

'?robots'     : "There are 10 robots in all. Some are more obedient than others.",

'?robotStats' : "This graph shows how many commands the robot can obey so far.",

'?score'      : "A bot's score s says it's gotten at least s wins for at least s commands. (see ?mybots).",

'?sensors'    : "Each robot has multiple sensors that send signals to the robot's brain.",

'?shadow'     : "Robots in shadow (the gray regions) can be killed by robots who aren't.",

'?touch'      : "Body parts darken when they hit something. These events are sent to the bot's brain.",

'?familyTree' : "This graph shows how the robots are related. See also ?evolution.",

'?vision'     : "The lengths of the laser beams issuing from the bots' eyes are sent to their brains.",

'?whatdoido'  : "Help train our robots! The bottom panel shows you what you can currently do.",

'?whatsthis'  : "This is Twitch Plays Robotics, the first school for robots where you are the teacher."

}
# ------------------- Help responses can be no longer than this -------------------------------------v"

# -------------- Chatbot parameters ---------------

WIDTH_OF_LEFTHAND_CHATBOT_OUTPUT = 10

WIDTH_OF_RIGHTHAND_CHATBOT_OUTPUT = 75

longestUserMessage = 30

timeBetweenConnectionResets = 60. # seconds 

# ------------- Ticker tape parameters ------------

tickerTapeSpeed = 3

tickerTapeRandomMessages = {

'unmuteMessage'   : "Unmute us! We're better with sound.",

'missionMessage'  : "Your current mission: help evolve a bot that collects XXX winZZZ for each of XXX commandZZZ.",

'bestBotMessage'  : "YYY is currently the best bot: it's collected XXX winZZZ for each of XXX commandZZZ."

}

# ------------ Speech parameters -----------------

SPEECH_COMMAND_SPEED       = 200 # words per minute

SPEECH_REINFORCEMENT_SPEED = 400
