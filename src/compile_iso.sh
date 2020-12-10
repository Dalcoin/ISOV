# This code attempts to compile ISOV binaries from their source code
# If Error: syntax error: unexpected end of file: in vim for this file ":set fileformat=unix"  

FILEISO=$PWD/run_iso

COMPILE_ISO="f90 $F90FLAGS -o run_iso -s -w iso_v4.f $LINK_FNL"

if [ -f "$FILEISO" ]
then
    isoexist=$true 
else
    isoexist=$false
fi

if [ !$isoexist ]; then 
    eval $COMPILE_ISO
fi