# ORCA-read-for-glowfreq
Python script to prepare .info files for the glowfreq program from ORCA quantum chemistry calculations.

**Version 1.0.0 - October of 2018**

The glowfreq program (reference below) was developed by the group of David Glowacki in the University of Bristol in order 
to carry out vibrational analysis at the MECP. 
It works really well in conjunction with MESMER (Master Equation Solver for Multi Energy-well Reactions).

### glowfreq

*Gannon, Glowacki et al., Faraday Discussions, 2010, 147, 173-188*

### MESMER

*Plane, ..., Glowacki, et al., Journal of Chemical Physics, 2012, 137, 014310*

http://sourceforge.net/projects/mesmer/

### ORCA 

ORCA is a software developed and maintained by prof. Frank Neese and coworkers at Max Planck Institute for Chemical Energy Conversion.
It's official website can be acessed at: **https://orcaforum.cec.mpg.de**

**The following text was taken from ORCA official website above.**

"The program ORCA is a modern electronic structure program package written by F. Neese, with contributions from many current and former coworkers and several collaborating groups. The binaries of ORCA are available free of charge for academic users for a variety of platforms.
ORCA is a flexible, efficient and easy-to-use general purpose tool for quantum chemistry with specific emphasis on spectroscopic properties of open-shell molecules. It features a wide variety of standard quantum chemical methods ranging from semiempirical methods to DFT to single- and multireference correlated ab initio methods. It can also treat environmental and relativistic effects.
Due to the user-friendly style, ORCA is considered to be a helpful tool not only for computational chemists, but also for chemists, physicists and biologists that are interested in developing the full information content of their experimental data with help of calculations."

**More help using ORCA can be found at ORCA Input Library: https://sites.google.com/site/orcainputlibrary/**

### ORCA-read

The python code in the ORCA-read-for-glowfreq was written just to extract the necessary information of a .hess and .engrad ORCA calculation
in order to do a vibrational analysis at the MECP by the glowfreq program which can be even further expanded to a study using the MESMER software.

## USAGE

**1) Get the Hessian** 

Do a Hessian calculation for all the states of the system at the MECP on ORCA (ex.: a singlet and a triplet state at MECP geometry).
This calculations will generate *.hess* files that will be needed.

**2) Get the Gradient**

If you get all information from an ORCA MECP optimization, the program will automatically compute the hessian from both states at the MECP
and will also generate all the gradients and place it in a *.engrad* file. In case you run a single point calculation just for the hessian
and the program do not print this file or the gradient, the best way is to run a new ```OPT``` calculation setting ```MaxIter 1``` in
the ```%geom``` block of the ORCA input. 

You can also get the desired gradients from an ORCA output file and copy it to a text file in the following format:

```
  # gradient in Eh/bohr
  #
      -0.003848028637
      -0.001799515893
      -0.000088818174
       0.000691429518
      -0.000341034250
      -0.000089399101
       0.008371481069
       0.001214831891
       0.000319221171
      -0.004901619992
       0.004082508772
      -0.000312011010
      -0.000312599429
      -0.003270591712
       0.000164498027
  #
```

**3) Run the code**

After that just run the python script for each of the MECP states, supplying the *.hess* and the gradient files, to create the *.info*
files for the **glowfreq** analysis. The syntax for the script run is just as follows:

```
orcaread.py -i hess_file.hess -g grad_file.engrad
```

The is also the ```-h``` or ```--help``` option to print the above usage.


Code written by Gabriel L. S. Rodrigues.
