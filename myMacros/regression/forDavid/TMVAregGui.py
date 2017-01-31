
# WORKS ON LXPLUS ONLY

# Launch the Gui

import ROOT
import os

os.system('. /cvmfs/sft.cern.ch/lcg/releases/ROOT/6.04.02-a6f71/x86_64-slc6-gcc49-dbg/bin/thisroot.sh')

os.system('source /cvmfs/sft.cern.ch/lcg/releases/gcc/4.9.3/x86_64-slc6/setup.sh')

os.system('export PATH=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.9.p1-df007/x86_64-slc6-gcc49-opt/bin/:$PATH')

os.system('python')

# From here type  ROOT.TMVA.TMVAGui('TMVAoutput.root')
