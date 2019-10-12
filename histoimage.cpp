#include <opencv2/opencv.hpp>
#include <iostream>
#include <TCanvas.h>
#include <TPad.h>
#include <TStyle.h>
#include <TASImage.h>
#include <TH2D.h>
#include <TPolyLine.h>
#include <TRint.h>

int main(int argc, char** argv){

	// Choose image to display
	const char* imagepath = "./sample-images/Image__2019-10-02__17-35-26.png";

	// Set ROI
	int topleft_x = 415;
	int topleft_y = 345;
	int width = 400;
	int height = 400;


	// Read image into histo
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

	TCanvas *c1 = new TCanvas("c1","c1",1280,1024);
	c1->Divide(2,2);

	// Draw original image with ROI rectangle
	c1->cd(1);

	cv_image->Draw();

	// Draw converted histogram with ROI rectangle
	c1->cd(2);

	TStyle *gStyle = new TStyle();
	gStyle->SetPalette(53);
	h->Draw("COLZ");

	TPolyLine *roihist = new TPolyLine(5);
	double x_1 = 2.0*double(topleft_x)/double(xPixels) - 1.0;
	double y_1 = 2.0*double(yPixels-topleft_y)/double(yPixels) - 1.0;
	double ww = 2.0*double(width)/double(xPixels);
	double hh = 2.0*double(height)/double(yPixels);
	roihist->SetPoint(0,x_1,y_1);
	roihist->SetPoint(1,x_1+ww,y_1);
	roihist->SetPoint(2,x_1+ww,y_1-hh);
	roihist->SetPoint(3,x_1,y_1-hh);
	roihist->SetPoint(4,x_1,y_1);
	roihist->SetLineColor(3);
	roihist->SetLineWidth(3);
	roihist->Draw();

	c1->Update();
	c1->Modified();

	rootapp.Run();

	return 0;
}
