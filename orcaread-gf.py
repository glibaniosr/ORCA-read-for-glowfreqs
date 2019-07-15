# Script written for Python 3.6
# Made by Gabriel L. S. Rodrigues for use with the glofreqs program cited below:
# Gannon, Glowacki et al., Faraday Discussions, 2010, 147, 173-188

import sys, re, os, getopt

s_version = "1.0.1"
#--- Utility Functions
# Function to construct an array
def make_array(r,c):
  array = [[0 for col in range(c)] for row in range(r)]
  return array
#--- END of Functions

# Getopt Parameters
usage = "Usage: orcaread.py -i hess_file.hess -g grad_file.engrad"
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:g:o:hv', ['hess=', 'grad=', 'help', 'version'])
except getopt.GetoptError:
    print(usage)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(usage)
        sys.exit(2)
    if opt in ('-v', '--version'):
        print("ORCA read to glowfreq Version {:s}".format(s_version))
        sys.exit(2)
    elif opt in ('-i', '--hess'):
        hess_file = arg
        hfile_base, hfile_ext = os.path.splitext(hess_file)
        info_file = hfile_base+".info"
    elif opt in ('-g', '--grad'):
        grad_file = arg
        gfile_base, gfile_ext = os.path.splitext(grad_file)
    else:
        print(usage)
        sys.exit(2)

#--- Get the HESSIAN matrix and some parameters
## Store the entire Hessian in memory from the .hess ORCA file
with open(hess_file, 'r') as inp:
    for line in inp:
        if not "$hessian" in line: # Flag for the Hessian group
            continue
        else:
            ## Get the Hessian size and other parameters
            # ORCA prints the Hessian in text with all lines from 5 columns each time.
            # Therefore, it will be printed n5_sets = hess_size//5 sets with hess_size number of lines.
            # In the last set will be printed rest = hess_size%5 columns with hess_size lines.
            # OBS: From version 4.1.2, ORCA started to print the Hessian in sets of 6 columns
            for data in inp:
                ##--- Important Parameters
                hess_size = int(data.strip())
                n_atoms = int(hess_size/3)
                n5_sets = hess_size//6 # Number of 5 columns sets. 
                rest = hess_size%6
                if rest == 0:
                    n5_sets = n5_sets-1 # If the size is divisible by 5, then the sets would be larger.
                    rest = 6
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

#--- Write the data in the information file
with open(info_file, 'w') as out:
    ## Number of atoms
    out.writelines(hfile_base+": Number of atoms\n"+str(n_atoms)+"\n")
    ## Standard orientation
    out.writelines(hfile_base+": Standard orientation (Bohr)\n")
    for line in xyz_data:
        for idx,element in enumerate(line):
            if idx == 0:
                out.writelines(str(element).ljust(4))
            else:
                out.writelines(str("{:.8f}".format(element)).rjust(20))
        out.writelines("\n")
    ## Hessian
    # Only the half of the diagonal Hessian must be outputed
    out.writelines(hfile_base+": Hessian (Hartree/Bohr^2)")
    for i,line in enumerate(hess_data):
        for j,element in enumerate(line):
            if j == 0:
                continue
            elif j > i+1:
                break
            elif j%4 == 1:
                out.writelines("\n"+str(line[0]).rjust(4))
                out.writelines(str("{:.8f}".format(element)).rjust(20))
            else:
                out.writelines(str("{:.8f}".format(element)).rjust(20))
    out.writelines("\n")
    ## Gradient
    out.writelines(hfile_base+": Gradient (Hartree/Bohr)\n") 
    for line in grad_data:
        for idx,element in enumerate(line):
            if idx == 0:
                out.writelines(str(element).ljust(4))
            else:
                out.writelines(str("{:.8f}".format(element)).rjust(20))
        out.writelines("\n")