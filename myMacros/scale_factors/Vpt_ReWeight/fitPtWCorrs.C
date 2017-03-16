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
using namespace RooFit ;


void fitPtWCorrs() {

using namespace RooFit ;

float SF_TT   = 1.;
float SF_Wj0b = 1.;
float SF_Wj1b = 1.;
float SF_Wj2b = 1.; 

TFile *ifile_ttZmm = TFile::Open("hists_ttZmm_to400.root", "r");
TH1F *hist_ttZmm_data = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_data_obs");
TH1F *hist_ttZmm_tt   = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_TT");
TH1F *hist_ttZmm_stop = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_s_Top");
TH1F *hist_ttZmm_zj2b = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_Zj2b");
TH1F *hist_ttZmm_zj1b = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_Zj1b");
TH1F *hist_ttZmm_zj0b = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_Zj0b");
TH1F *hist_ttZmm_vvlf = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_VVHF");
TH1F *hist_ttZmm_vvhf = (TH1F*) ifile_ttZmm->Get("BDT_ttZmm_VVHLF");

TFile *ifile_zlfZmm = TFile::Open("hists_zlfZmm_to400.root", "r");
TH1F *hist_zlfZmm_data = (TH1F*) ifile_zlfZmm->Get("BDT_zlfZmm_data_obs");
TH1F *hist_zlfZmm_tt   = (TH1F*) ifile_zlfZmm->Get("BDT_zlfZmm_TT");
TH1F *hist_zlfZmm_stop = (TH1F*) ifile_zlfZmm->Get("BDT_zlfZmm_s_Top");
TH1F *hist_zlfZmm_zj2b = (TH1F*) ifile_zlfZmm->Get("BDT_zlfZmm_Zj2b");
TH1F *hist_zlfZmm_zj1b = (TH1F*) ifile_zlfZmm->Get("BDT_zlfZmm_Zj1b");
TH1F *hist_zlfZmm_zj0b = (TH1F*) ifile_zlfZmm->Get("BDT_zlfZmm_Zj0b");
TH1F *hist_zlfZmm_vvlf = (TH1F*) ifile_ttZmm->Get("BDT_zlfZmm_VVHF");
TH1F *hist_zlfZmm_vvhf = (TH1F*) ifile_ttZmm->Get("BDT_zlfZmm_VVHLF");


TFile *ifile_zhfZmm = TFile::Open("hists_zhfZmm_to400.root", "r");
TH1F *hist_zhfZmm_data = (TH1F*) ifile_zhfZmm->Get("BDT_zhfZmm_data_obs");
TH1F *hist_zhfZmm_tt = (TH1F*) ifile_zhfZmm->Get("BDT_zhfZmm_TT");
TH1F *hist_zhfZmm_stop = (TH1F*) ifile_zhfZmm->Get("BDT_zhfZmm_s_Top");
TH1F *hist_zhfZmm_zj2b = (TH1F*) ifile_zhfZmm->Get("BDT_zhfZmm_Zj2b");
TH1F *hist_zhfZmm_zj1b = (TH1F*) ifile_zhfZmm->Get("BDT_zhfZmm_Zj1b");
TH1F *hist_zhfZmm_zj0b = (TH1F*) ifile_zhfZmm->Get("BDT_zhfZmm_Zj0b");
TH1F *hist_zhfZmm_vvlf = (TH1F*) ifile_ttZmm->Get("BDT_zhfZmm_VVHF");
TH1F *hist_zhfZmm_vvhf = (TH1F*) ifile_ttZmm->Get("BDT_zhfZmm_VVHLF");

// hist_ttZmm_tt->Scale(SF_TT);
// hist_ttZmm_wj0b->Scale(SF_Wj0b);
// hist_ttZmm_wj1b->Scale(SF_Wj1b);
// hist_ttZmm_wj2b->Scale(SF_Wj2b);

// hist_zlfZmm_tt->Scale(SF_TT);
// hist_zlfZmm_wj0b->Scale(SF_Wj0b);
// hist_zlfZmm_wj1b->Scale(SF_Wj1b);
// hist_zlfZmm_wj2b->Scale(SF_Wj2b);

// hist_zhfZmm_tt->Scale(SF_TT);
// hist_zhfZmm_wj0b->Scale(SF_Wj0b);
// hist_zhfZmm_wj1b->Scale(SF_Wj1b);
// hist_zhfZmm_wj2b->Scale(SF_Wj2b);

TH1F *hist_ttZmm_sub = hist_ttZmm_data->Clone();
hist_ttZmm_sub->Reset();
hist_ttZmm_sub->Add(hist_ttZmm_zj2b);
hist_ttZmm_sub->Add(hist_ttZmm_zj1b);
hist_ttZmm_sub->Add(hist_ttZmm_zj0b);
hist_ttZmm_sub->Add(hist_ttZmm_stop);
hist_ttZmm_sub->Add(hist_ttZmm_vvhf);
hist_ttZmm_sub->Add(hist_ttZmm_vvlf);

TH1F *hist_zlfZmm_sub = hist_zlfZmm_data->Clone();
hist_zlfZmm_sub->Reset();
hist_zlfZmm_sub->Add(hist_zlfZmm_zj2b);
hist_zlfZmm_sub->Add(hist_zlfZmm_zj1b);
hist_zlfZmm_sub->Add(hist_zlfZmm_tt);
hist_zlfZmm_sub->Add(hist_zlfZmm_stop);
hist_zlfZmm_sub->Add(hist_zlfZmm_vvhf);
hist_zlfZmm_sub->Add(hist_zlfZmm_vvlf);

TH1F *hist_zhfZmm_sub = hist_zhfZmm_data->Clone();
hist_zhfZmm_sub->Reset();
hist_zhfZmm_sub->Add(hist_zhfZmm_zj0b);
hist_zhfZmm_sub->Add(hist_zhfZmm_tt);
hist_zhfZmm_sub->Add(hist_zhfZmm_vvhf);
hist_zhfZmm_sub->Add(hist_zhfZmm_vvlf);
 hist_zhfZmm_sub->Add(hist_zhfZmm_stop);

TH1F *hist_zlfZmm_zhf = hist_zlfZmm_zj2b->Clone();
hist_zlfZmm_zhf->Add(hist_zlfZmm_zj1b);

TH1F *hist_ttZmm_zhf = hist_ttZmm_zj2b->Clone();
hist_ttZmm_zhf->Add(hist_ttZmm_zj1b);

TH1F *hist_zhfZmm_zhf = hist_zhfZmm_zj2b->Clone();
hist_zhfZmm_zhf->Add(hist_zhfZmm_zj1b);


std::cout<<"Total data: "<<hist_ttZmm_data->Integral()<<std::endl;;
std::cout<<"Total TT: "<<hist_ttZmm_tt->Integral()<<std::endl;;
std::cout<<"Total non-TT: "<<hist_ttZmm_sub->Integral()<<std::endl;;

std::cout<<"Total data: "<<hist_zlfZmm_data->Integral()<<std::endl;;
std::cout<<"Total ZLF: "<<hist_zlfZmm_zj0b->Integral()<<std::endl;;
std::cout<<"Total non-ZLF: "<<hist_zlfZmm_sub->Integral()<<std::endl;;

std::cout<<"Total data: "<<hist_zhfZmm_data->Integral()<<std::endl;;
std::cout<<"Total ZHF: "<<hist_zhfZmm_zhf->Integral()<<std::endl;;
std::cout<<"Total non-ZHF: "<<hist_zhfZmm_sub->Integral()<<std::endl;;

hist_ttZmm_data->Sumw2();
hist_zlfZmm_data->Sumw2();
hist_zhfZmm_data->Sumw2();

//hist_ttZmm_data->Add(hist_ttZmm_sub, -1.0);
//hist_ttZmm_tt->Add(hist_ttZmm_sub);
//hist_zlfZmm_zlf->Add(hist_zlfZmm_sub);

//std::cout<<"Total data after subtraction: "<<hist_ttZmm_data->Integral()<<std::endl;;

//hist_ttZmm_data->Divide(hist_ttZmm_tt);

RooWorkspace w("ws");

RooRealVar vpt("vpt","vpt",50,400);

RooDataHist data_ttZmm("data_ttZmm","data_ttZmm",vpt,hist_ttZmm_data);
RooDataHist tt_ttZmm("tt_ttZmm","tt_ttZmm",vpt,hist_ttZmm_tt);
RooDataHist zj0b_ttZmm("zj0b_ttZmm","zj0b_ttZmm",vpt,hist_ttZmm_zj0b);
RooDataHist zj1b_ttZmm("zj1b_ttZmm","zj1b_ttZmm",vpt,hist_ttZmm_zj1b);
RooDataHist zj2b_ttZmm("zj2b_ttZmm","zj2b_ttZmm",vpt,hist_ttZmm_zj2b);
RooDataHist stop_ttZmm("stop_ttZmm","stop_ttZmm",vpt,hist_ttZmm_stop);
RooDataHist stop_ttZmm("vvlf_ttZmm","vvlf_ttZmm",vpt,hist_ttZmm_vvhf);
RooDataHist stop_ttZmm("vvhf_ttZmm","vvhf_ttZmm",vpt,hist_ttZmm_vvlf);

RooDataHist zhf_ttZmm("zhf_ttZmm","zhf_ttZmm",vpt,hist_ttZmm_zhf);

RooDataHist data_zlfZmm("data_zlfZmm","data_zlfZmm",vpt,hist_zlfZmm_data);
RooDataHist tt_zlfZmm("tt_zlfZmm","tt_zlfZmm",vpt,hist_zlfZmm_tt);
RooDataHist zj0b_zlfZmm("zj0b_zlfZmm","zj0b_zlfZmm",vpt,hist_zlfZmm_zj0b);
RooDataHist zj1b_zlfZmm("zj1b_zlfZmm","zj1b_zlfZmm",vpt,hist_zlfZmm_zj1b);
RooDataHist zj2b_zlfZmm("zj2b_zlfZmm","zj2b_zlfZmm",vpt,hist_zlfZmm_zj2b);
RooDataHist stop_zlfZmm("stop_zlfZmm","stop_zlfZmm",vpt,hist_zlfZmm_stop);
RooDataHist vvlf_zlfZmm("vvlf_zlfZmm","vvlf_zlfZmm",vpt,hist_zlfZmm_vvlf);
RooDataHist vvhf_zlfZmm("vvhf_zlfZmm","vvhf_zlfZmm",vpt,hist_zlfZmm_vvhf);

RooDataHist zhf_zlfZmm("zhf_zlfZmm","zhf_zlfZmm",vpt,hist_zlfZmm_zhf);

RooDataHist data_zhfZmm("data_zhfZmm","data_zhfZmm",vpt,hist_zhfZmm_data);
RooDataHist tt_zhfZmm("tt_zhfZmm","tt_zhfZmm",vpt,hist_zhfZmm_tt);
RooDataHist zj0b_zhfZmm("zj0b_zhfZmm","zj0b_zhfZmm",vpt,hist_zhfZmm_zj0b);
RooDataHist zj1b_zhfZmm("zj1b_zhfZmm","zj1b_zhfZmm",vpt,hist_zhfZmm_zj1b);
RooDataHist zj2b_zhfZmm("zj2b_zhfZmm","zj2b_zhfZmm",vpt,hist_zhfZmm_zj2b);
RooDataHist stop_zhfZmm("stop_zhfZmm","stop_zhfZmm",vpt,hist_zhfZmm_stop);
RooDataHist vvlf_zhfZmm("vvlf_zhfZmm","vvlf_zhfZmm",vpt,hist_zhfZmm_vvlf);
RooDataHist vvhf_zhfZmm("vvhf_zhfZmm","vvhf_zhfZmm",vpt,hist_zhfZmm_vvhf);

RooDataHist zhf_zhfZmm("zhf_zhfZmm","zhf_zhfZmm",vpt,hist_zhfZmm_zhf);

//RooRealVar a0_tt("a0_tt","a0_tt",0.);
//RooRealVar a0_zlf("a0_zlf","a0_zlf",0.);
//RooRealVar a0_zhf("a0_zhf","a0_zhf",0.);
RooRealVar a0_tt("a0_tt","a0_tt",-0.00086,-0.01,0.);
RooRealVar a0_zlf("a0_zlf","a0_zlf",-0.00075,-0.01,0.0);
RooRealVar a0_zhf("a0_zhf","a0_zhf",-0.00075,-0.01,0.0);
//RooRealVar a0_tt("a0_tt","a0_tt",-0.00001,-0.01,0.01);
//RooRealVar a1_tt("a1_tt","a1_tt",-0.00001,-0.01,0.01);
//RooRealVar a0_zlf("a0_zlf","a0_zlf",-0.0007,-0.01,0.01);
RooRealVar a1_zlf("a1_zlf","a1_zlf",0.0002,-10000,10000);
//RooRealVar a0_zhf("a0_zhf","a0_zhf",-0.009,-10000,10000);
RooRealVar a1_zhf("a1_zhf","a1_zhf",0.0002,-10000,10000);

RooArgList arglist_tt(a0_tt);
//RooArgList arglist_tt(a0_tt,a1_tt);
RooArgList arglist_zlf(a0_zlf);
//RooArgList arglist_zlf(a0_zlf,a1_zlf);
RooArgList arglist_zhf(a0_zhf);
//RooArgList arglist(a0,a1,a2,a3,a4,a5,a6,a7,a8);
//arglist.add(a9);
//arglist.add(a10);
//arglist.add(a11);
//arglist.add(a12);
//arglist.add(a13);
RooPolynomial poly_tt("poly_tt","poly_tt",vpt,arglist_tt);
RooPolynomial poly_zlf("poly_zlf","poly_zlf",vpt,arglist_zlf);
RooPolynomial poly_zhf("poly_zhf","poly_zhf",vpt,arglist_zhf);


RooHistPdf ttpdf_ttZmm("ttpdf_ttZmm","ttpdf_ttZmm",vpt,tt_ttZmm);
RooProdPdf model_tt_ttZmm("model_tt_ttZmm","model_tt_ttZmm",ttpdf_ttZmm,poly_tt);
RooHistPdf zlfpdf_ttZmm("zlfpdf_ttZmm","zlfpdf_ttZmm",vpt,zj0b_ttZmm);
RooProdPdf model_zlf_ttZmm("model_zlf_ttZmm","model_zlf_ttZmm",zlfpdf_ttZmm,poly_zlf);
RooHistPdf zhfpdf_ttZmm("zhfpdf_ttZmm","zhfpdf_ttZmm",vpt,zhf_ttZmm);
RooProdPdf model_zhf_ttZmm("model_zhf_ttZmm","model_zhf_ttZmm",zhfpdf_ttZmm,poly_zhf);
RooRealVar ttfrac_ttZmm("ttfrac_ttZmm","ttfrac_ttZmm",(hist_ttZmm_tt->Integral()/(hist_ttZmm_tt->Integral()+hist_ttZmm_sub->Integral())));
RooRealVar zlffrac_ttZmm("zlffrac_ttZmm","zlffrac_ttZmm",(hist_ttZmm_zj0b->Integral()/(hist_ttZmm_tt->Integral()+hist_ttZmm_sub->Integral())));
//RooAddPdf model_ttZmm("model_ttZmm","model_ttZmm",RooArgList(model_zlf_ttZmm,model_tt_ttZmm),ttfrac_ttZmm);
RooAddPdf model_ttZmm("model_ttZmm","model_ttZmm",RooArgList(model_tt_ttZmm,model_zlf_ttZmm,model_zhf_ttZmm),RooArgList(ttfrac_ttZmm,zlffrac_ttZmm));

RooHistPdf ttpdf_zlfZmm("ttpdf_zlfZmm","ttpdf_zlfZmm",vpt,tt_zlfZmm);
RooProdPdf model_tt_zlfZmm("model_tt_zlfZmm","model_tt_zlfZmm",ttpdf_zlfZmm,poly_tt);
RooHistPdf zlfpdf_zlfZmm("zlfpdf_zlfZmm","zlfpdf_zlfZmm",vpt,zj0b_zlfZmm);
RooProdPdf model_zlf_zlfZmm("model_zlf_zlfZmm","model_zlf_zlfZmm",zlfpdf_zlfZmm,poly_zlf);
RooHistPdf zhfpdf_zlfZmm("zhfpdf_zlfZmm","zhfpdf_zlfZmm",vpt,zhf_zlfZmm);
RooProdPdf model_zhf_zlfZmm("model_zhf_zlfZmm","model_zhf_zlfZmm",zhfpdf_zlfZmm,poly_zhf);
RooRealVar zlffrac_zlfZmm("zlffrac_zlfZmm","zlffrac_zlfZmm",(hist_zlfZmm_zj0b->Integral()/(hist_zlfZmm_zj0b->Integral()+hist_zlfZmm_sub->Integral())));
RooRealVar ttfrac_zlfZmm("ttfrac_zlfZmm","ttfrac_zlfZmm",(hist_zlfZmm_tt->Integral()/(hist_zlfZmm_zj0b->Integral()+hist_zlfZmm_sub->Integral())));
//RooAddPdf model_zlfZmm("model_zlfZmm","model_zlfZmm",RooArgList(model_zlf_zlfZmm,model_tt_zlfZmm),zlffrac_zlfZmm);
RooAddPdf model_zlfZmm("model_zlfZmm","model_zlfZmm",RooArgList(model_zlf_zlfZmm,model_tt_zlfZmm,model_zhf_zlfZmm),RooArgList(zlffrac_zlfZmm,ttfrac_zlfZmm));

RooHistPdf ttpdf_zhfZmm("ttpdf_zhfZmm","ttpdf_zhfZmm",vpt,tt_zhfZmm);
RooProdPdf model_tt_zhfZmm("model_tt_zhfZmm","model_tt_zhfZmm",ttpdf_zhfZmm,poly_tt);
RooHistPdf zlfpdf_zhfZmm("zlfpdf_zhfZmm","zlfpdf_zhfZmm",vpt,zj0b_zhfZmm);
RooProdPdf model_zlf_zhfZmm("model_zlf_zhfZmm","model_zlf_zhfZmm",zlfpdf_zhfZmm,poly_zlf);
RooHistPdf zhfpdf_zhfZmm("zhfpdf_zhfZmm","zhfpdf_zhfZmm",vpt,zhf_zhfZmm);
RooProdPdf model_zhf_zhfZmm("model_zhf_zhfZmm","model_zhf_zhfZmm",zhfpdf_zhfZmm,poly_zhf);
RooRealVar zlffrac_zhfZmm("zlffrac_zhfZmm","zlffrac_zhfZmm",(hist_zhfZmm_zj0b->Integral()/(hist_zhfZmm_zhf->Integral()+hist_zhfZmm_sub->Integral())));
RooRealVar ttfrac_zhfZmm("ttfrac_zhfZmm","ttfrac_zhfZmm",(hist_zhfZmm_tt->Integral()/(hist_zhfZmm_zhf->Integral()+hist_zhfZmm_sub->Integral())));
//RooAddPdf model_zhfZmm("model_zhfZmm","model_zhfZmm",RooArgList(model_zlf_zhfZmm,model_tt_zhfZmm),zlffrac_zhfZmm);
RooAddPdf model_zhfZmm("model_zhfZmm","model_zhfZmm",RooArgList(model_zlf_zhfZmm,model_tt_zhfZmm,model_zhf_zhfZmm),RooArgList(zlffrac_zhfZmm,ttfrac_zhfZmm));
//RooRealVar n1("n1","n1",1,0,1000);
//RooRealVar n2("n2","n2",1,0,1000);
//RooExtendPdf model_ttZmm2("model_ttZmm2","model_ttZmm2",model_ttZmm,n1);
//RooExtendPdf model_zlfZmm2("model_zlfZmm2","model_zlfZmm2",model_zlfZmm,n2);

//RooHistPdf zlfpdf("zlfpdf","zlfpdf",vpt,zj0b_zlfZmm);
//RooProdPdf model_zlf("model_zlf","model_zlf",zlfpdf,poly_zlf);

//prod.chi2FitTo(data);
//prod.fitTo(data);
//model_ttZmm->chi2FitTo(data_ttZmm);
//model_tt_ttZmm->fitTo(data_ttZmm);

RooCategory sample("sample","sample") ;
sample.defineType("ttZmm") ;
sample.defineType("zlfZmm") ;
sample.defineType("zhfZmm") ;

RooDataSet *data = model_ttZmm.generate(RooArgSet(vpt),1000); 
RooDataSet *data2 = model_zlfZmm.generate(RooArgSet(vpt),1000); 
RooDataSet *data3 = model_zhfZmm.generate(RooArgSet(vpt),1000); 

//RooDataSet combData("combData","combined data",vpt,RooFit::Index(sample),RooFit::Import("ttZmm",*data),RooFit::Import("zlfZmm",*data2),RooFit::Import("zhfZmm",*data3)) ;
RooDataSet combData("combData","combined data",RooArgSet(vpt,sample));

//RooRealVar y("y","y",0,100000);
for (int i=1; i<hist_ttZmm_data->GetNbinsX()+1; i++) {
    vpt = hist_ttZmm_data->GetBinLowEdge(i) + 0.5*hist_ttZmm_data->GetBinWidth(i);
    float val = hist_ttZmm_data->GetBinContent(i);
    sample.setLabel("ttZmm");
//    combData.add(RooArgSet(vpt,sample),val);
    cout<<i<<":, "<<vpt<<", "<<val<<std::endl;
    for (int j=0; j<val; j++) {
        combData.add(RooArgSet(vpt,sample));
    }
}
for (int i=1; i<hist_zlfZmm_data->GetNbinsX()+1; i++) {
    vpt = hist_zlfZmm_data->GetBinLowEdge(i) + 0.5*hist_zlfZmm_data->GetBinWidth(i);
    float val = hist_zlfZmm_data->GetBinContent(i);
    sample.setLabel("zlfZmm");
    //combData.add(RooArgSet(vpt,sample));
    //combData.add(RooArgSet(vpt,sample),val);
    cout<<i<<":, "<<vpt<<", "<<val<<std::endl;
    for (int j=0; j<val; j++) {
        combData.add(RooArgSet(vpt,sample));
    }
}
for (int i=1; i<hist_zhfZmm_data->GetNbinsX()+1; i++) {
    vpt = hist_zhfZmm_data->GetBinLowEdge(i) + 0.5*hist_zhfZmm_data->GetBinWidth(i);
    float val = hist_zhfZmm_data->GetBinContent(i);
    sample.setLabel("zhfZmm");
    //combData.add(RooArgSet(vpt,sample));
    //combData.add(RooArgSet(vpt,sample),val);
    cout<<i<<":, "<<vpt<<", "<<val<<std::endl;
    for (int j=0; j<val; j++) {
        combData.add(RooArgSet(vpt,sample));
    }
}

RooSimultaneous simPdf("simPdf","simultaneous pdf",sample) ;

simPdf.addPdf(model_ttZmm,"ttZmm") ;
simPdf.addPdf(model_zlfZmm,"zlfZmm"); 
simPdf.addPdf(model_zhfZmm,"zhfZmm"); 
//simPdf.addPdf(model_ttZmm2,"ttZmm") ;
//simPdf.addPdf(model_zlfZmm2,"zlfZmm"); 

RooDataHist dh("dh","dh",*combData.get(),combData) ; 
RooChi2Var chi2("chi2","chi2",simPdf,dh);
RooMinuit m2(chi2);
m2.migrad();
//m2.minos();

//std::cout<<"simPDF.canBeExtend() = "<<simPdf.canBeExtended()<<std::endl;
//simPdf.chi2FitTo(combData) ;
//simPdf.fitTo(combData) ;


//RooChi2Var chi2_var_A("","", model_ttZmm, *data_ttZmm);
//RooMinuit m2_var_A(chi2_var_A);
//m2_var_A.migrad();

//poly_tt.fitTo(data);
//poly_tt.fitTo(data,SumW2Error(kFALSE));

//RooPlot* frame = vpt.frame();
//data_ttZmm.plotOn(frame);
//poly_tt.plotOn(frame);
//poly_zlf.plotOn(frame,LineColor(kGreen));
//model_ttZmm.plotOn(frame,LineColor(kRed));
//model_tt_ttZmm.plotOn(frame,LineColor(kBlue));
//model_zlf_ttZmm.plotOn(frame,LineColor(kGreen));

//combData.plotOn(frame,Cut("sample==sample::ttZmm")) ;
//simPdf.plotOn(frame,Slice(sample,"ttZmm"),ProjWData(sample,combData)) ;
//simPdf.plotOn(frame,Slice(sample,"ttZmm"),Components("model_ttWm"),ProjWData(sample,combData),LineStyle(kDashed)) ;

RooPlot* frame1 = vpt.frame(Bins(60),Title("TT CR")) ;
combData.plotOn(frame1,Cut("sample==sample::ttZmm")) ;
simPdf.plotOn(frame1,Slice(sample,"ttZmm"),ProjWData(sample,combData)) ;
simPdf.plotOn(frame1,Slice(sample,"ttZmm"),Components("model_tt_ttZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kBlue)) ;
simPdf.plotOn(frame1,Slice(sample,"ttZmm"),Components("model_zlf_ttZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kGreen)) ;
simPdf.plotOn(frame1,Slice(sample,"ttZmm"),Components("model_zhf_ttZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kViolet)) ;
simPdf.plotOn(frame1,Slice(sample,"ttZmm"),Components("model_ttZmm"),ProjWData(sample,combData),LineStyle(kDashed)) ;

RooPlot* frame2 = vpt.frame(Bins(60),Title("ZLF CR")) ;
combData.plotOn(frame2,Cut("sample==sample::zlfZmm")) ;
simPdf.plotOn(frame2,Slice(sample,"zlfZmm"),ProjWData(sample,combData)) ;
simPdf.plotOn(frame2,Slice(sample,"zlfZmm"),Components("model_tt_zlfZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kBlue)) ;
simPdf.plotOn(frame2,Slice(sample,"zlfZmm"),Components("model_zlf_zlfZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kGreen)) ;
simPdf.plotOn(frame2,Slice(sample,"zlfZmm"),Components("model_zhf_zlfZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kViolet)) ;
simPdf.plotOn(frame2,Slice(sample,"zlfZmm"),Components("model_zlfZmm"),ProjWData(sample,combData),LineStyle(kDashed));

RooPlot* frame3 = vpt.frame(Bins(60),Title("ZHF CR")) ;
combData.plotOn(frame3,Cut("sample==sample::zhfZmm")) ;
simPdf.plotOn(frame3,Slice(sample,"zhfZmm"),ProjWData(sample,combData)) ;
simPdf.plotOn(frame3,Slice(sample,"zhfZmm"),Components("model_tt_zhfZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kBlue)) ;
simPdf.plotOn(frame3,Slice(sample,"zhfZmm"),Components("model_zlf_zhfZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kGreen)) ;
simPdf.plotOn(frame3,Slice(sample,"zhfZmm"),Components("model_zhf_zhfZmm"),ProjWData(sample,combData),LineStyle(kDashed),LineColor(kViolet)) ;
simPdf.plotOn(frame3,Slice(sample,"zhfZmm"),Components("model_zhfZmm"),ProjWData(sample,combData),LineStyle(kDashed));

//TCanvas* c = new TCanvas("rf501_simultaneouspdf","rf403_simultaneouspdf",600,600) ;
TCanvas* c = new TCanvas("rf501_simultaneouspdf","rf403_simultaneouspdf",1600,800) ;
c->Divide(3) ;
c->cd(1) ; gPad->SetLeftMargin(0.15) ; frame1->GetYaxis()->SetTitleOffset(1.4) ; frame1->Draw() ;
c->cd(3) ; gPad->SetLeftMargin(0.15) ; frame2->GetYaxis()->SetTitleOffset(1.4) ; frame2->Draw() ;
c->cd(2) ; gPad->SetLeftMargin(0.15) ; frame3->GetYaxis()->SetTitleOffset(1.4) ; frame3->Draw() ;

//frame3->Draw();

std::cout<<"TT chi2/ndof = "<<frame1.chiSquare()<<std::endl;;
std::cout<<"ZHF chi2/ndof = "<<frame3.chiSquare()<<std::endl;;
std::cout<<"ZLF chi2/ndof = "<<frame2.chiSquare()<<std::endl;;

frame3.Print();
//ttpdf.plotOn(frame);
//nb.plotOn(frame);
//expo.plotOn(frame);
//bkgmodel.plotOn(frame);
//CBall.plotOn(frame);
//std::cout<<"chi2/ndof = "<<frame.chiSquare()<<std::endl;;
//frame.Draw();

//RooPlot* frame2 = vpt.frame();
//data_zlfZmm.plotOn(frame2);
//poly_tt.plotOn(frame2);
//poly_zlf.plotOn(frame2,LineColor(kGreen));
//model_zlfZmm.plotOn(frame2,LineColor(kRed));
//std::cout<<"chi2/ndof = "<<frame2.chiSquare()<<std::endl;;
//frame2.Draw();

std::cout<<hist_zhfZmm_data->Integral()<<std::endl;

std::cout<<ttfrac_ttZmm->getVal()<<std::endl;;

std::cout<<(1-zlffrac_zhfZmm->getVal()-ttfrac_zhfZmm->getVal())<<std::endl;;

std::cout<<zlffrac_zlfZmm->getVal()<<std::endl;;

//std::cout<<(hist_zlfZmm_zj0b->Integral()/(hist_zlfZmm_zj0b->Integral()+hist_zlfZmm_sub->Integral()))<<std::endl;;

}
