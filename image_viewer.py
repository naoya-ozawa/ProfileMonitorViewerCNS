import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

sampleimage = './sample-images/Image__2019-10-02__17-35-26.png'

img = plt.imread(sampleimage)

roi = img[275:825,350:900]
print(roi.shape) #=> ROI image size
print(roi.ndim)
print(roi[260][110])

# Display image
plt.imshow(img)
plt.imshow(roi)

# Display image as 2D-hist
#fig = plt.figure()
#ax = fig.add_subplot(111)
#H = ax.hist2d(roi, bins=65)
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#fig.colorbar(H[3],ax=ax)

# Export image as TXT file
np.savetxt('./sample-images/Image__2019-10-02__17-35-26.txt', roi, fmt='%.2f')

plt.show()
