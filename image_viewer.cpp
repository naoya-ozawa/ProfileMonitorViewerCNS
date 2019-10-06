#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<TMath.h>
#include<TH2D.h>
#include<TCanvas.h>
#include<TPolyLine.h>
#include<TRint.h>

using namespace std;

int main (int argc, char** argv){

	TRint rootapp("app",&argc,argv);

	const char* sampletxt = "./sample-images/Image__2019-10-02__17-35-26.txt";
	const int pix = 550;
	const int repix = 65;
	double imgtxt[pix][pix];

	TCanvas *c1 = new TCanvas();

	TH2D *histimage = new TH2D("histimage","Rebinned CCD Image",pix,-15.,15.,pix,-15.,15.);
	histimage->GetXaxis()->SetTitle("X");
	histimage->GetYaxis()->SetTitle("Y");

	int valcount = 0;

	ifstream matrix( sampletxt );
	string line;
	int i = 0;
	int j = 0;
	while ( getline(matrix,line) ){
		istringstream linestream(line);
		string item;
		while ( getline(linestream,item) ){
			imgtxt[i][j] = stod(item);
			if (imgtxt[i][j] > 0){
				++valcount;
				histimage->Fill(i,j,imgtxt[i][j]);
			}
			++i;
		}
		++j;
	}

	cout << "There are " << valcount << " non-zero pixels" << endl;

	histimage->Draw("COLZ");

	// Draw a circle indicating the BPM
	const int PLpts = 1000;
	const double R_MCP = 12.5;
	TPolyLine *MCP_circ = new TPolyLine(PLpts);
	for (int k=0; k<PLpts; ++k){
		double X = R_MCP*TMath::Cos(2.*double(k)*TMath::Pi()/double(PLpts-1));
		double Y = R_MCP*TMath::Sin(2.*double(k)*TMath::Pi()/double(PLpts-1));
		MCP_circ->SetPoint(k,X,Y);
	}
	MCP_circ->SetLineWidth(2);
	MCP_circ->SetLineColor(2);
	MCP_circ->Draw();

	c1->Update();
	c1->Modified();

	rootapp.Run();

	return 0;
}
