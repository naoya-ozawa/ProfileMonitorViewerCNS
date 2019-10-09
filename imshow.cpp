#include <opencv2/opencv.hpp>

int main(){
	cv::Mat img;

	img = cv::imread("./sample-images/Image__2019-10-02__17-35-26.png");

	cv::imshow("title", img);
	cv::waitKey(0);

	return 0;
}
