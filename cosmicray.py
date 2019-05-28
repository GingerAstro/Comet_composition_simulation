# need to sort: 
#    access .cl file from default location
#    define file path so program can be run from any location?
#    A better way of selecting files that need processed
#    Quantitative method for deciding on optimal settings

from pyraf import iraf
import os
import glob
import time

#iraf.noao()
iraf.stsdas()

##EPAR settings for LACOS.SPEC
iraf.lacos_spec.gain = 1.2
iraf.lacos_spec.readn = 4.2
iraf.lacos_spec.xorder = 3.0
iraf.lacos_spec.yorder = 3.0
iraf.lacos_spec.sigclip = 3.9
iraf.lacos_spec.sigfrac = 2.0
iraf.lacos_spec.objlim = 1.0
iraf.lacos_spec.niter = 4
iraf.lacos_spec.verbose = "n"

start = time.time()
n=0

#Produce input and output file names (Need to fix for file duplicates)
inlist = list(glob.glob(os.path.join('wi*.*')))
outlist = ["c" + file for file in inlist]
i = len(inlist)
print "Files to process: ", i 

#processing LACOS on each file
while n < i:
    print "workin on file", inlist[n], "(", n+1, ")"
    iraf.lacos_spec(inlist[n], outlist[n], 'temp.pl')
    n +=1
    os.remove('temp.pl')
    time.sleep(5) #Needed as LACOS was slow at deleting files when it finishes
       
print "Finished"
end = time.time()
print "Run Time: ", end - start