import re
import os
import time
import math
import glob
#import pandas as pd
#import numpy as np
from libraries import *
from variables import *
from atreader import *
nat,ntyp=len(geom)-2,len(species)

pre=molname
title=molname
file=pre
filein=file+'.in'

input = open(filein, 'w')       
input.write('&CPMD\n')
input.write('rESTART WAVEFUNCTION LATEST \nrESTART WAVEFUNCTION COORDINATES VELOCITIES LATEST \nrESTART NOSEP ACCUMULATORS LATEST\n')
input.write('mOLECULAR DYNAMICS CP \nOPTIMIZE GEOMETRY XYZ\noPTIMIZE WAVEFUNCTION\n')
input.write('qUENCH BO \nlSD\n')
input.write('CONVERGENCE ORBITAL \n%s\n' %(conv_ob))
input.write('CONVERGENCE GEOMETRY \n%s\n' %(conv_geo))
input.write('MAXSTEPS \n%s\n' %(max_step))
input.write('MAXITER \n%s\n' %(max_iter))
input.write('MAXCPUTIME \n%s\n' %(max_cputime))
input.write('TIMESTEP \n%s\n' %(time_step))
input.write('EMASS \n%s\n' %(e_mass))
input.write('STORE \n%s\n' %(store))
input.write('nOSE IONS MASSIVE \n%s  %s\n' %(temp_ion, frequency_ion))
input.write('TRAJECTORY SAMPLE XYZ \n%s\n' %(traject_sample))
input.write('GDIIS \n%s \n' %(gdiis))
input.write('PRINT COORDINATES FORCES ENERGIES wannier \n%s \n' %(print_step))
input.write('COMPRESS WRITE %s \n' %(compress))
input.write('CP_GROUPS \n%s\n' %(cp_groups))
input.write('LBFGS\n')
input.write('&END\n')

input.write('\n&DFT\n')
input.write('nEWCODE\n')
input.write('FUNCTIONAL %s\n' %(func))
input.write('GC-CUTOFF \n%s\n' %(gc_cutoff))
input.write('&END\n')
       
input.write('\n&SYSTEM\n')
input.write('ANGSTROM\n')
input.write('SYMMETRY\n%s\n' %(symmetry))
input.write('sURFACE  %s\n' %(surface))
input.write('pOISSON SOLVER  %s\n' %(poisson))
input.write('CELL \n%s %s %s 0 0 0 \n' %(a,b,c))
input.write('CUTOFF\n%s\n' %(en_cutoff))
input.write('CHARGE\n%s\n' %(charge))
input.write('mULTIPLICITY\n%s\n' %(multiplicity))
input.write('KPOINTS MONKHORST-PACK \n %s %s %s \n' %(k1, k2, k3))
input.write('&END\n')

input.write('\n&VDW\n')
input.write('eMPIRICAL CORRECTION\nVDW pARAMETERS\naLL DFT-D2\n')
input.write('vDW-CUTOFF\n%s\n' %(vdw_cutoff))
input.write('vDW-CELL\n%s\n' %(vdw_cell))
input.write('eND EMPIRICAL CORRECTION\n')
input.write('&END\n')

geo=open(molname+'.xyz','r').readlines()
input.write('\n&ATOMS\n')
for at in range(0,ntyp):
 input.write(pseudos[re.sub('[0-9]','',species[at])][0]+'\n')
 input.write('LMAX= %s\n' %(lmax))
 #input.write(species[at]+'\n')
 for at0 in range(2,nat+2):
  if (geo[at0].split()[0] == species[at]):
   count +=1
 input.write('%s \n' %(count))
 count = 0
 #geo[n]=geo[n].split()[1]+' '+geo[n].split()[2]+' '+geo[n].split()[3]+'\n'
 for at0 in range(2,nat+2):
  if (geo[at0].split()[0] == species[at]):
   input.write(geo[at0].split()[1]+' '+geo[at0].split()[2]+' '+geo[at0].split()[3]+'\n')
 input.write('\n')
input.write('&END\n')

input.close()

file=pre
filein=file+'.tmp1'
input = open(filein, 'w')
geo=open(molname+'.xyz','r').readlines()
for at0 in range(2,nat+2):
 count +=1
 input.write('%s'%(count)+' '+geo[at0].split()[0]+' '+geo[at0].split()[1]+' '+geo[at0].split()[2]+' '+geo[at0].split()[3]+'\n')
count = 0
input.close()

file=pre
filein=file+'.tmp'
input = open(filein, 'w')
geo=open(molname+'.tmp1','r').readlines()
for at in range(0,ntyp):
 for at0 in range (0,nat+0): 
  if (geo[at0].split()[1] == species[at]):
   count +=1
   input.write(geo[at0].split()[0]+' '+geo[at0].split()[1]+' '+'%s'%(count)+' '+geo[at0].split()[2]+' '+geo[at0].split()[3]+' '+geo[at0].split()[4]+'\n')
 count = 0 
input.close()

file=pre
filein=file+'.surface_atoms'
input = open(filein, 'w')
geo=open(molname+'.tmp','r').readlines()
for at0 in range(0,nat+0):
 z=float(geo[at0].split()[5])
 list_z.append(z)
top_z= max(list_z)
print (top_z)
for at0 in range(0,nat+0):
 if (((float(geo[at0].split()[5]))+3) >= top_z):
  input.write(geo[at0].split()[0]+' '+geo[at0].split()[1]+' '+geo[at0].split()[2]+' '+geo[at0].split()[3]+' '+geo[at0].split()[4]+' '+geo[at0].split()[5]+'\n')
input.close()

print "done\n"
os.remove(file+'.tmp1')

filein=file+'.make_dos'
input = open(filein, 'w')
geo=open(molname+'.surface_atoms','r').readlines()
input.write('/home/theanh/anaconda3/bin/sumo-dosplot --xmin -6 --xmax 6 --total-only\n')
for at in range(0,ntyp):
 input.write('/home/theanh/anaconda3/bin/sumo-dosplot --xmin -6 --xmax 6 --atoms'+' '+species[at])
 for x in geo:
  if (x.split()[1] == species[at]):
   input.write('.'+x.split()[2])
 input.write('\n')

input.close()
