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

import sys
from datetime import datetime

# Maximum grayscale value of the image
maxscale = 255

# Set ROI position
x_1 = 415 # Top left position x-coordinate
y_1 = 345 # Top right position y-coordinate
width = 400
height = 400
angle = 0

# Number of data points to display in the ROI brightness logger
logging = 15

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
    plt.figure()
    plt.ion()

    # Prepare brightness lists
    time_elapsed = []
    roi_brightness = []

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    counter = 0
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            counter = counter + 1
            # Access the image data.
#            print("SizeX: ", grabResult.Width)
#            print("SizeY: ", grabResult.Height)
            img = grabResult.Array
#            print("Gray value of first pixel: ", img[0, 0])
#            print("Entire image: ", img)

            # Draw histogramized image
            plt.subplot(2,2,1)
            plt.matshow(img,0)
            current_time = datetime.strftime(datetime.now(),"%Y-%m-%d_%H-%M-%S-%f")
            plt.title('Obtained Image (%s)'%current_time)
            if counter == 1:
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
            if counter == 1:
                cmap = cm.get_cmap('jet',4)
                bounds = np.linspace(0,1,21)
                plt.colorbar(cmap=colors.ListedColormap(['b','g','y','r']),boundaries=bounds,norm=colors.BoundaryNorm(bounds,cmap.N))
            plt.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)

            # Look at the time evolution of the ROI brightness
            plt.subplot(2,2,3)
            current_brightness = np.sum(img_roi, axis=None)
            time_elapsed.extend([counter])
            roi_brightness.extend([current_brightness])
            plt.plot(time_elapsed[-logging:],roi_brightness[-logging:],'xb-')
            plt.xlim([counter-logging,counter])
            plt.autoscale(True,axis='y')
            plt.xlabel('Captured Frames')
            plt.ylabel('Brightness [a.u.]')
            plt.title('Brightness within the ROI')

            # Draw the Histo/Graph
#            plt.tight_layout()
            plt.show()
            plt.pause(0.5)

        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        grabResult.Release()
    camera.Close()

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)
