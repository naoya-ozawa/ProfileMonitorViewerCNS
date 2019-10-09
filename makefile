root_image_viewer:	image_viewer.cpp
	`root-config --cxx --cflags` -o image_viewer image_viewer.cpp `root-config --glibs`

imshow:	imshow.cpp
	g++ -o imshow imshow.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui
