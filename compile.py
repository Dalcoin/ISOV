from lib.progLib.programCompile import progComp

'''
This script faciliates compiling binaries from the source ('src') folder
and moving those binaries to the binary folder ('bin'). This script uses
the scaffolding provided by 'compile.py'
'''

srcBin = ("run",)
srcRun = "compile.sh"
binRun = "run.sh"

compInst = progComp(srcBin, dir_name='isov')
successfulCompilation = compInst.compileFunc(safety_bool=False)

print(" ")
if(successfulCompilation):
    print("No fatal errors detected, see above for runtime messesges")
else:
    print("Fatal error detected! See above for runtime error(s)")
print(" ")