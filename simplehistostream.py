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
from collections import deque
import matplotlib.animation as animation

import sys
from datetime import datetime
import gc
import os
import csv

# Maximum grayscale value of the image
maxscale = 255

# Set ROI position
x_1 = 465 # Top left position x-coordinate
y_1 = 335 # Top right position y-coordinate
width = 400
height = 400
angle = 0

# Logging time for ROI brightness display (in seconds)
log_time = 90

# Number of images to be grabbed.
#countOfImagesToGrab = 100

# Animation interval
shoot_int = 100 # ms

# The exit code of the sample application.
exitCode = 0

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    print("Press 'q' to stop streaming")
    print()

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
#    camera.MaxNumBuffer = 5
    camera.MaxNumBuffer = 10

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
#    camera.StartGrabbingMax(countOfImagesToGrab)
#    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # Retrieve sample image to set default canvas
    take_one_shot = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    sampleGrab = take_one_shot.Array

    # Create figure
    fig = plt.figure()
    ax1 = fig.add_subplot(2,2,1)
    im1 = ax1.matshow(sampleGrab)
    ax2 = fig.add_subplot(2,2,2)
    im2 = ax2.matshow(sampleGrab[y_1:y_1+height+1, x_1:x_1+width+1]/maxscale)
    ax3 = fig.add_subplot(2,2,3)
    ax4 = fig.add_subplot(2,2,4)

    # Set empty titles/labels
    ax1.set_title('')
    ax2.set_title('')
    ax3.set_title('')
    ax3.set_xlabel('')
    ax3.set_ylabel('')

    # Prepare brightness lists
    # Record the starting time for acquisition
    time_start = datetime.now()
    init_time = datetime.strftime(time_start, "%Y%m%d_%H%M%S%f")
    time_elapsed = deque()
    roi_brightness = deque()

    # Prepare output directories/folders/files
    data_path = 'profile-monitor-images'
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    run_path = data_path + '/' + init_time
    if not os.path.exists(run_path):
        os.mkdir(run_path)
    img_path = run_path + '/images'
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    stm_path = run_path + '/stream'
    if not os.path.exists(stm_path):
        os.mkdir(stm_path)
    writer = csv.writer(open(run_path+'/PMImage_'+init_time+'.csv','w',newline='',encoding='utf-8'))
    p_image = pylon.PylonImage()

    # Define action in each update cycle
    def update(i, ax1_title, ax2_title, ax3_title, ax3_xlabel, ax3_ylabel):
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            # Calling AttachGrabResultBuffer creates another reference to the
            # grab result buffer. This prevents the buffer's reuse for grabbing.
            p_image.AttachGrabResultBuffer(grabResult)

            # Clear the previous image and acquire the latest image
            plt.cla()
            img = grabResult.Array
            acquisition = datetime.now()
            acq_timestamp = datetime.strftime(acquisition,"%Y-%m-%d_%H-%M-%S-%f")
            save_index = init_time+'_'+str(i+1)

            # Draw histogram-ized image
            ax1.set_title(ax1_title + '(' + save_index + ')')
            im1.set_data(img)
            ax1.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)
            roi = patches.Rectangle((x_1,y_1),width,height,angle,linewidth=1,edgecolor='r',facecolor='none')
            ax1.add_patch(roi)

            # Draw the Zoomed image in the ROI
            img_roi = img[y_1:y_1+height+1, x_1:x_1+width+1]/maxscale
            del img
            gc.collect()
            im2.set_data(img_roi)
            ax2.set_title(ax2_title + '(x_1=' + str(x_1) + ', y_1=' + str(y_1) + ', w=' + str(width) + ', h=' + str(height) + ')')
            ax2.tick_params(axis='x',which='both',top=False,labeltop=False,labelbottom=True)

            # Look at the time evolution of the ROI brightness
            current_brightness = np.sum(img_roi, axis=None)
            del img_roi
            gc.collect()
            time_from_start = (acquisition - time_start).total_seconds()
            time_elapsed.append(time_from_start)
            roi_brightness.append(current_brightness)
            if time_from_start > log_time:
                deqtime = time_elapsed.popleft()
                shotframes = len(time_elapsed)
                deqtime = time_from_start - deqtime
                roi_brightness.popleft()
                gc.collect()
                fps = float(shotframes)/deqtime
                ax3.set_title(ax3_title + '(' + str(fps) + ' fps)')
            else:
                deqtime = 0.0
                shotframes = len(time_elapsed)
                deqtime = time_from_start - deqtime
                fps = float(shotframes)/deqtime
                ax3.set_title(ax3_title + '(' + str(fps) + ' fps)')
            ax3.plot(time_elapsed,roi_brightness,'b-')
            ax3.set_xlim([time_from_start-log_time,time_from_start])
            ax3.autoscale(True,axis='y')
            ax3.set_xlabel(ax3_xlabel)
            ax3.set_ylabel(ax3_ylabel)

            # Save output
            ax4.text(0.1,0.7,'Saved data at ' + acq_timestamp + '\n as ' + save_index,size='x-large',multialignment='left')
            ax4.text(0.1,0.4,'Elapsed time: ' + str(time_from_start) + ' s')
            ax4.text(0.1,0.3,'ROI Brightness: ' + str(current_brightness))
            ax4.set_axis_off()
            p_image.Save(pylon.ImageFileFormat_Tiff, img_path+'/image_'+save_index+'.tiff')
            plt.savefig(stm_path+'/stream_'+save_index+'.png')
            datalist = [i+1,time_from_start,current_brightness]
            writer.writerow(datalist)

            # In order to make it possible to reuse the grab result for grabbing
            # again, we have to release the image (effectively emptying the
            # image object).
            p_image.Release()
            grabResult.Release()

        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)



    # Draw the Histo/Graph as an animation
    histostream = animation.FuncAnimation(plt.gcf(), update, interval=shoot_int, fargs = ('Obtained Image ', 'Region of Interest ', 'ROI Brightness ', 'Elapsed Time [s]', 'Brightness [a.u.]'))

    # The closing method
    def close(event):
        if event.key == 'q':
            plt.close(event.canvas.figure)
            camera.StopGrabbing()
            camera.Close()
            time_elapsed.clear()
            roi_brightness.clear()
            raise SystemExit

    # Close action
    cid = plt.gcf().canvas.mpl_connect("key_press_event", close)

    # Set full-size window output by default
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    # Display
    plt.show()


except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)
