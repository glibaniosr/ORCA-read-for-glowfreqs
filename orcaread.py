# Script written for Python 3.6
# Made by Gabriel L. S. Rodrigues for use with the glofreqs program cited below:
# Gannon, Glowacki et al., Faraday Discussions, 2010, 147, 173-188

import sys
import re
import os

#--- Utility Functions
# Function to construct an array
def make_array(r,c):
  array = [[0 for col in range(c)] for row in range(r)]
  return array

#--- END of Functions

#--- Variables
## Files
hfile_base, hfile_ext = os.path.splitext(sys.argv[1])
hess_file = hfile_base+hfile_ext
gfile_base, gfile_ext = os.path.splitext(sys.argv[2])
grad_file = gfile_base+gfile_ext
info_file = hess_file+".info"
## Calculation Parameters

#--- END of variables

#--- Get the HESSIAN matrix and some parameters
## Store the entire Hessian in memory from the .hess ORCA file
with open(hess_file, 'r') as inp:
    for line in inp:
        if not "$hessian" in line: # Flag for the Hessian group
            continue
        else:
            ## Get the Hessian size
            # ORCA prints the Hessian in text with all lines from 5 columns each time.
            # Therefore, it will be printed n5_sets = hess_size//5 sets with hess_size number of lines.
            # In the last set will be printed rest = hess_size%5 columns with hess_size lines.
            for data in inp:
                ##--- Important Parameters
                hess_size = int(data.strip())
                n_atoms = int(hess_size/3)
                n5_sets = hess_size//5 # Number of 5 columns sets. 
                rest = hess_size%5
                if rest == 0:
                    n5_sets = n5_sets-1 # If the size is divisible by 5, then the sets would be larger.
                    rest = 5
                ## Create the HESSIAN array
                hess_data = make_array(hess_size,hess_size+1)
                ## Write the number of the output line in the first element of the hess_data matrix
                for n_line in range(hess_size):
                    hess_data[n_line][0] = n_line+1
                next(inp) # Jump the second line.
                break
            #for data in inp: # Jump the second line (improve this)
            #    break
            count = 0
            while count <= n5_sets:
                count2 = 0
                ## First get the data from all sets of 5 columns except the last one if rest
                # is not zero.
                if count != n5_sets:
                    for data in inp:
                        columns = [ int(num) for num in range(count*5,(count)*5+5) ]
                        data = data.split()
                        n_line = int(data[0])
                        if  count2 >= hess_size:
                            break
                        for i in range(5):
                            j = columns[i] + 1
                            hess_data[n_line][j] = float(data[i+1])
                        count2 += 1
                ## This is the condition for the last sets of column that will not be zero
                # if the size of the HESS matrix is not divisible by 5.
                else:
                    for data in inp:
                        columns = [ int(num) for num in range(count*5,(count)*5+rest) ]
                        if data.strip() == '':
                            break
                        data = data.split()
                        n_line = int(data[0])
                        if  count2 >= hess_size:
                            break
                        for i in range(rest):
                            j = columns[i] + 1
                            hess_data[n_line][j] = float(data[i+1])
                        count2 += 1
                count += 1

#--- Get the Standard Orientation (Bohrs) from the .hess file
## Create the xyz_data array with the cartesian coordinates in Bohrs
xyz_data = make_array(n_atoms,4)
with open(hess_file, 'r') as inp:
    for line in inp:
        if not "$atoms" in line: # Flag for the Hessian group
            continue
        else:
            next(inp) # Jump the first line with the number of atoms.
            for idx,data in enumerate(inp):
                if data.strip() == '':
                    break
                data = data.strip().split()
                xyz_data[idx] = [ data[0], float(data[2]), float(data[3]), float(data[4]) ]

#--- Get the Gradient from the .engrad ORCA file
## Create the grad_data array with the x, y and z values in Hartree/Bohr
grad_data = make_array(n_atoms,4)
## Get the gradient information from the .engrad file
with open(grad_file, 'r') as inp:
    for line in inp:
        if not "gradient in Eh/bohr" in line: # Flag for gradient group, and possibility to write on file.
            continue
        else:
            next(inp) # Jump the first line with a comment symbol.
            xyz_temp = []
            for idx,data in enumerate(inp):
                if data.strip() == '#':
                    break
                data = data.strip()
                xyz_temp.append(float(data))
                if (idx+1)%3 == 0:
                    nline = (idx+1)//3 - 1
                    grad_data[nline] = [ xyz_data[nline][0], float(xyz_temp[0]), float(xyz_temp[1]), float(xyz_temp[2]) ]
                    xyz_temp = []






#--- Write the Hessian to the file (only bottom elements, hence Hij with i<j)
# with open(info_file, 'w'):
#     n_line = 0
#     while n_line < hess_size:
#         line = [ "{:10.8f}".format(element) for element in hess_data[n_line] ]
#         i = 0
#         j = 0
#         #while i <= j:

        
        
#         print("\n")
#         n_line += 1