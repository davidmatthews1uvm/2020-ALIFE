import sys
sys.path.insert(0, '..')

from visualizations.cumulativeYesVotes import CUMULATIVE_YES_VOTES

cyv = CUMULATIVE_YES_VOTES()

if cyv.Sufficient_Conditions_For_Drawing():
    cyv.Collect_Data()
    cyv.Show()
