#include <iostream>
#include <TMath.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TStyle.h>
#include <TASImage.h>
#include <TH2D.h>
#include <TPolyLine.h>
#include <TLatex.h>
#include <TRint.h>

double round_off(double value, double position){
	double multiplied = value * TMath::Power(10.,position);
	double rounded = std::round(multiplied);
	return rounded / TMath::Power(10.,position);
}

int main(int argc, char** argv){

	// Choose image to display
//	const char* imagepath = "./sample-images/Image__2019-10-02__17-35-26.png"; // Beam On
//	const char* imagepath = "./sample-images/106793-17-direct__23113341__20191011_164312788_1.tiff"; // Beam Off 
	const char* imagepath = "./../profile-monitor-images/20191023_102027334782/PylonViewerImages/106793-17-direct__23113341__20191023_101920953_1.tiff"; // Position calibration 2019.10.23

	// Set ROI
	int topleft_x = 465;
	int topleft_y = 335;
	int width = 400;
	int height = 400;


	// Read image into histo

	TASImage *image = new TASImage(imagepath);
	std::cout << "Image Opened" << std::endl;
	UInt_t yPixels = image->GetHeight();
	UInt_t xPixels = image->GetWidth();
	UInt_t *argb = image->GetArgbArray();
	TH2D *histo = new TH2D("histo","Histogram",xPixels,-1,1,yPixels,-1,1);
	for (int row=0; row<xPixels; ++row){
		for (int col=0; col<yPixels; ++col){
			int index = col*xPixels+row;
			float gray = float(argb[index]&0xff)/256;
			histo->SetBinContent(row+1,yPixels-col,gray);
		}
	}

	image->DrawRectangle(topleft_x,topleft_y,width,height,"#00ff00",3);

	TRint rootapp("app",&argc,argv);

	TCanvas *c1 = new TCanvas("c1","c1",1280,1024);
	c1->Divide(2,2);

	// Draw original image with ROI rectangle
	c1->cd(1);

	image->Draw();


	// Draw converted histogram with ROI rectangle
	c1->cd(2);

	TStyle *gStyle = new TStyle();
	gStyle->SetPalette(53);
	histo->Draw("COLZ");

	TPolyLine *roiframe = new TPolyLine(5);
	double x_1 = 2.0*double(topleft_x)/double(xPixels) - 1.0;
	double y_1 = 2.0*double(yPixels-topleft_y)/double(yPixels) - 1.0;
	double ww = 2.0*double(width)/double(xPixels);
	double hh = 2.0*double(height)/double(yPixels);
	roiframe->SetPoint(0,x_1,y_1);
	roiframe->SetPoint(1,x_1+ww,y_1);
	roiframe->SetPoint(2,x_1+ww,y_1-hh);
	roiframe->SetPoint(3,x_1,y_1-hh);
	roiframe->SetPoint(4,x_1,y_1);
	roiframe->SetLineColor(3);
	roiframe->SetLineWidth(3);
	roiframe->Draw();

//	std::cout << "(x_1,y_1) = (" << x_1 << ", " << y_1 << ")" << std::endl;

	
	// Draw close-up hist of the ROI region
	c1->cd(3);

//	TH2D *roi = new TH2D("roi","Region of Interest",width,x_1,x_1+width,height,y_1-height,y_1);
	double rounded_x_1 = round_off(x_1,3);
	double rounded_y_1 = round_off(y_1,3);
	double rounded_ww = round_off(ww,3);
	double rounded_hh = round_off(hh,3);
	TH2D *roi = new TH2D("roi","Region of Interest",width,rounded_x_1,rounded_x_1+rounded_ww,height,rounded_y_1-rounded_hh,rounded_y_1);
	for (int i=1; i<=xPixels; ++i){
		for (int j=1; j<=yPixels; ++j){
			double val = histo->GetBinContent(i,j);
			double x_c = 2.0*double(i)/double(xPixels)-1.0;
			double y_c = 2.0*double(j)/double(yPixels)-1.0;
			bool x_in = (x_c > x_1) && (x_c < x_1+ww);
			bool y_in = (y_c < y_1) && (y_c > y_1-hh);
			bool in_roi = x_in && y_in;
			if (in_roi){
				roi->Fill(x_c,y_c,val);
			}
		}
	}

	roi->Draw("COLZ");


	// Display integral of ROI histo
	c1->cd(4);

	double integ = roi->Integral();

	TLatex l;
	l.SetTextAlign(12);
	l.SetTextSize(0.05);
	l.DrawLatex(0.15,0.8,"Net Brightness in ROI");
	l.DrawLatex(0.2,0.7,Form("%g [a.u.]",integ));
	l.DrawLatex(0.15,0.6,"ROI Position");
	l.DrawLatex(0.2,0.5,"(topleft_x, topleft_y, width, height)");
	l.DrawLatex(0.2,0.4,Form("= (%d, %d, %d, %d)",topleft_x,topleft_y,width,height));

	c1->Update();
	c1->Modified();

	rootapp.Run();

	return 0;
}
