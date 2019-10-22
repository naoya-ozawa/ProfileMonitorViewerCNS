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

	const char* samplecsv = "./sample-images/Image__2019-10-02__17-35-26.csv";
	const int pix = 550;
	const int repix = 65;
	double imgtxt[pix][pix];

	TCanvas *c1 = new TCanvas();

	TH2D *histimage = new TH2D("histimage","CCD Image",pix,0.,550.,pix,0.,550.);
	histimage->GetXaxis()->SetTitle("X");
	histimage->GetYaxis()->SetTitle("Y");

	int valcount = 0;

	ifstream matrix( samplecsv );
	string line;
	int i = 0;
	int j = 0;
	while ( getline(matrix,line) ){
		istringstream linestream(line);
		string item;
		while ( getline(linestream,item,',') ){
			imgtxt[i][j] = stod(item);
//			cout << imgtxt[i][j] << " ";
			if (imgtxt[i][j] > 0){
				++valcount;
				histimage->Fill(i,pix-j-1,imgtxt[i][j]);
			}
			++i;
		}
//		cout << endl;
		i = 0;
		++j;
	}

//	cout << "There are " << valcount << " non-zero pixels" << endl;

	histimage->Draw("COLZ");

	// Draw a circle indicating the BPM
	const int PLpts = 1000;
	const double R_MCP = 12.5*(550./30.);
	TPolyLine *MCP_circ = new TPolyLine(PLpts);
	for (int k=0; k<PLpts; ++k){
		double X = R_MCP*TMath::Cos(2.*double(k)*TMath::Pi()/double(PLpts-1)) + (550./2.);
		double Y = R_MCP*TMath::Sin(2.*double(k)*TMath::Pi()/double(PLpts-1)) + (550./2.);
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
