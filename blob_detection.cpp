#include <cstdio>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/features2d.hpp>

using namespace cv;

int main(int argc, char** argv){
//	cv::Mat img, dst;

	// Choose image to display
//	const char* imagepath = "./sample-images/Image__2019-10-02__17-35-26.png";
	const char* imagepath = "./sample-images/blob_detection_sample.png";

	// Set ROI
	int topleft_x = 415;
	int topleft_y = 345;
	int width = 400;
	int height = 400;

	Mat img = imread(imagepath, IMREAD_GRAYSCALE);

	// Set up SimpleBlobDetector parameters
	SimpleBlobDetector::Params params;

	// Change thresholds
//	params.minThreshold = 10;
//	params.maxThreshold = 200;

	// Filter by Area.
//        params.filterByArea = true;
//        params.minArea = 1500;

	// Filter by Circularity
//        params.filterByCircularity = true;
//        params.minCircularity = 0.1;

	// Filter by Convexity
//        params.filterByConvexity = true;
//        params.minConvexity = 0.87;

	// Filter by Inertia
//        params.filterByInertia = true;
//        params.minInertiaRatio = 0.01;

	// Storage for blobs
	std::vector<KeyPoint> keypoints;
	// Set up detector with params
	Ptr<SimpleBlobDetector> detector = SimpleBlobDetector::create(params);

	// Detect blobs
	detector->detect( img, keypoints );

	// Draw detected blobs as red circles
	// DrawMatchesFlags::DRAW_RICH_KEYPOINTS flag 
	// ensures the size of the circle corresponds to the size of the blob
	Mat im_with_keypoints;
	drawKeypoints( img, keypoints, im_with_keypoints, Scalar(0,0,255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );

	// Show blobs
	imshow("keypoints", im_with_keypoints );
	waitKey(0);

//	cv::Rect roi(topleft_x,topleft_y,width,height); // set ROI (left x-pos,upper y-pos,width,height)
//	std::cout << dst(roi) << std::endl; // retrieve specific column
//	cv::rectangle(img,roi,cv::Scalar(0,255,0),2); // draw ROI range on image

//	cv::namedWindow("image", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
//	cv::imshow("image", img);
//	cv::namedWindow("ROI", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
//	cv::imshow("ROI", dst(roi));
//	cv::waitKey(0);

	destroyAllWindows();


	return 0;
}
