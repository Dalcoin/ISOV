# This code attempts to compile ISOV binaries from their source code
# If Error: syntax error: unexpected end of file: in vim for this file ":set fileformat=unix"  

FILEISO=$PWD/run_iso
FILEPHN=$PWD/run_phen

COMPILE_ISO="f90 $F90FLAGS -o run_iso -s -w eos_v4.f ios_v4.f $LINK_FNL"
COMPILE_PHN="f90 $F90FLAGS -o run_phn -s -w eos_v4.f phen_eos.f $LINK_FNL"

if [ -f "$FILEISO" ]
then
    isoexist=$true 
else
    isoexist=$false
fi

if [ !$isoexist ]; then 
    eval $COMPILE_ISO
fi 

if [ -f "$FILEPHN" ]
then
    phnexist=$true 
else
    phnexist=$false
fi

if [ !$phnexist ]; then 
    eval $COMPILE_PHN
fi 

    
