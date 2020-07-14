import pickle
from scipy.stats import mannwhitneyu
import numpy as np

cvscores = pickle.load(open("cvscores.p", 'rb'))
cvscores_control = pickle.load(open("cvscores_control.p", 'rb'))
cvscores_bool = pickle.load(open("cvscores_bool.p", 'rb'))
cvscores_bool_control = pickle.load(open("cvscores_bool_control.p", 'rb'))

# using 2 means we have accuracy score, but if 0 is used we get loss and  with 1 we get MAE
cvscores = np.array(cvscores)[:,2]
cvscores_control = np.array(cvscores_control)[:,2]
cvscores_bool = np.array(cvscores_bool)[:,2]
cvscores_bool_control = np.array(cvscores_bool_control)[:,2]


print("With reinforcements between -1 and 1")
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
print("And control:")
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores_control), np.std(cvscores_control)))
print("With reinforcements that are rounded to -1 or 1")
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores_bool), np.std(cvscores_bool)))
print("And control:")
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores_bool_control), np.std(cvscores_bool_control)))

print("Mann Whitney with reinforcements between -1 and 1")

stat, p = mannwhitneyu(cvscores, cvscores_control)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')
    
print("Man Whitney with reinforcements that are rounded to -1 or 1")

stat, p = mannwhitneyu(cvscores_bool, cvscores_bool_control)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

