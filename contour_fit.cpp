#include <iostream>
#include <opencv2/opencv.hpp>
using namespace cv;

private void fncDrawContours(Mat image, List contours){
	Point pt1 = new Point();
	Point pt2 = new Point();
	double data1[];
	double data2[];
	for (int i=0; i<contours.size(); ++i){
		Mat m = contours.get(i);
		if (m.rows() > 80){ // Ignore small contours
			for (int j=0; j<m.rows()-1;++j){
				data1 = m.get(j,0);
				data2 = m.get(j+1,0);
				pt1.x = data1[0];
				pt1.y = data1[1];
				pt2.x = data2[0];
				pt2.y = data2[1];
				Core.line(image, pt1, pt2, new Scalar(255,0,0),1);
			}
		}
	}
}

int main (int argc, char** argv){
	Mat gray = new Mat();
	Mat dst_bin = new Mat();
	Imgproc.cvtColor(image,gray,Imgproc.COLOR_RGB2GRAY);
	Imgproc.threshold(gray,dst_bin,0,255,Imgproc.THRESH_BINARY | Imgproc.THRESH_OTSU);
	Mat hierarchy = new Mat();
	List contours = new ArrayList(100);
	Imgproc.findContours(dst_bin,contours,hierarchy,Imgproc.CV_RETR_LIST,Imgproc.CV_CHAIN_APPROX_NONE);
	Imgproc.cvtColor(gray,gray,Imgproc.COLOR_GRAY2BGRA,4);
//	fncDrawContours(gray,contours);
	Imgproc.drawContours(gray,contours,-1,new Scalar(255,0,0),1);

	return 0;
}
