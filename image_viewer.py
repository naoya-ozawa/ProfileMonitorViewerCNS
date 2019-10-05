import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

sampleimage = './sample-images/Image__2019-10-02__17-35-26.png'

img = plt.imread(sampleimage)
type(img) #=> numpy.ndarray
img.size #=> image size

# Display image
plt.imshow(img)
plt.show()
