# ISOV


### How to Run

The python program is simply run from the 'isov' directory with the following command:

python exe.py

The fortran program may be run directly by entering the 'bin' directory 
and using the following shell command:

./run 

Alternatively the following shell script will save any console printout:

./run.sh

### Introduction

The ISOV program facilates analysis of the nuclear Equation of State.
Options for computing the isoscalar and isovector properties from a
given input are provided.


Acronyms:

EoS : Equation of State
NM  : Neutron Matter
SNM : Symmetric Nuclear Matter
EPA : Energy per Nucleon 

Abbreviations : 

Den  : Density
Eng  : Energy
Phen : Phenomenolgoical
Sat  : Saturation

### Theory:

The nuclear matter EoS is approximated with the parabolic approximation:

e(rho, alpha) = e0 + esym\*alpha\*alpha

where,

alpha = (rhon-rhop)/(rhon+rhop)

esym(rho) = e1(rho) - e0(rho)

and,

rho = rhon + rhop.

The pressure expression:

P = rho\*rho\*(d e)/(d rho)

The parameters:

Slope Parameter : L = 3.0\*rho_0\*(d e_sym)/(d rho)

Curvature Parameter : K = 9.0\*rho_0\*rho_0\*(d^2 e_sym)/(d^2 rho)

alpha : isospin asymmetry parameter
rho  : hadron den.
rhon : neutron den.
rhop : proton den.
e : EPA
e0 : SNM EPA
e1 : NM EPA

rho_0 : Saturation Den. (0.16 fm^-3)
rho_1 : Reference Den. = 0.1 fm^-3



## Documentation ##

### ISOV - inputs ###

ISOV parameter files:

   -   execpar.don : parameters which govern how the program is executed
   -   readpar.don : parameters which govern how the program reads in the EoS
   -   phenpar.don : parameters which govern the phenomenolgoical EoS input

The input files are examined in detail:



   -   execpar.don

Style : I1  I2
E.g.  : 1   1

Description:

I1 : 'nrun'    ->  [1,2,3] see below for details
I2 : 'nprint'  ->  [ >0 ] see below for details

If nrun = 1
   -   The Isovector and Isoscalar values for the input EoS are generated

       - If 'nprint' = 1, Then E0(rho), E1(rho), Esym(rho) and the pressures
         are printed for 'n' number of density if 'n' > 0 these densities
         corrospond to the densities found in the 'den.don' file, else these
         quantites are printed for 'n0' number of densities corrosponding to
         the densities found in the 'e0_nxlo.don' file. These quantites are
         printed to a file named 'eosvals.don'

       - If 'nprint' = 2, Then the following isoscalar and isovector values
         are printed to a file titled 'isovals.don', according to the
         following order:

          -  n0     :   The number of E0 values
          -  rho0   :   The saturation density
          -  rho1   :   The reference density
          -  rho2   :   Twice saturation density
          -  e0o    :   SNM EoS at saturation density
          -  e01    :   SNM EoS at reference density
          -  e02    :   SNM EoS at twice saturation density
          -  e1o    :   NM EoS at saturation density
          -  e11    :   NM EoS at reference density
          -  e12    :   NM EoS at twice saturation density
          -  esym0  :   Symmetry energy at saturation density
          -  esym1  :   Symmetry energy at reference density
          -  esym2  :   Symmetry energy at twice saturation density
          -  prs0o  :   SNM Pressure at saturation density
          -  prs01  :   SNM Pressure at reference density
          -  prs02  :   SNM Pressure at twice saturation density
          -  prs1o  :   NM Pressure at saturation density
          -  prs11  :   NM Pressure at reference density
          -  prs12  :   NM Pressure at twice saturation density
          -  bigL   :   Slope Parameter
          -  bigK   :   Curvature Parameter
          -  bigKR  :   Curvature at reference density
          -  bigK0  :   SNM Curvature at saturation

If nrun = 2
   -   The parabolic EoS progression is partitioned
       into 'nprint' number of divisions with equal
       incrementing of isospin asymmetry

       - nprint range is [3,]

If nrun = 3
   -   A phenomenolgoical EoS is generated according to input 'phenpar' parameters

If nprint = 0
If nprint = 1
If nprint = 2



   -   readpar.don

Style : I1  I2  I3  I4  I5  I6
E.g.  : 0   1   0   0   10  10

Description:

I1 : 'n_read'    ->  [0,1]  0 is a single file (ex) read, 1 is a two file (e0,e1) read
I2 : 'nkf_read'  ->  [0,1]  reads the first column of EoS file(s) as: 0 - momenta, 1 - density
I3 : 'ndn_read'  ->  [0,1]  reads the first column of 'den.don' file as: 0 - momenta, 1 - density
I3 : 'n'         ->  [>= 0] 0 - no densities read, >0 - number of densities read
I4 : 'n0'        ->  [>= 0] number of SNM values to be read, number of NM values as well if n_read = 0
I5 : 'n1'        ->  [>= 0] number of NM values to be read if n_read = 1.


If n_read = 0

   -   'ex_nxlo.don' : contains n0 entries, formatted as follows:   xval,  e0,  e1

if n_read = 1

   -   'e0_nxlo.don' : contains n0 entries, formatted as follows:   xval,  e0
   -   'e1_nxlo.don' : contains n1 entries, formatted as follows:   xval,  e1

nkf_read determines 'xval':

If nkf_read = 0 : xval is read as fermi momenta (kf) (see conversion below)
If nkf_read = 1 : xval is read as density (fm^-3)

For SNM, e0 : den = 2.0\*xkf\*xkf\*xkf/(3.0\*pi\*pi)
For NM,  e1 : den = xkf\*xkf\*xkf/(3.0\*pi\*pi)

If n > 0 :

   -   'den.don' is read for n entries, formatted as follows:   dval

ndn_read determines 'dval':

If ndn_read = 0 : dval is read as fermi momenta (kf) (see conversion below)
If ndn_read = 1 : dval is read as density (fm^-3)

Note that 'den.don' entries read as momenta are converted to density according to SNM.



   -   phenpar.don

Style : I1  I2  I3  F1   F2    F3
E.g.  : 1   0   0   2.7  220.  0.16

Description:

I1 : 'mic'       ->  [0,1]  0 SNM EoS is phen., 1 SNM EoS is microscopic
I2 : 'isnm'      ->  [0,1]  0 SNM EoS independent of sat., 1 SNM EoS dependent on sat.
I3 : 'isym_emp'  ->  [0,1]  0 for symmetry energy from e0 and e1, 1 for phen symmetry energy
F1 : 'gam'       ->  [>= 0.] Exponent parameter for phenomenolgoical symmetry energy
F2 : 'xk0'       ->  [>= 0.] Symmetry Curvature (K0) float value for sat. dependent phen EoS 
F3 : 'rhosat'    ->  [>= 0.] Saturation Density (rho0) float value for sat. dependent phen EoS 

If mic = 0
   -   The SNM EoS (e0) will be phenomenolgoical, the other inputs in this file determine the parameters
if mic = 1
   -   The SNM EoS (e0) will be microscopic, the other inputs in this file are ignored

If isnm = 0 : The Phenomenolgoical SNM EoS (e0) is parameterized independently from saturation properties
If isnm = 1 : The Phenomenolgoical SNM EoS (e0) is dependent on input saturation properties (rho0 and K0)

If isym_emp = 0 : The symmetry energy is determined from the SNM and NM EoS:   e1(rho) - e0(rho)
If isym_emp = 1 : The symmetry energy is determined from a phen. curve:   esym(rho)

gam : Exponent parameter for phenomenolgoical symmetry energy, typically around 2.7

xk0 : the symmetry curvature (K0), typically around 220 MeV.

rhosat : The saturation density is emperically given by 0.16 fm^-3 and is typically between 0.15 - 0.17 fm^-3