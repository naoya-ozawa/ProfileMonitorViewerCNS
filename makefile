root_image_viewer:	image_viewer.cpp
	`root-config --cxx --cflags` -o image_viewer image_viewer.cpp `root-config --glibs`

imshow:	imshow.cpp
	g++ -o imshow imshow.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui

blob_detection:	blob_detection.cpp
	g++ -o blob_detection blob_detection.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_features2d

matrix:	matrix.cpp
	`root-config --cxx --cflags` -o matrix matrix.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui `root-config --glibs` -lASImage

histoimage:	histoimage.cpp
	`root-config --cxx --cflags` -o histoimage histoimage.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui `root-config --glibs` -lASImage

