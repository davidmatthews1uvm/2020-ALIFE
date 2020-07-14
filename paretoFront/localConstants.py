# ----------------- Screen ----------------
width = 1000 

depth = 800

textColor        = (255,255,255)

# --------------- The sun -------------------

sizeOfSun        = 1 

numberOfSunsRays = 50

lengthOfSunsRays = depth / 12

# ----------------- Axes --------------------

xAxisIndentation = 0.15 * depth # 0.1 * depth

yAxisIndentation = xAxisIndentation 

xAxisWidth       = width - yAxisIndentation

yAxisHeight      = depth - xAxisIndentation

arrowHeadSize    = 0.05

arrowLineWidth   = 3

xAxisLabel       = 'Losses'

yAxisLabel       = 'Wins'

leaveSpaceOnTheRight = 0.1 
# Ensures robot with max losses does not go beyond the right-hand edge of the window

leaveSpaceAtTheTop   = 0.1
# Ensures robot with max wins does not go above the top edge of the window

# ------------------ Robots ----------------

circleSize      = 30

fontSize = 55

circleOffsetInPixels = 20 # To enable viewing of occluded circles.

colorCharToCircleOffset = {
    'r': [ 0 * circleOffsetInPixels , 0 * circleOffsetInPixels ],
    'g': [ 1 * circleOffsetInPixels , 0 * circleOffsetInPixels ], 
    'b': [ 2 * circleOffsetInPixels , 0 * circleOffsetInPixels ],
    'y': [ 0 * circleOffsetInPixels , 1 * circleOffsetInPixels ],
    'o': [ 1 * circleOffsetInPixels , 1 * circleOffsetInPixels ],
    'p': [ 2 * circleOffsetInPixels , 1 * circleOffsetInPixels ],
    'w': [ 0 * circleOffsetInPixels , 2 * circleOffsetInPixels ],
    'j': [ 1 * circleOffsetInPixels , 2 * circleOffsetInPixels ],
    'c': [ 2 * circleOffsetInPixels , 2 * circleOffsetInPixels ],
    's': [ 3 * circleOffsetInPixels , 0 * circleOffsetInPixels ]
}

# ----------------- Reinforcements ---------

userNameFontSize = 55 

speedOfReinforcement = 1
