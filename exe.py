import sys

from lib import isov
from lib.progLib.pmod import ioparse as iop


'''
This script is the main routine for the ISOV program

Direction:

    programMode : If True, will run the ISOV program in the shell
    benvMode :    If True, will run only the ISOV Loop

'''

programMode = True

isovInst = isov.isov()

if(programMode):
    isovInst.set_isov_menu()
    isovInst.program_loop(isovInst.isov_program_loop, program_name='ISOV')
    isovInst.exit_function("exiting program...", binlogfiles='CONSOLE.txt')
else:
    isovInst.exit_function("exiting program...")
