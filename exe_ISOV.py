import sys

from pmod import benv               # 'benv' is not a standard pmod module and must be added
from pmod import ioparse as iop


def failure_Detection(test, msg):
         
    if(test == False):
        print("[exe] Error: A Fatal error was detected...")
        print("Failure point: "+msg)
        print("The script will perform clean-up and then terminate\n")
        sys.exit()
    else:
        pass 
    return None 
        

benv_inst = benv.benv()
failure_Detection(benv_inst, "Fatal error when initializing benv routine\n")

success = benv_inst.clear_data_folder()
if(success == False):
    print("    [exe] Warning: failure to clear data file\n")
 
benv_data = benv_inst.benv_eos_loop()
failure_Detection(benv_data, "Fatal error when performing benv loop routine\n")

formatted_benv_data = benv_inst.format_benv_data(benv_data, style = 'eos')
failure_Detection(formatted_benv_data, "Fatal error when formatting benv data\n")
par_Strings, val_Strings = formatted_benv_data 


success = iop.flat_file_write('Pars.srt', par_Strings)
if(success == False):
    print("    [exe] Warning: failure to write pars data to 'Pars.srt' file\n")

success = iop.flat_file_write('Vals.srt', val_Strings)
if(success == False):
    print("    [exe] Warning: failure to write vals data to 'Vals.srt' file\n")

success = benv_inst.move_results_to_data_folder()
if(success == False):
    print("    [exe] Warning: failure to move data files to data folder\n")

benv_inst.clean_up()

