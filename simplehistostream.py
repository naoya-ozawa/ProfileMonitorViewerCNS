# ===============================================================================
#    This sample illustrates how to grab and process images using the CInstantCamera class.
#    The images are grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    The CInstantCamera class uses a pool of buffers to retrieve image data
#    from the camera device. Once a buffer is filled and ready,
#    the buffer can be retrieved from the camera object for processing. The buffer
#    and additional image data are collected in a grab result. The grab result is
#    held by a smart pointer after retrieval. The buffer is automatically reused
#    when explicitly released or when the smart pointer object is destroyed.
# ===============================================================================
from pypylon import pylon
from pypylon import genicam

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
import matplotlib.patches as patches
from matplotlib.widgets import Button
from collections import deque
import matplotlib.animation as animation

import sys
from datetime import datetime
import time
import gc

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

# Number of images to be grabbed.
countOfImagesToGrab = 100

# The exit code of the sample application.
exitCode = 0

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # demonstrate some feature access
    new_width = camera.Width.GetValue() - camera.Width.GetInc()
    if new_width >= camera.Width.GetMin():
        camera.Width.SetValue(new_width)

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer = 5

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(countOfImagesToGrab)

    # Create figure
    ax1 = plt.subplot(2,2,1)
#    im1 = ax1.matshow()
    ax2 = plt.subplot(2,2,2)
#    im2 = ax2.matshow()
    ax3 = plt.subplot(2,2,3)

    # Prepare brightness lists
    time_start = time.time()
    time_elapsed = deque()
    roi_brightness = deque()

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    counter = 0
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            def update(i):
                # Access the image data.
#               print("SizeX: ", grabResult.Width)
#               print("SizeY: ", grabResult.Height)
                img = grabResult.Array
#               print("Gray value of first pixel: ", img[0, 0])
#               print("Entire image: ", img)

                # Draw histogramized image
                ax1.set_data(img,0)
                current_time = datetime.strftime(datetime.now(),"%Y-%m-%d_%H-%M-%S-%f")
                ax1.title('Obtained Image (%s)'%current_time)
                if i == 1:
                    cmap = cm.get_cmap('jet',4)
                    bounds = np.linspace(0,maxscale,(maxscale+1)*20+1)
                    ax1.colorbar(cmap=colors.ListedColormap(['b','g','y','r']),boundaries=bounds,norm=colors.BoundaryNorm(bounds,cmap.N))
                ax1.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)
                roi = patches.Rectangle((x_1,y_1),width,height,angle,linewidth=1,edgecolor='r',facecolor='none')
                ax1.gca().add_patch(roi)

                # Draw the Zoomed image in the ROI
                img_roi = img[y_1:y_1+height+1, x_1:x_1+width+1]/maxscale
                del img
                gc.collect()
                ax2.set_data(img_roi,0)
                ax2.title('Region of Interest (x_1=%s, y_1=%s, w=%s, h=%s)'%(x_1,y_1,width,height))
                if i == 1:
                    cmap = cm.get_cmap('jet',4)
                    bounds = np.linspace(0,1,21)
                    ax2.colorbar(cmap=colors.ListedColormap(['b','g','y','r']),boundaries=bounds,norm=colors.BoundaryNorm(bounds,cmap.N))
                ax2.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)

                # Look at the time evolution of the ROI brightness
                current_brightness = np.sum(img_roi, axis=None)
                del img_roi
                gc.collect()
                time_now = time.time() - time_start
                time_elapsed.append(time_now)
                roi_brightness.append(current_brightness)
                if time_now > log_time:
                    time_elapsed.popleft()
                    roi_brightness.popleft()
                    gc.collect()
                ax3.clear()
                ax3.plot(time_elapsed,roi_brightness,'b-')
                ax3.xlim([time_now-log_time,time_now])
                ax3.autoscale(True,axis='y')
                ax3.xlabel('Elapsed Time [s]')
                ax3.ylabel('Brightness [a.u.]')
                ax3.title('Brightness within the ROI')
            
#               # Create a STOP button to stop acquisition
#               class Index(object):
#                   ind = 0
#                   def stop_acq(self, event):
#                       self.ind += 1
#                       raise SystemExit
#               callback = Index()
#               axstop = ax4.axes([0.7,0.05,0.1,0.075])
#               bstop = Button(axstop, 'STOP')
#               bstop.on_clicked(callback.stop_acq)

            # Draw the Histo/Graph
            histostream = animation.FuncAnimation(plt.gcf(), update, interval=100)
            def close(event):
                if event.key == 'q':
                    plt.close(event.canvas.figure)
                    raise SystemExit
            cid = plt.gcf().canvas.mpl_connect("key_press_event", close)
#            plt.tight_layout()
            plt.show()

        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        grabResult.Release()
    camera.Close()
    time_elapsed.clear()
    roi_brightness.clear()

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)
