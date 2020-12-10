import pmod.program_scaffolding.compile as comp

'''
This script faciliates compiling binaries from the source ('src') folder
and moving those binaries to the binary folder ('bin'). This script uses
the scaffolding provided by 'compile.py'
'''

binList = ("run_iso", "run_phn")
srcScript = "compile.sh"
binScript = "run.sh"

success = comp.compileFunc(binList, src_script=srcScript, bin_script=binScript)

print(" ")
if(success):
    print("No fatal errors detected, see above for runtime messesges")
else:
    print("Fatal error detected! See above for runtime error(s)")
print(" ")