# dos-surface
#This module deals with the PDOS of the surface atoms

1. You need to run DOS calculation in VASP to get the "vasprun.xml" file
2. You need to have a coordinates file *.xyz (in this folder, that file is "g0H.xyz")
3. Change the "molname" in the "variables.py" file into "g0H" which is identical to the name of *.xyz file
4. By typing "python2.7(space)jobrun.py", The python program will create a CPMD input file("g0H.in"), "g0H.tmp" file which stores the coordinates of all atoms and their stt, "g0H.surface_atoms" which stores the coordinates and stt of surface atoms only (I define a surface atom is the one which stays less than 3 angstroms (you can change is number as you like) below the topmost atom along the Z direction), "g0H.make_dos" file which uses "sumo" python code to get the PDOS of all atoms and surface atoms from "vasprun.xml"
5. chmod +x "g0H.make_dos" file and executize it: ./g0H.make_dos
6. The *.pdf file is output picture, the data files are "*.dat"  

With this module, we can handle million atoms easily!
