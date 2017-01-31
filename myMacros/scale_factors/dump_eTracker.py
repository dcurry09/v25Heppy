import os
import math

name = 'egammaEffi_tracker'
# name = 'ScaleFactor_egammaEff_WP90'


json = open(name+'.json', 'w')
inp = open(name+'.txt', 'r')

ptbins = []

json.write('{\n')
json.write("    \"egammaEffi_tracker\" : {\n")
json.write('        \"eta_pt_ratio\" : {\n')
for line in inp.readlines():
     split = line.split()
     print 'split1', split
     ptbin = [split[2], split[3], split[4], split[5]]
     if ptbin not in ptbins:
         ptbins.append(ptbin)
print 'ptbins:', ptbins

inp.close()

for ptbin in ptbins:    
    json.write('            "eta:[' + ptbin[0] + ','+ ptbin[1] + ']\": {\n')
    inp = open(name+'.txt', 'r')

    first = True
    for line in inp.readlines():   
        split = line.split()
        print 'split2', split
        bin1 = [split[0], split[1]]
        #if bin1 != ptbin :
        #    continue
        #print bin1
        #if not first:
        #     json.write(',\n')
        #     first = False

        #sf = str( float(split[4])/float(split[6]) )
        #err = str( math.sqrt( float(split[5])/float(split[4])*float(split[5])/float(split[4]) + 
        #                 float(split[7])/float(split[6])*float(split[7])/float(split[6]) ) )

        sf  = str(float(split[4]))
        err = str(float(split[5])) 

        bin2 = [split[0], split[1], sf, err]
        json.write('                \"pt:[' + bin2[0] + ','+bin2[1] + ']\": {\n')
        json.write('                    \"value\": '+ ptbin[2]+",\n")   
        json.write('                    \"error\": '+ ptbin[3]+"\n")           
        json.write('                },\n')
        break
        
    #json.write('\n')

    inp.close()
    json.write('            },\n')

json.write('        }\n')
json.write('    }\n')
json.write('}\n')

json.close()
inp.close()
