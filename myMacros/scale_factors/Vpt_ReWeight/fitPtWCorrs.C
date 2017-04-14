//
// Perform fits on the pT(W) distribution for backgrounds in CR's.
// used to correct for data/MC discrepancies in pT(W) distribution
// with full 2016 dataset.
//
// Author: Stephane Cooperstein
//

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooSimultaneous.h"
#include "RooCategory.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "TFile.h"
#include "TH1F.h"
#include "RooWorkspace.h"
#include "RooDataHist.h"
#include "RooPolynomial.h"
#include "RooHistPdf.h"
#include "RooProdPdf.h"
#include "RooChi2Var.h"
#include "RooMinuit.h"
#include <ostream>
#include <istream>
using namespace RooFit;
using namespace std;


void fitPtWCorrs() {
  
  using namespace RooFit ;

  float SF_TT   = 1.;
  float SF_Zj0b = 1.;
  float SF_Zj1b = 1.;
  float SF_Zj2b = 1.; 
  
  TFile *ifile_zlf = TFile::Open("Zlf_Vpt.root", "r");
  TH1F *hist_zlf_data = (TH1F*) ifile_zlf->Get("noData");
  TH1F *hist_zlf_tt   = (TH1F*) ifile_zlf->Get("ttbar");
  TH1F *hist_zlf_stop = (TH1F*) ifile_zlf->Get("ST_s");
  TH1F *hist_zlf_zj2b = (TH1F*) ifile_zlf->Get("Z2b");
  TH1F *hist_zlf_zj1b = (TH1F*) ifile_zlf->Get("Z1b");
  TH1F *hist_zlf_zj0b = (TH1F*) ifile_zlf->Get("Zudsg");
  TH1F *hist_zlf_vvlf = (TH1F*) ifile_zlf->Get("WZlight");
  TH1F *hist_zlf_vvhf = (TH1F*) ifile_zlf->Get("WZb");
  
  
  TFile *ifile_zhf = TFile::Open("Zhf_Vpt.root", "r");
  TH1F *hist_zhf_data = (TH1F*) ifile_zhf->Get("noData");
  TH1F *hist_zhf_tt   = (TH1F*) ifile_zhf->Get("ttbar");
  TH1F *hist_zhf_stop = (TH1F*) ifile_zhf->Get("ST_s");
  TH1F *hist_zhf_zj2b = (TH1F*) ifile_zhf->Get("Z2b");
  TH1F *hist_zhf_zj1b = (TH1F*) ifile_zhf->Get("Z1b");
  TH1F *hist_zhf_zj0b = (TH1F*) ifile_zhf->Get("Zudsg");
  TH1F *hist_zhf_vvlf = (TH1F*) ifile_zhf->Get("WZlight");
  TH1F *hist_zhf_vvhf = (TH1F*) ifile_zhf->Get("WZb");
  
  //hist_zhf_tt->Scale(SF_TT);
  //hist_zhfZmm_wj0b->Scale(SF_Wj0b);
  //hist_zhfZmm_wj1b->Scale(SF_Wj1b);
  //hist_zhfZmm_wj2b->Scale(SF_Wj2b);
  
  TH1F *hist_zlf_sub = (TH1F*) hist_zlf_data->Clone();
  hist_zlf_sub->Reset();
  hist_zlf_sub->Add(hist_zlf_zj2b);
  hist_zlf_sub->Add(hist_zlf_zj1b);
  hist_zlf_sub->Add(hist_zlf_tt);
  hist_zlf_sub->Add(hist_zlf_stop);
  hist_zlf_sub->Add(hist_zlf_vvhf);
  hist_zlf_sub->Add(hist_zlf_vvlf);
  
  TH1F *hist_zhf_sub = (TH1F*) hist_zhf_data->Clone();
  hist_zhf_sub->Reset();
  hist_zhf_sub->Add(hist_zhf_zj0b);
  hist_zhf_sub->Add(hist_zhf_tt);
  hist_zhf_sub->Add(hist_zhf_vvhf);
  hist_zhf_sub->Add(hist_zhf_vvlf);
  hist_zhf_sub->Add(hist_zhf_stop);
  
  TH1F *hist_zlf_zhf = (TH1F*) hist_zlf_zj2b->Clone();
  hist_zlf_zhf->Add(hist_zlf_zj1b);
  
  TH1F *hist_zhf_zhf = (TH1F*) hist_zhf_zj2b->Clone();
  hist_zhf_zhf->Add(hist_zhf_zj1b);
  
  
  // std::cout<<"Total data: "<<hist_tt_data->Integral()<<std::endl;;
  // std::cout<<"Total TT: "<<hist_tt_tt->Integral()<<std::endl;;
  // std::cout<<"Total non-TT: "<<hist_tt_sub->Integral()<<std::endl;;
  
  //std::cout<<"Total data: "<<hist_zlf_data->Integral()<<std::endl;;
  //std::cout<<"Total ZLF: "<<hist_zlf_zj0b->Integral()<<std::endl;;
  //std::cout<<"Total non-ZLF: "<<hist_zlf_sub->Integral()<<std::endl;;
  
  //std::cout<<"Total data: "<<hist_zhf_data->Integral()<<std::endl;;
  //std::cout<<"Total ZHF: "<<hist_zhf_zhf->Integral()<<std::endl;;
  //std::cout<<"Total non-ZHF: "<<hist_zhf_sub->Integral()<<std::endl;;
  
  //hist_tt_data->Sumw2();
  hist_zlf_data->Sumw2();
  hist_zhf_data->Sumw2();
  
  //hist_ttZmm_data->Add(hist_ttZmm_sub, -1.0);
  //hist_ttZmm_tt->Add(hist_ttZmm_sub);
  //hist_zlfZmm_zlf->Add(hist_zlfZmm_sub);
  
  //std::cout<<"Total data after subtraction: "<<hist_ttZmm_data->Integral()<<std::endl;;
  
  //hist_ttZmm_data->Divide(hist_ttZmm_tt);
  
  RooWorkspace w("ws");
  
  RooRealVar vpt("vpt","vpt",50,400);
  
  // RooDataHist data_tt("data_tt","data_tt",vpt,hist_tt_data);
  // RooDataHist tt_tt("tt_tt","tt_tt",vpt,hist_tt_tt);
  // RooDataHist zj0b_tt("zj0b_tt","zj0b_tt",vpt,hist_tt_zj0b);
  // RooDataHist zj1b_tt("zj1b_tt","zj1b_tt",vpt,hist_tt_zj1b);
  // RooDataHist zj2b_tt("zj2b_tt","zj2b_tt",vpt,hist_tt_zj2b);
  // RooDataHist stop_tt("stop_tt","stop_tt",vpt,hist_tt_stop);
  // RooDataHist stop_tt("vvlf_tt","vvlf_tt",vpt,hist_tt_vvhf);
  // RooDataHist stop_tt("vvhf_tt","vvhf_tt",vpt,hist_tt_vvlf);
  // RooDataHist zhf_tt("zhf_tt","zhf_tt",vpt,hist_tt_zhf);
  
  RooDataHist data_zlf("data_zlf","data_zlf",vpt,hist_zlf_data);
  RooDataHist tt_zlf("tt_zlf","tt_zlf",vpt,hist_zlf_tt);
  RooDataHist zj0b_zlf("zj0b_zlf","zj0b_zlf",vpt,hist_zlf_zj0b);
  RooDataHist zj1b_zlf("zj1b_zlf","zj1b_zlf",vpt,hist_zlf_zj1b);
  RooDataHist zj2b_zlf("zj2b_zlf","zj2b_zlf",vpt,hist_zlf_zj2b);
  RooDataHist stop_zlf("stop_zlf","stop_zlf",vpt,hist_zlf_stop);
  RooDataHist vvlf_zlf("vvlf_zlf","vvlf_zlf",vpt,hist_zlf_vvlf);
  RooDataHist vvhf_zlf("vvhf_zlf","vvhf_zlf",vpt,hist_zlf_vvhf);
  
  RooDataHist zhf_zlf("zhf_zlf","zhf_zlf",vpt,hist_zlf_zhf);
  
  RooDataHist data_zhf("data_zhf","data_zhf",vpt,hist_zhf_data);
  RooDataHist tt_zhf("tt_zhf","tt_zhf",vpt,hist_zhf_tt);
  RooDataHist zj0b_zhf("zj0b_zhf","zj0b_zhf",vpt,hist_zhf_zj0b);
  RooDataHist zj1b_zhf("zj1b_zhf","zj1b_zhf",vpt,hist_zhf_zj1b);
  RooDataHist zj2b_zhf("zj2b_zhf","zj2b_zhf",vpt,hist_zhf_zj2b);
  RooDataHist stop_zhf("stop_zhf","stop_zhf",vpt,hist_zhf_stop);
  RooDataHist vvlf_zhf("vvlf_zhf","vvlf_zhf",vpt,hist_zhf_vvlf);
  RooDataHist vvhf_zhf("vvhf_zhf","vvhf_zhf",vpt,hist_zhf_vvhf);
  
  RooDataHist zhf_zhf("zhf_zhf","zhf_zhf",vpt,hist_zhf_zhf);
  
  
  RooRealVar a0_zlf("a0_zlf","a0_zlf",-0.00075,-0.01,0.0);
  RooRealVar a0_zhf("a0_zhf","a0_zhf",-0.00075,-0.01,0.0);
  RooRealVar a1_zlf("a1_zlf","a1_zlf",0.0002,-10000,10000);
  RooRealVar a1_zhf("a1_zhf","a1_zhf",0.0002,-10000,10000);
  
  RooArgList arglist_zlf(a0_zlf);
  //RooArgList arglist_zlf(a0_zlf,a1_zlf);
  RooArgList arglist_zhf(a0_zhf);
  
  //RooPolynomial poly_tt("poly_tt","poly_tt",vpt,arglist_tt);
  RooPolynomial poly_zlf("poly_zlf","poly_zlf",vpt,arglist_zlf);
  RooPolynomial poly_zhf("poly_zhf","poly_zhf",vpt,arglist_zhf);

  

  RooHistPdf ttpdf_zlf("ttpdf_zlf","ttpdf_zlf",vpt,tt_zlf);
  RooProdPdf model_tt_zlf("model_tt_zlf","model_tt_zlf",ttpdf_zlf,poly_tt);
  RooHistPdf zlfpdf_zlf("zlfpdf_zlf","zlfpdf_zlf",vpt,zj0b_zlf);
  RooProdPdf model_zlf_zlf("model_zlf_zlf","model_zlf_zlf",zlfpdf_zlf,poly_zlf);
  RooHistPdf zhfpdf_zlf("zhfpdf_zlf","zhfpdf_zlf",vpt,zhf_zlf);
  RooProdPdf model_zhf_zlf("model_zhf_zlf","model_zhf_zlf",zhfpdf_zlf,poly_zhf);
  RooRealVar zlffrac_zlf("zlffrac_zlf","zlffrac_zlf",(hist_zlf_zj0b->Integral()/(hist_zlf_zj0b->Integral()+hist_zlf_sub->Integral())));
  RooRealVar ttfrac_zlf("ttfrac_zlf","ttfrac_zlf",(hist_zlf_tt->Integral()/(hist_zlf_zj0b->Integral()+hist_zlf_sub->Integral())));
  RooAddPdf model_zlf("model_zlf","model_zlf",RooArgList(model_zlf_zlf,model_zhf_zlf),RooArgList(zlffrac_zlf, ttfrac_zlf));
  
  RooHistPdf ttpdf_zhf("ttpdf_zhf","ttpdf_zhf",vpt,tt_zhf);
  RooProdPdf model_tt_zhf("model_tt_zhf","model_tt_zhf",ttpdf_zhf,poly_tt);
  RooHistPdf zlfpdf_zhf("zlfpdf_zhf","zlfpdf_zhf",vpt,zj0b_zhf);
  RooProdPdf model_zlf_zhf("model_zlf_zhf","model_zlf_zhf",zlfpdf_zhf,poly_zlf);
  RooHistPdf zhfpdf_zhf("zhfpdf_zhf","zhfpdf_zhf",vpt,zhf_zhf);
  RooProdPdf model_zhf_zhf("model_zhf_zhf","model_zhf_zhf",zhfpdf_zhf,poly_zhf);
  RooRealVar zlffrac_zhf("zlffrac_zhf","zlffrac_zhf",(hist_zhf_zj0b->Integral()/(hist_zhf_zhf->Integral()+hist_zhf_sub->Integral())));
  RooRealVar ttfrac_zhf("ttfrac_zhf","ttfrac_zhf",(hist_zhf_tt->Integral()/(hist_zhf_zhf->Integral()+hist_zhf_sub->Integral())));
  RooAddPdf model_zhf("model_zhf","model_zhf",RooArgList(model_zlf_zhf,model_zhf_zhf),RooArgList(zlffrac_zhf, ttfrac_zhf));
    
    
  RooCategory sample("sample","sample") ;
  sample.defineType("zlf");
  sample.defineType("zhf");
  
  RooDataSet *data2 = model_zlf.generate(RooArgSet(vpt),1000); 
  RooDataSet *data3 = model_zhf.generate(RooArgSet(vpt),1000); 
  
  RooDataSet combData("combData","combined data",RooArgSet(vpt,sample));
  
  //RooRealVar y("y","y",0,100000);
  // for (int i=1; i<hist_tt_data->GetNbinsX()+1; i++) {
  //     vpt = hist_tt_data->GetBinLowEdge(i) + 0.5*hist_tt_data->GetBinWidth(i);
  //     float val = hist_tt_data->GetBinContent(i);
  //     sample.setLabel("tt");
  // //    combData.add(RooArgSet(vpt,sample),val);
  //     cout<<i<<":, "<<vpt<<", "<<val<<std::endl;
  //     for (int j=0; j<val; j++) {
  //         combData.add(RooArgSet(vpt,sample));
  //     }
  // }
  
  for (int i=1; i<hist_zlf_data->GetNbinsX()+1; i++) {
    vpt = hist_zlf_data->GetBinLowEdge(i) + 0.5*hist_zlf_data->GetBinWidth(i);
    float val = hist_zlf_data->GetBinContent(i);
    sample.setLabel("zlf");
    //combData.add(RooArgSet(vpt,sample));
    //combData.add(RooArgSet(vpt,sample),val);
    //std::cout<<i<<":, "<<vpt<<", "<<val<<std::endl;
    for (int j=0; j<val; j++) {
      combData.add(RooArgSet(vpt,sample));
    }
  }
  
  for (int i=1; i<hist_zhf_data->GetNbinsX()+1; i++) {
    vpt = hist_zhf_data->GetBinLowEdge(i) + 0.5*hist_zhf_data->GetBinWidth(i);
    float val = hist_zhf_data->GetBinContent(i);
    sample.setLabel("zhf");
    //combData.add(RooArgSet(vpt,sample));
    //combData.add(RooArgSet(vpt,sample),val);
    //std::cout<<i<<":, "<<vpt<<", "<<val<<std::endl;
    for (int j=0; j<val; j++) {
      combData.add(RooArgSet(vpt,sample));
    }
  }
  


RooSimultaneous simPdf("simPdf","simultaneous pdf",sample) ;

//simPdf.addPdf(model_tt,"tt") ;
simPdf.addPdf(model_zlf,"zlf"); 
simPdf.addPdf(model_zhf,"zhf"); 

RooDataHist dh("dh","dh",*combData.get(),combData) ; 
RooChi2Var chi2("chi2","chi2",simPdf,dh);
RooMinuit m2(chi2);
m2.migrad();
//m2.minos();

//std::cout<<"simPDF.canBeExtend() = "<<simPdf.canBeExtended()<<std::endl;
//simPdf.chi2FitTo(combData) ;
//simPdf.fitTo(combData) ;
 
//RooChi2Var chi2_var_A("","", model_tt, *data_tt);
//RooMinuit m2_var_A(chi2_var_A);
//m2_var_A.migrad();

//poly_tt.fitTo(data);
//poly_tt.fitTo(data,SumW2Error(kFALSE));

//RooPlot* frame = vpt.frame();
//data_tt.plotOn(frame);
//poly_tt.plotOn(frame);
//poly_zlf.plotOn(frame,LineColor(kGreen));
//model_tt.plotOn(frame,LineColor(kRed));
//model_tt_tt.plotOn(frame,LineColor(kBlue));
//model_zlf_tt.plotOn(frame,LineColor(kGreen));

//combData.plotOn(frame,Cut("sample==sample::tt")) ;
//simPdf.plotOn(frame,Slice(sample,"tt"),ProjWData(sample,combData)) ;
//simPdf.plotOn(frame,Slice(sample,"tt"),Components("model_ttWm"),ProjWData(sample,combData),LineStyle(kDashed)) ;

// RooPlot* frame1 = vpt.frame(Bins(60),Title("TT CR")) ;
// combData.plotOn(frame1,Cut("sample==sample::tt")) ;
// simPdf.plotOn(frame1,Slice(sample,"tt"),ProjWData(sample,combData)) ;
// simPdf.plotOn(frame1,Slice(sample,"tt"),Components("model_tt_tt"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kBlue)) ;
// simPdf.plotOn(frame1,Slice(sample,"tt"),Components("model_zlf_tt"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kGreen)) ;
// simPdf.plotOn(frame1,Slice(sample,"tt"),Components("model_zhf_tt"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kViolet)) ;
// simPdf.plotOn(frame1,Slice(sample,"tt"),Components("model_tt"),ProjWData(sample,combData),LineStyle(kDashed)) ;

RooPlot* frame2 = vpt.frame(Bins(60),Title("ZLF CR")) ;
combData.plotOn(frame2,Cut("sample==sample::zlf")) ;
simPdf.plotOn(frame2,Slice(sample,"zlf"),ProjWData(sample,combData)) ;
simPdf.plotOn(frame2,Slice(sample,"zlf"),Components("model_tt_zlf"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kBlue)) ;
simPdf.plotOn(frame2,Slice(sample,"zlf"),Components("model_zlf_zlf"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kGreen)) ;
simPdf.plotOn(frame2,Slice(sample,"zlf"),Components("model_zhf_zlf"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kViolet)) ;
simPdf.plotOn(frame2,Slice(sample,"zlf"),Components("model_zlf"),ProjWData(sample,combData),LineStyle(kDashed));

RooPlot* frame3 = vpt.frame(Bins(60),Title("ZHF CR")) ;
combData.plotOn(frame3,Cut("sample==sample::zhf")) ;
simPdf.plotOn(frame3,Slice(sample,"zhf"),ProjWData(sample,combData)) ;
simPdf.plotOn(frame3,Slice(sample,"zhf"),Components("model_tt_zhf"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kBlue)) ;
simPdf.plotOn(frame3,Slice(sample,"zhf"),Components("model_zlf_zhf"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kGreen)) ;
simPdf.plotOn(frame3,Slice(sample,"zhf"),Components("model_zhf_zhf"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kViolet)) ;
simPdf.plotOn(frame3,Slice(sample,"zhf"),Components("model_zhf"),ProjWData(sample,combData),LineStyle(kDashed));

TCanvas* c = new TCanvas("rf501_simultaneouspdf","rf403_simultaneouspdf",1600,800) ;
c->Divide(2) ;
c->cd(1) ; gPad->SetLeftMargin(0.15) ; frame2->GetYaxis()->SetTitleOffset(1.4) ; frame2->Draw() ;
c->cd(2) ; gPad->SetLeftMargin(0.15) ; frame3->GetYaxis()->SetTitleOffset(1.4) ; frame3->Draw() ;

//std::cout<<"TT chi2/ndof = "<<frame1.chiSquare()<<std::endl;;
//std::cout<<"ZHF chi2/ndof = "<<frame3->chiSquare()<<std::endl;;
//std::cout<<"ZLF chi2/ndof = "<<frame2->chiSquare()<<std::endl;;

frame3->Print();
//ttpdf.plotOn(frame);
//nb.plotOn(frame);
//expo.plotOn(frame);
//bkgmodel.plotOn(frame);
//CBall.plotOn(frame);
//std::cout<<"chi2/ndof = "<<frame.chiSquare()<<std::endl;;
//frame.Draw();

//RooPlot* frame2 = vpt.frame();
//data_zlf.plotOn(frame2);
//poly_tt.plotOn(frame2);
//poly_zlf.plotOn(frame2,LineColor(kGreen));
//model_zlf.plotOn(frame2,LineColor(kRed));
//std::cout<<"chi2/ndof = "<<frame2.chiSquare()<<std::endl;;
//frame2.Draw();

//std::cout<<hist_zhf_data->Integral()<<std::endl;

//std::cout<<ttfrac_tt->getVal()<<std::endl;;

//std::cout<<(1-zlffrac_zhf.getVal()-ttfrac_zhf.getVal())<<std::endl;;

//std::cout<<zlffrac_zlf.getVal()<<std::endl;;

//std::cout<<(hist_zlf_zj0b->Integral()/(hist_zlf_zj0b->Integral()+hist_zlf_sub->Integral()))<<std::endl;;

}
