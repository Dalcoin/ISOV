RUN_XEB="./run_iso"
RUN_AUX="./run_phn"

eval $RUN_XEB &>> "CONSOLE.txt"
eval $RUN_AUX &>> "CONSOLE.txt"

exit 0
