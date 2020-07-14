import matplotlib.pyplot as plt
import numpy as np

f = plt.figure()

sp = f.add_subplot(111)

plt.xlim([0, 100])

plt.ylim([0, 100])

for i in range(0, 5):
    dots = np.random.randint(0, 100, [2, 50])
    sp.clear()
    sp.plot(dots[0, :], dots[1, :], 'ko')
    f.show()
