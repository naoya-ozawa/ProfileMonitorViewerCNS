import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os
import csv

def grab_frame():
    n = 1500
    number_of_frames = 1500
    return np.random.rand(n, number_of_frames)

elapsetime = []
brightness = []
fps = []
dt_init_time = datetime.now()
init_time = datetime.strftime(dt_init_time, "%Y%m%d_%H%M%S%f")

ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3)
ax4 = plt.subplot(2,2,4)

im1 = ax1.matshow(grab_frame())
im2 = ax2.matshow(grab_frame())


if not os.path.exists('animation-sample-images'):
    os.mkdir('animation-sample-images')

run_path = 'animation-sample-images/' + init_time
img_path = run_path + '/images'
stm_path = run_path + '/stream'
if not os.path.exists(run_path):
    os.mkdir(run_path)
if not os.path.exists(img_path):
    os.mkdir(img_path)
if not os.path.exists(stm_path):
    os.mkdir(stm_path)

def update(i):
    image = grab_frame()
    im1.set_data(image)
    #ax1.savefig(img_path+"/image_"+init_time+"_"+str(i)+".tiff")
    # Saving images should be implemented using the pypylon method
    im2.set_data(grab_frame())
    dt_current_time = datetime.now()
    current_time = datetime.strftime(dt_current_time, "%Y%m%d_%H%M%S%f")
    elapsed_time = (dt_current_time - dt_init_time).total_seconds()
    elapsetime.append(elapsed_time)
    current_fps = float(i)/(elapsed_time)
    fps.append(current_fps)
    b_now = np.sum(image, axis=None)
    brightness.append(b_now)
    ax3.clear()
    ax3.plot(elapsetime, brightness)
    ax4.clear()
    ax4.plot(elapsetime, fps)
    datalist = [elapsed_time,b_now]
    plt.savefig(stm_path+"/stream_"+init_time+"_"+str(i)+".png")
    writer.writerow(datalist)

mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
writer = csv.writer(open(run_path+"/animation_data_"+init_time+".csv","w",newline='',encoding="utf-8"))
ani1 = animation.FuncAnimation(plt.gcf(), update, interval=50)

def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)
#        with open(run_path+"/animation_data_"+init_time+".csv","w",newline='',encoding="utf-8") as wf:
#            writer = csv.writer(wf, lineterminator="\n")
#            datalist = np.array([elapsetime,brightness]).T.tolist()
#            writer.writerows(datalist)


cid = plt.gcf().canvas.mpl_connect("key_press_event", close)

plt.show()
