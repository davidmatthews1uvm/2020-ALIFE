import matplotlib.image as mpimg
import matplotlib.pyplot as plt

img = mpimg.imread('test.png')

f = plt.figure()

imgplot = plt.imshow(img)

plt.show()
