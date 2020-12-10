import sys

import pmod.isov as isov               # 'isov' is not a standard pmod module and must be added to the 'pmod' folder
import pmod.ioparse as iop


def failure_Detection(test, msg, spc='    '):

    if(isinstance(spc, str)):
        space = spc
    else:
        space = ''

    if(test == False):
        print(space+"[exe] Error: A Fatal error was detected...")
        print(space+"Failure point: "+msg)
        print(space+"The script will perform clean-up and then terminate\n")
        sys.exit()
    else:
        pass
    return None

spc = '    '

isov_inst = isov.isov()
failure_Detection(isov_inst, "Fatal error when initializing ISOV routine\n", spc)

success = isov_inst.clear_data_folder()
if(success == False):
    print(spc+"[exe] Warning: failure to clear data folder and reset internal pathway\n")

isov_run_test = isov_inst.run_isov_loop()
failure_Detection(isov_run_test, "Fatal error when running ISOV program\n", spc)
isov_inst.clean_up()
