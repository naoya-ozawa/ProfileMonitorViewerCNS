import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def grab_frame():
    n = 1500
    number_of_frames = 1500
    return np.random.rand(n, number_of_frames)

elapsetime = []
brightness = []
fps = []
init_time = time.time()

ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3)
ax4 = plt.subplot(2,2,4)

im1 = ax1.matshow(grab_frame())
im2 = ax2.matshow(grab_frame())

def update(i):
    image = grab_frame()
    im1.set_data(image)
    im2.set_data(grab_frame())
    current_time = time.time()
    elapsetime.append(current_time-init_time)
    current_fps = float(i)/(current_time-init_time)
    fps.append(current_fps)
    b_now = np.sum(image, axis=None)
    brightness.append(b_now)
    ax3.clear()
    ax3.plot(elapsetime, brightness)
    ax4.clear()
    ax4.plot(elapsetime, fps)

ani1 = animation.FuncAnimation(plt.gcf(), update, interval=50)

def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)

cid = plt.gcf().canvas.mpl_connect("key_press_event", close)

plt.show()
