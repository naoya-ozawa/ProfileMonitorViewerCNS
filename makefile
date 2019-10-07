root_image_viewer:	image_viewer.cpp
	`root-config --cxx --cflags` -o image_viewer image_viewer.cpp `root-config --glibs`
