# This code attempts to compile ISOV binaries from their source code
# If Error: syntax error: unexpected end of file: in vim for this file ":set fileformat=unix"  

FILEISO=$PWD/run

COMPILE_ISO="f90 $F90FLAGS -o run -s -w isov.f $LINK_FNL"

if [ -f "$FILEISO" ]
then
    isoexist=$true 
else
    isoexist=$false
fi

if [ !$isoexist ]; then 
    eval $COMPILE_ISO
fi