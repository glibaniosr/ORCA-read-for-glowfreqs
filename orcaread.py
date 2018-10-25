# Script written for Python 3.6
# Made by Gabriel L. S. Rodrigues for use with the glofreqs program cited below:
# Gannon, Glowacki et al., Faraday Discussions, 2010, 147, 173-188

import sys
import re
import numpy

#--- Utility Functions
# Function to construct an array
def make_array(r,c):
  array = [[0 for col in range(c)] for row in range(r)]
  return array

#--- END of Functions

n_atoms = 38 #sys.argv[1]
hess_file = "ru3-no-salen-cl-mecp.hess" # nohno-sing-mecp.freq.hess"#sys.argv[2]
info_file = "nohno-sing-mecp.freq.info"
hess_size = n_atoms*3
### ORCA prints the Hessian in text with all lines from the 5 columns each time.
# Therefore, it will be printed n_sets = hess_size//5 sets with hess_size number of lines
# and in the last set will be printed n_rest = hess_size%5 columns with hess_size lines. 
n_sets = hess_size//5
rest = hess_size%5 

#--- Create the HESSIAN array
hess_data = make_array(hess_size,hess_size+1)
# Write the number of the output line in the first element of the hess_data matrix
for n_line in range(hess_size):
    hess_data[n_line][0] = n_line+1
# Get the entire HESSIAN matrix in the memory (can be dangerous) from the .hess ORCA file
with open(hess_file, 'r') as inp:
    for line in inp:
        if not "$hessian" in line:
            continue
        else:
            for data in inp:
                break
            for data in inp:
                break
            count = 0
            while count <= n_sets:
                columns = [ int(num) for num in range(count*5,(count+1)*5) ]
                count2 = 0
                if count != n_sets:
                    for data in inp:
                        #if data.strip() == '':
                            #break
                        data = data.split()
                        n_line = int(data[0])
                        if  count2 >= hess_size:
                            break
                        for i in range(5):
                            #hess_data[n_line][columns[sets*i+1]] = float(data[i+1])
                            j = columns[i] + 1
                            hess_data[n_line][j] = float(data[i+1])
                        count2 += 1
                else:
                    for data in inp:
                        if data.strip() == '':
                            break
                        data = data.split()
                        n_line = int(data[0])
                        if  count2 >= hess_size:
                            break
                        for i in range(rest):
                            #hess_data[n_line][columns[sets*i+1]] = float(data[i+1])
                            j = columns[i] + 1
                            hess_data[n_line][j] = float(data[i+1])
                        count2 += 1
                count += 1


#--- Write the Hessian to the file (only bottom elements, hence Hij with i<j)
with open(info_file, 'w'):
    n_line = 0
    while n_line < hess_size:
        line = [ "{:10.8f}".format(element) for element in hess_data[n_line] ]
        i = 0
        j = 0
        #while i <= j:

        
        
        print("\n")
        n_line += 1