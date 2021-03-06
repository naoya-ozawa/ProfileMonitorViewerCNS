# Profile Monitor Viewer using the Basler Pylon Viewer

last updated 2020.02.12 by n.ozawa

## Labview streamer [NEW]

A streaming program has been created using LabView 2020. 
Note that it requires Vision Acquisition Software.
See the [official documentation](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x0UsCAI&l=en-GB) for details.

## simplehistostream.py

### Usage

```bash
$ python3 simplehistostream.py
```

### Input/Output

Connect a Basler GigE camera and run script. The image acquired by the camera is displayed as a 2D histogram (subplot 1). A rectangular region of interest (ROI) is defined on the 2D histogram by the four parameters (x_1, y_1, w, h) where (x_1, y_1) is the top-left position, and w and h are the width and height of the ROI. Another 2D histogram is drawn only showing the contents of the ROI region (subplot 2). 

As a rough indication of the beam intensity, the integration of the ROI histogram is calculated. The time evolution of this ROI brightness is plotted as a graph (subplot 3).

Each acquired image, the displayed window, and the brightness values at each time step are saved in the following directory format:

    <base directory of the script>
    └── profile-monitor-images
        └── <run-started-datetime>
                ├── PMImage_<run-started-datetime>.csv
                └── images
                        └── (acquired images in ```png``` format)

where ```<run-started-datetime>``` is in the form of ```YYMMDD_HHMMSSMMMMMM``` and the ```PMImage_<run-started-datetime>.csv``` stores the time elapsed from the start of the run and the ROI brightness obtained at that frame.

The ```PMImage_<run-started-datetime>.csv``` file contains 3 columns of values:

```
| data index | elapsed time | brightness |
```

The ```data index``` corresponds to the loop index of the ```FuncAnimation```, which starts at 0 and increases by 1 for each acquisition. The acquired image also has a suffix of this ```data index``` in its file name, so the time and brightness of the acquired image could be found by looking at the row with the same ```data index``` value.

The ```elapsed time``` corresponds to the time elapsed in seconds from the start of the streaming.

The ```brightness``` corresponds to the sum of all values within the ROI of the acquired grayscale image.

By default, the acquired image is saved every 30 seconds, and the brightness data is recorded every second.

### Environment

The aim of this script is to be usable with minimum external libraries. The requirements are

* Python 3.6
* Matplotlib 3.1
* Numpy 1.7
* [Pypylon 1.4](https://github.com/basler/pypylon)
* [Pylon Viewer 5.2 for Linux x86](https://www.baslerweb.com/jp/sales-support/downloads/software-downloads/pylon-5-2-0-linux-x86-64-bit/)

The script has been developed on Ubuntu 18.04 (Windows Subsystem for Linux) along with a Basler ace acA1300-60gm camera.

### Example

![Stream Example](./sample_stream.png)

## histostream.py

(under construction)

### Environment

The aim of this script is to provide a rapid streaming system using Qt libraries. The requirements are

* Python 3.6
* Matplotlib 3.1
* Numpy 1.7
* [Pypylon 1.4](https://github.com/basler/pypylon)
* [Pylon Viewer 5.2 for Linux x86](https://www.baslerweb.com/jp/sales-support/downloads/software-downloads/pylon-5-2-0-linux-x86-64-bit/)
* [PyQt 5.13](https://pypi.org/project/PyQt5/)
    * PySide2 did not work, although recommended on the PyQtGraph GitHub
* [PyQtGraph 0.11](https://github.com/pyqtgraph/pyqtgraph)
* [libxkbcommon-x11.so.0](https://stackoverflow.com/questions/57503682/matplotlib-qt-wsl-ubuntu-qt5/57503683#57503683)
    * Solutions to any other errors of this sort could be found by running ```export QT_DEBUG_PLUGINS=1``` before running the script

The script has been developed on Ubuntu 18.04 (Windows Subsystem for Linux) along with a Basler ace acA1300-60gm camera.
