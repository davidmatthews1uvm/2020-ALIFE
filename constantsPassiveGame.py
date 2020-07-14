# -------------- User constants -------------------

startingPoints            = 1.0

startingPtsPerSec         = 0.1

ptsPerSecIncreaseInterval = 0.1

# -------------- Passive game parameters ----------

columnJustifications = ['right'                                       , 'center' , 'left'                        , 'right'  , 'center'  , 'left' ]

columnWidths         = [ 0.4                                          , 0.05     , 0.25                           , 0.1      , 0.05      , 0.15   ]

titles =               ['Options'                                     , 'Cost'   , 'Type:'                     , 'XP'     , 'XP/sec'  , 'User' ]

options =           [    [ "Unlock world 2"                           , 10240    , 'u2'                             ] ,
                         [ "Steal red"                                , 2560     , 'sr'                             ] ,
                         [ "Buy red"                                  , 640      , 'br'                             ] ,
                         [ "Show all bots"                            , 160      , 'all'                            ] ,
                         [ "Change speed"                             , 40       , '+'                              ] ,
                         [ ""                                         , 40       , '-'                              ] ,
                         [ "Create command"                           , 20       , '*jumping, e.g.'                 ] ,
                         [ "Show best bot"                            , 10       , 'best'                           ] ,
                         [ "Tell red it's better"                     , 0        , 'r'                              ] ,
                         [ "Tell green it's better"                   , 0        , 'g'                              ] ,
                         [ "Get help:"                                , 0        , '?'                              ] ,
                         [ "Start/continue:"                          , 0        , 'anything'                       ] ]

unlockEnvRequest              = 0
stealRequest                  = 1
buyRequest                    = 2
showAllBotsRequest            = 3
speedUpRequest                = 4
slowDownRequest               = 5
commandRequest                = 6
showBestBotRequest            = 7
aggressorReinforcementRequest = 8
defenderReinforcementRequest  = 9
helpRequest                   = 10
rawChat                       = 11

# ------------- Passive game screen parameters --------------

numColumns = len( titles )

numOptions = len( options )

numRows = 1 + numOptions # Include the title row 


backgroundColor = 0, 0, 0 # 255, 255, 255

font = "Anonymous_Pro.ttf"

fontSize = 24 

width = 1650 

depth = 300

columnHeight = int(depth / numRows )

panelWidth = int(width / numColumns)

panelDepth = int(depth / numRows)

textPadding = 10

maxSecondsBetweenChat = 10

rowForTitles = 0

columnForWhatCanIDo = 0

columnForCost = 1

columnForWhatDoIType = 2

columnForPoints = 3

columnForPtsPerSec = 4

columnForUserNames = 5 

# ------------------ Timings -----------------

timeBetweenPointsUpdates          = 0.1 # seconds

timeBetweenUsersUpdates           = 1.0 

timeBetweenOptionsUpdates         = 1.0

inactivateUserAfter               = 300.0  # seconds

# ----------------- Colors -------------------

colorCharToPygameColor = {
    'r': (255 , 0   , 0  ),
    'g': (0   , 255 , 0  ),
    'b': (50  , 50  , 255),
    'y': (255 , 255 , 0  ),
    'o': (255 , 140 , 0  ),
    'p': (186 , 85  , 211),
    'w': (255 , 255 , 255),
    'j': (189 , 252 , 201),
    'c': (0   , 238 , 238),
    's': (128 , 128 , 128)
}

