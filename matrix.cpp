#include <opencv2/opencv.hpp>
#include <iostream>
#include <TCanvas.h>
#include <TPad.h>
#include <TStyle.h>
#include <TASImage.h>
#include <TH2D.h>
#include <TRint.h>

int main(int argc, char** argv){
	cv::Mat img, dst;

	// Choose image to display
	const char* imagepath = "./sample-images/Image__2019-10-02__17-35-26.png";

	// Set ROI
	int topleft_x = 415;
	int topleft_y = 345;
	int width = 400;
	int height = 400;


	// ROOT section
	//
	TASImage *cv_image = new TASImage(imagepath);
	UInt_t yPixels = cv_image->GetHeight();
	UInt_t xPixels = cv_image->GetWidth();
	UInt_t *argb = cv_image->GetArgbArray();
	TH2D *h = new TH2D("h","Histogram",xPixels,-1,1,yPixels,-1,1);
	for (int row=0; row<xPixels; ++row){
		for (int col=0; col<yPixels; ++col){
			int index = col*xPixels+row;
			float gray = float(argb[index]&0xff)/256;
			h->SetBinContent(row+1,yPixels-col,gray);
		}
	}

	cv_image->DrawRectangle(topleft_x,topleft_y,width,height,"#00ff00",3);

	TRint rootapp("app",&argc,argv);

	TCanvas *c1 = new TCanvas("c1","c1",1280,512);
	c1->Divide(2,1);

	c1->cd(1);

	cv_image->Draw();

	c1->cd(2);

//	TPad *hpad = new TPad("hpad","hpad",0,0.1,1,0.9,-1,-1);
//	hpad->Draw();

	TStyle *gStyle = new TStyle();
	gStyle->SetPalette(53);
	h->Draw("COLZ");



	// OpenCV section
	//
	img = cv::imread(imagepath);
	cv::cvtColor(img, dst, cv::COLOR_BGR2GRAY);

//	std::cout << dst << std::endl; // retrieve entire matrix
//	std::cout << dst.row(250) << std::endl; // retrieve specific row
//	std::cout << dst.col(250) << std::endl; // retrieve specific column
	
	cv::Rect roi(topleft_x,topleft_y,width,height); // set ROI (left x-pos,upper y-pos,width,height)
//	std::cout << dst(roi) << std::endl; // retrieve specific column
	cv::rectangle(img,roi,cv::Scalar(0,255,0),2); // draw ROI range on image

//	cv::namedWindow("image", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
//	cv::imshow("image", img);
//	cv::namedWindow("ROI", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
	cv::imshow("ROI", dst(roi));
	cv::waitKey(0);

	cv::destroyAllWindows();

	rootapp.Run();

	return 0;
}
