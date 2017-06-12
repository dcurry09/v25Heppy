import sys
import os

# The two pull .txt for comparison
filename1 = '/afs/cern.ch/user/d/dcurry/www/NuisancePulls_ZllHbb_Datacards_CrossCheckZll_5_24/Zll_SigPlusBKG_data_pulls.txt'
filename2 = '/afs/cern.ch/user/d/dcurry/www/NuisancePulls_ZllHbb_Datacards_ZlfMjjCut_oldCMVA_SR0to1_v2_6_1/Zll_SigPlusBKG_data_pulls.txt'

outpath = '/afs/cern.ch/user/d/dcurry/www/NuisanceComparison_Nominalvs0to1_6_2/'
outfile = outpath+'comparePulls.txt'
if os.path.isfile(outfile): os.remove(outfile) 
_outfile = open(outfile, "w")

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)

def BuildDict(lines):
    pullDict={}
    for i,line in enumerate(lines):
        if i == 0: continue
        #print line
        line=line.replace(",","")
        line=line.replace("*","")
        line=line.replace("!","")
        items=line.split()
        #print 'items:',items
        try:
            pullDict[items[0]]=[items[3],items[4]]
            #print 'SYS:', pullDict[items[0]], items[4],items[5]
        except:
            print "can't parse",line

    return pullDict

def ComputePullofPulls(pull1,pull2):
    #print 'Pulls1:', pull1[0],pull1[1]
    #print 'Pulls2:', pull2[0],pull2[1]
    out = (float(pull1[0])-float(pull2[0]))/(0.5*(float(pull1[1])+float(pull2[1])))
    return out

def CheckAndPrint(diff):
    iCount=0
    iTiny=0
    for syst in commonKeys:
        pull=ComputePullofPulls(dict1[syst],dict2[syst])
        if pull>diff:
            iCount=iCount+1
            #print "{0:40}  Pull1: {1}, Pull2: {2}, Difference/average: {3}".format(syst,str(dict1[syst]),str(dict2[syst]),str(pull))
            _outfile.write("\n{0:40}  Pull1: {1}, Pull2: {2}, Difference/average: {3}".format(syst,str(dict1[syst]),str(dict2[syst]),str(pull)))
        if pull<0.05:
            iTiny=iTiny+1    

    #print iTiny,"out of",len(commonKeys),"nuissances with diff/avg < ",0.05
    #print iCount,"out of",len(commonKeys),"nuissances with diff/avg > ",diff
    _outfile.write("\n{0} out of {1} nuissances with diff/avg < {2}".format(str(iTiny),str(len(commonKeys)),str(0.05)))
    _outfile.write("\n{0} out of {1} nuissances with diff/avg > {2}".format(str(iCount),str(len(commonKeys)),str(diff)))

    

try:
    outlabel=sys.argv[3]
except:
    outlabel=outpath+'PullComparison.txt'


file1=open(filename1)
file2=open(filename2)


lines1=file1.readlines()
lines2=file2.readlines()

dict1=BuildDict(lines1)
dict2=BuildDict(lines2)

keys1=dict1.keys()
keys2=dict2.keys()

commonKeys=list(set(keys1).intersection(keys2))

print len(keys1),len(keys2),len(commonKeys)

commonKeys.sort()

CheckAndPrint(0.2)
_outfile.write("\n\n")
CheckAndPrint(0.5)

_outfile.close()

# iCount=0
# diff=0.2
# for syst in commonKeys:
#     pull=ComputePullofPulls(dict1[syst],dict2[syst])
#     if pull>diff:
#         iCount=iCount+1
#         #print syst,dict1[syst],dict2[syst],pull
#         print "{0:40}  Pull1: {1}, Pull2: {2}, Difference/average: {3}".format(syst,str(dict1[syst]),str(dict2[syst]),str(pull))
        

# print iCount,"out of",len(commonKeys),"different nuissances with diff/avg > ",diff
