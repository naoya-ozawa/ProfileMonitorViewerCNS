# Contains an Image Event Handler that prints a message for each event method call.
# Additionally displays histo-ed image and ROI brightness.

from pypylon import pylon
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
import matplotlib.patches as patches
from datetime import datetime
import time

# Maximum grayscale value of the image
maxscale = 255

# Set ROI position
x_1 = 415 # Top left position x-coordinate
y_1 = 345 # Top right position y-coordinate
width = 400
height = 400
angle = 0

# Logging time for ROI brightness display (in seconds)
log_time = 15

class ImageEventPrinter(pylon.ImageEventHandler):
    def OnImagesSkipped(self, camera, countOfSkippedImages):
        print("OnImagesSkipped event for device ", camera.GetDeviceInfo().GetModelName())
        print(countOfSkippedImages, " images have been skipped.")
        print()

    def OnImageGrabbed(self, camera, grabResult):
        print("OnImageGrabbed event for device ", camera.GetDeviceInfo().GetModelName())

        # Create figure
        plt.figure()
        plt.ion()

        # Prepare brightness lists
        time_start = time.time()
        time_elapsed = []
        roi_brightness = []

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
#            print("SizeX: ", grabResult.GetWidth())
#            print("SizeY: ", grabResult.GetHeight())
            img = grabResult.GetArray()
#            print("Gray values of first row: ", img[0])
#            print()

            # Draw histogramized image
            plt.subplot(2,2,1)
            plt.matshow(img,0)
            current_time = datetime.strftime(datetime.now(),"%Y-%m-%d_%H-%M-%S-%f")
            plt.title('Obtained Image (%s)'%current_time)
            cmap = cm.get_cmap('jet',4)
            bounds = np.linspace(0,maxscale,(maxscale+1)*20+1)
            plt.colorbar(cmap=colors.ListedColormap(['b','g','y','r']),boundaries=bounds,norm=colors.BoundaryNorm(bounds,cmap.N))
            plt.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)
            roi = patches.Rectangle((x_1,y_1),width,height,angle,linewidth=1,edgecolor='r',facecolor='none')
            plt.gca().add_patch(roi)
  
            # Draw the Zoomed image in the ROI
            plt.subplot(2,2,2)
            img_roi = img[y_1:y_1+height+1, x_1:x_1+width+1]/maxscale
            plt.matshow(img_roi,0)
            plt.title('Region of Interest (x_1=%s, y_1=%s, w=%s, h=%s)'%(x_1,y_1,width,height))
            cmap = cm.get_cmap('jet',4)
            bounds = np.linspace(0,1,21)
            plt.colorbar(cmap=colors.ListedColormap(['b','g','y','r']),boundaries=bounds,norm=colors.BoundaryNorm(bounds,cmap.N))
            plt.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)
            
            # Look at the time evolution of the ROI brightness
            plt.subplot(2,2,3)
            current_brightness = np.sum(img_roi, axis=None)
            time_now = time.time() - time_start
            time_elapsed.extend([time_now])
            roi_brightness.extend([current_brightness])
            plt.plot(time_elapsed,roi_brightness,'b-')
            plt.xlim([time_now-log_time,time_now])
            plt.autoscale(True,axis='y')
            plt.xlabel('Elapsed Time [s]')
            plt.ylabel('Brightness [a.u.]')
            plt.title('Brightness within the ROI')

            # Draw the Histo/Graph
#            plt.tight_layout()
            plt.show()
            plt.pause(0.1)

        else:
            print("Error: ", grabResult.GetErrorCode(), grabResult.GetErrorDescription())
