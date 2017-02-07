import os
import math

#name = 'ScaleFactor_tracker_80x'
name = 'ScaleFactor_MVAIDWP80_80x'


json = open('80x/'+name+'.json', 'w')
inp  = open('80x/'+name+'.txt', 'r')

ptbins = []
etabins= []

json.write('{\n')
#json.write("    \"ScaleFactor_doubleElectron76x\" : {\n")
json.write("    \""+name+"\" : {\n")
json.write('        \"eta_pt_ratio\" : {\n')
for line in inp.readlines():
     split = line.split()
     print 'split1', split
     ptbin = [split[2], split[3]]
     etabin = [split[0], split[1]]
     
     if ptbin not in ptbins:
         ptbins.append(ptbin)
     if etabin not in etabins:
           etabins.append(etabin)

print 'ptbins:', ptbins
print 'etabins:', etabins


inp.close()

iEtabin = 0
iPtbin  = 0

#for ptbin in ptbins:    
for etabin in etabins:
     iEtabin +=1
     json.write('            "eta:[' + etabin[0] + ','+ etabin[1] + ']\": {\n')
     inp = open('80x/'+name+'.txt', 'r')

     first = True
     for line in inp.readlines():   
        iPtbin +=1 
        split = line.split()
        print 'split2', split
        bin1 = [split[0], split[1]]
        bin2 = [split[2], split[3]]
        
        if bin1 != etabin: continue

        #print bin1
        #if not first:
        #     json.write(',\n')
        #     first = False

        #sf = str( float(split[4])/float(split[6]) )
        #err = str( math.sqrt( float(split[5])/float(split[4])*float(split[5])/float(split[4]) + 
        #                 float(split[7])/float(split[6])*float(split[7])/float(split[6]) ) )

        sf  = str(float(split[4]))
        err = str(float(split[5])) 

        bin2 = [split[2], split[3], sf, err]
        json.write('                \"pt:[' + split[2] + ','+split[3] + ']\": {\n')
        json.write('                    \"value\": '+ split[4]+",\n")   
        json.write('                    \"error\": '+ split[5]+"\n")           
        json.write('                },\n')

        
    #json.write('\n')

     inp.close()
     json.write('            },\n')

json.write('        }\n')
json.write('    }\n')
json.write('}\n')

json.close()
inp.close()
