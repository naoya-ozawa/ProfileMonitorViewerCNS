#include <opencv2/opencv.hpp>
#include <iostream>
#include <TCanvas.h>
#include <TRint.h>

int main(int argc, char** argv){
	cv::Mat img, dst;

	img = cv::imread("./sample-images/Image__2019-10-02__17-35-26.png");
	cv::cvtColor(img, dst, cv::COLOR_BGR2GRAY);

	TRint rootapp("app",&argc,argv);

	TCanvas *c1 = new TCanvas();

//	std::cout << dst << std::endl; // retrieve entire matrix
//	std::cout << dst.row(250) << std::endl; // retrieve specific row
//	std::cout << dst.col(250) << std::endl; // retrieve specific column
	
	cv::Rect roi(415,345,400,400); // set ROI (left x-pos,upper y-pos,width,height)
//	std::cout << dst(roi) << std::endl; // retrieve specific column
	cv::rectangle(img,roi,cv::Scalar(0,255,0),2); // draw ROI range on image

//	cv::namedWindow("image", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
	cv::imshow("image", img);
//	cv::namedWindow("ROI", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
//	cv::imshow("ROI", dst(roi));
	cv::waitKey(0);

	cv::destroyAllWindows();

	rootapp.Run();

	return 0;
}
