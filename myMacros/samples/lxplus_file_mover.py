#! /usr/bin/env python

# ===================================================
# Python script to move files from DAS to servers. Also combines files
#
# Must be on lxplus with voms actiavted!!
#
# 2/15/2015 David Curry
# ===================================================

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
import multiprocessing
from ROOT import *


# file destination on EOS
eos_path = '/store/user/dcurry/heppy/v14/'

# final combined destination on uftrig
uftrig_path = '/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/'

# ===========================

# Define what files to move from DAS to CERN eos
file_list  = []
file_names = []



