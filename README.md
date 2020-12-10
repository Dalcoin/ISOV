# ISOV

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

L = 3.0\*rho_0\*(d e_sym)/(d rho)

K = 9.0\*rho_0\*rho_0\*(d^2 e_sym)/(d^2 rho)

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

   -   readpar.don : parameters which govern how the program reads in the EoS
   -   phenpar.don : parameters which govern the phenomenolgoical EoS input
   -   execpar.don : parameters which govern how the program is executed

The input files are examined in detail:



   -   readpar.don

Style : I1  I2  I3  I4  I5
E.g.  : 0   1   0   10  10

Description:

I1 : 'n_read'    ->  [0,1]  0 is a single file (ex) read, 1 is a two file (e0,e1) read
I2 : 'nkf_read'  ->  [0,1]  0 reads the first column as momenta, 1 reads the first column as density
I3 : 'n'         ->  [>= 0] 0 no densities read, >0 number of densities read
I4 : 'n0'        ->  [>= 0] number of SNM values to be read, number of NM values as well if n_read = 0
I5 : 'n1'        ->  [>= 0] number of NM values to be read if n_read = 1.

If n_read = 1

   -   'ex_nxlo.don' : contains n0 entries, formatted as follows:   xval,  e0,  e1

if n_read = 0

   -   'e0_nxlo.don' : contains n0 entries, formatted as follows:   xval,  e0
   -   'e1_nxlo.don' : contains n1 entries, formatted as follows:   xval,  e1

nkf_read determines 'xval':

If nkf_read = 0 : xval is read as fermi momenta (kf) (see conversion below)
If nkf_read = 1 : xval is read as density (fm^-3)

For SNM, e0 : den = 2.0\*xkf\*xkf\*xkf/(3.0\*pi\*pi)
For NM,  e1 : den = xkf\*xkf\*xkf/(3.0\*pi\*pi)

If n > 0 :

   -   'den.don' is read for n entries, formatted as follows:   xval

Note that 'den.don' entries read as momenta are converted to density according to SNM.



   -   phenpar.don

Style : I1  I2  I3  F1    F2
E.g.  : 1   0   0   220.  0.16

Description:

I1 : 'mic'       ->  [0,1]  0 SNM EoS is phen., 1 SNM EoS is microscopic
I2 : 'isnm'      ->  [0,1]  0 SNM EoS independent of sat., 1 SNM EoS dependent on sat.
I3 : 'isym_emp'  ->  [0,1]  0 for symmetry energy from e0 and e1, 1 for phen symmetry energy
F1 : 'xk0'       ->  [>= 0.] Symmetry Curvature (K0) float value for sat. dependent phen EoS 
F2 : 'rhosat'    ->  [>= 0.] Saturation Density (rho0) float value for sat. dependent phen EoS 

If mic = 0
   -   The SNM EoS (e0) will be phenomenolgoical, the other inputs in this file determine the parameters
if mic = 1
   -   The SNM EoS (e0) will be microscopic, the other inputs in this file are ignored

If isnm = 0 : The Phenomenolgoical SNM EoS (e0) is parameterized independently from saturation properties
If isnm = 1 : The Phenomenolgoical SNM EoS (e0) is dependent on input saturation properties (rho0 and K0)

If isym_emp = 0 : The symmetry energy is determined from the SNM and NM EoS:   e1(rho) - e0(rho)
If isym_emp = 1 : The symmetry energy is determined from a phen. curve:   esym(rho)

The symmetry curvature (K0) is typically around 220 MeV.

The saturation density is emperically given by 0.16 fm^-3 and is typically between 0.15 - 0.17 fm^-3



   -   execpar.don

Style : I1  I2  I3
E.g.  : 1   1   1 

Description:

I1 : 'nread'   ->  [1,2,3]   see below for details
I2 : 'nrun'    ->  [1,2,3] see below for details
I3 : 'nprint'  ->  [0,1,2] see below for details

If nread = 0
   -   Fill in!
if nread = 1
   -   The program reads the EoS and density files as dictated by 
if nread != 0,1
   -   The program terminates

If nrun = 1
   -   The Isovector and Isoscalar values for the input EoS are generated (use nread = 1)
If nrun = 2
   -   The parabolic progression 
If nrun = 3

If nprint = 0
If nprint = 1
If nprint = 2