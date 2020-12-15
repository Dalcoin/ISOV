#!/usr/bin/env python

'''

programStructure : 

    - Contains class progStruct (a subclass of 'cmdUtil')

Purpose :

    This file contains the class progStruct which is a 
    part of the programScaffold package. This package
    is meant to facilitate the creation of consistant
    program structure so as to reduce the time required
    for automation of simple shell based programs

File Structure :

    The file structure described in the programScaffold
    package is shown graphically below :

    1) Three folders are required : 'src', 'bin' and 
       'dat', additional directories may be included but
       are not required.

    2) Three files are required : 'compile.py', 'exe.py',
       'option.don'.

    3) 'src' must contain at least two files, at least 
       one source code file, 'source.src', and a shell
       script which facilitates scripting, 'compile.sh'

    4) 'bin' must contain at least two files, at least
       one binary code file, 'binaries', and a shell
       script which exceutes the binaries.

    5) 'dat' is the folder where the end results of
       the program end up.

    6) 'compile_main.py' invokes the 'compile' script
       in 'pmod' to compile the source code in 'src'
       and move the binaries to the 'bin' directory

    7) 'exe.py' executes the binaries in 'bin'

    8) 'option.don' provides options for changing the
       operation of the binaries in 'bin'

    9) 'pmod' is the package which facilitates this
       program structuring and internal operation
 
                    |--- 'src' -|--- 'source.src'
                    |           |
                    |           |--- 'compile.sh'
                    |
'Main' Directory ---|--- 'bin' -|--- 'binaries'
                    |           |
                    |           |--- 'run.sh'
                    |
                    |--- 'dat' -|--- ''
                    |
                    |--- 'lib' -|---'...'
                    |
                    |--- 'compile_main.py'
                    |
                    |--- 'exe.py'
                    |
                    |--- 'option.don'
                    |
                    |--- 'logfile.don'

'''

import sys
import os
import subprocess
import re
import time

from pmod import ioparse as iop 
from pmod import strlist as strl
from pmod.cmdutil import cmdUtil


class progStruct(cmdUtil):

    def __init__(self,
                dir_fold_name='loc',
                src_fold_name='src',
                bin_fold_name='bin',
                dat_fold_name='dat',
                opt_file_name='options.don',
                log_file_name='logfile.don',
                initialize=True,
                osFormat='linux',
                newPath=None,
                rename=False,
                debug=True,
                shellPrint=False,
                colourPrint=True,
                space='    ',
                endline='\n',
                moduleNameOverride="progStruct",
                **kwargs):

        super(progStruct, self).__init__(osFormat,
                                         newPath,
                                         rename,
                                         debug,
                                         shellPrint,
                                         colourPrint,
                                         space,
                                         endline,
                                         moduleNameOverride,
                                         **kwargs)

        kwargs = self.__update_funcNameHeader__("init", **kwargs)

        # File and folder names

        self.DIRNAME = dir_fold_name
        self.DIRPATH = ''

        self.SRCFOLD = src_fold_name
        self.SRCPATH = ''

        self.BINFOLD = bin_fold_name
        self.BINPATH = ''

        self.DATFOLD = dat_fold_name
        self.DATPATH = ''

        self.OPTFILE = opt_file_name
        self.OPTPATH = ''

        self.LOGFILE = log_file_name
        self.LOGPATH = ''

        self.FOLDNAME_LIST = [self.SRCFOLD, self.BINFOLD, self.DATFOLD]
        self.FOLDPATH_LIST = [self.SRCPATH, self.BINPATH, self.DATPATH]
        self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))

        self.FILENAME_LIST = [self.OPTFILE, self.LOGFILE]
        self.FILEPATH_LIST = [self.OPTPATH, self.LOGPATH]
        self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))

        self.DIR_FOLDERS = []
        self.DIR_FILES = []

        self.BIN_DICT = {}

        #-------#----------------#-------#
        # debug #                # debug #
        #-------#----------------#-------#

        self.time_start = time.time()
        self.time_end = 0.0

        # Initialization
        self.INITIALIZATION = False

        # Pathway Errors
        self.DIRPATH_ERROR = False
        self.SRCPATH_ERROR = False
        self.BINPATH_ERROR = False
        self.DATPATH_ERROR = False
        self.OPTPATH_ERROR = False
        self.LOGPATH_ERROR = False

        self.FOLDPATH_ERROR_LIST = [self.SRCPATH_ERROR, self.BINPATH_ERROR, self.DATPATH_ERROR]
        self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))

        self.FILEPATH_ERROR_LIST = [self.OPTPATH_ERROR, self.LOGPATH_ERROR]
        self.FILEPATH_ERROR_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_ERROR_LIST))

        # Set Pathways
        self.DIRPATH_SET = False
        self.SRCPATH_SET = False
        self.BINPATH_SET = False
        self.DATPATH_SET = False
        self.OPTPATH_SET = False
        self.LOGPATH_SET = False

        self.FOLDPATH_SET_LIST = [self.SRCPATH_SET, self.BINPATH_SET, self.DATPATH_SET]
        self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))

        self.FILEPATH_SET_LIST = [self.OPTPATH_SET, self.LOGPATH_SET]
        self.FILEPATH_SET_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_SET_LIST))

        # Intial task errors
        self.INTERNAL_CML_ERROR = False
        self.EXIT_ERROR = False

        self.cycle = 0
        self.option_menu_lines = []

        #initialization (optional)
        if(initialize):
            self.INITIALIZATION = True

            print(" ")
            print("Initialization option detected")
            print("Error messages and test results shown below")
            print("Initialization sequence will now begin...\n")

            proceed = self.init_internal_pathway(**kwargs)

            if(proceed):
                # Checking for folders
                self.src_check(**kwargs)
                self.bin_check(**kwargs)
                self.dat_check(**kwargs)

                # Checking for files
                self.opt_check(**kwargs)
                self.log_check(**kwargs)

            self.assess_initialization()
            self.update_dicts()
            print("Initialization sequence complete.\n")
            if(self.EXIT_ERROR):
                print("A fatal error was detected in the initialization sequence...the program will now terminate:\n")
            else:
                print("Runtime warnings and errors will be printed below: \n")


    #--------------------#----------------#--------------------#
    # Verify Directories #                # Verify Directories #
    #--------------------#----------------#--------------------#

    def init_internal_pathway(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("init_internal_pathway", **kwargs)

        if(isinstance(self.varPath, str) and isinstance(self.varPath_Contains, list)):
            self.DIRPATH = self.varPath
            if(isinstance(self.varPath_Files, list) and isinstance(self.varPath_Folders, list)):
                self.DIR_FOLDERS = self.varPath_Folders 
                self.DIR_FILES = self.varPath_Files
                self.DIRPATH_SET = True
                self.INTERNAL_CML_SET = True
            else:
                self.__err_print__("internal pathway failed to initialize", **kwargs)
                self.INTERNAL_CML_ERROR = True
                self.DIRPATH_ERROR = True
                return False
        else:
            self.__err_print__("internal pathway failed to initialize", **kwargs)
            self.INTERNAL_CML_ERROR = True
            self.DIRPATH_ERROR = True
            return False
        return True

    def src_check(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("src_check", **kwargs)
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.SRCFOLD in self.DIR_FOLDERS):
                self.SRCPATH = self.joinNode(self.DIRPATH,self.SRCFOLD, **kwargs)
                if(self.SRCPATH == False):
                    self.SRCPATH = ''
                    self.SRCPATH_ERROR = True
                    return False
                self.SRCPATH_SET = True
                return True
            else:
                self.SRCPATH_ERROR = True
                return False
        else:
            return False

    def bin_check(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("bin_check", **kwargs)
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.BINFOLD in self.DIR_FOLDERS):
                self.BINPATH = self.joinNode(self.DIRPATH,self.BINFOLD, **kwargs)
                if(self.BINPATH == False):
                    self.BINPATH = ''
                    self.BINPATH_ERROR = True
                    return False
                self.BINPATH_SET = True
                return True
            else:
                self.BINPATH_ERROR = True
                return False
        else:
            return False

    def dat_check(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("dat_check", **kwargs)
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.DATFOLD in self.DIR_FOLDERS):
                self.DATPATH = self.joinNode(self.DIRPATH,self.DATFOLD, **kwargs)
                if(self.DATPATH == False):
                    self.DATPATH = ''
                    self.DATPATH_ERROR = True
                    return False
                self.DATPATH_SET = True
                return True
            else:
                self.BINPATH_ERROR = True
                return False
        else:
            return False

    def opt_check(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("opt_check", **kwargs)
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.OPTFILE in self.DIR_FILES):
                self.OPTPATH = self.joinNode(self.DIRPATH,self.OPTFILE, **kwargs)
                if(self.OPTPATH == False):
                    self.OPTPATH = ''
                    self.OPTPATH_ERROR = True
                    return False
                self.OPTPATH_SET = True
                return True
            else:
                self.OPTPATH_ERROR = True
                return False
        else:
            return False

    def log_check(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("log_check", **kwargs)
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.LOGFILE in self.DIR_FILES):
                self.LOGPATH = self.joinNode(self.DIRPATH, self.LOGFILE, **kwargs)
                if(self.LOGPATH == False):
                    self.LOGPATH = ''
                    self.LOGPATH_ERROR = True
                    return False
                self.LOGPATH_SET = True
                return True
            else:
                self.LOGPATH_ERROR = True
                return False
        else:
            return False


    #--------------------------#----------------#--------------------------#
    # Initialize Main Contents #                # Initialize Main Contents #
    #--------------------------#----------------#--------------------------#


    def update_dicts(self, dict_type='all', **kwargs):

        kwargs = self.__update_funcNameHeader__("update_dicts", **kwargs)

        if(dict_type == 'all'):	    
            self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))
            self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))
            self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_ERROR_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_ERROR_LIST))
            self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_SET_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_SET_LIST))

        elif(dict_type == 'fold'):
            self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))
            self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))

        elif(dict_type == 'file'):
            self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))
            self.FILEPATH_ERROR_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_ERROR_LIST))
            self.FILEPATH_SET_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_SET_LIST))

        elif(dict_type == 'path'):
            self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))
            self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))

        elif(dict_type == 'error'):
            self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_ERROR_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_ERROR_LIST))
            self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_SET_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_SET_LIST))

        else:
            return self.__err_print__("type not recognizned : "+str(type(dict_type)), varID='dict_type', **kwargs)
        return True


    def init_fold_in_main(self, fold_name, auto_check=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("init_fold_in_main", **kwargs)
        if(self.__not_str_print__(fold_name, varID='fold_name', **kwargs)):
            return False

        if(fold_name not in self.FOLDNAME_LIST):
            self.FOLDNAME_LIST.append(fold_name)
        else:
            return False
        self.FOLDPATH_SET_DICT[fold_name] = False
        self.FOLDPATH_ERROR_DICT[fold_name] = False

        if(auto_check):
            return self.fold_check_in_main(fold_name, **kwargs)
        return True


    def init_file_in_main(self, file_name, auto_check=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("init_file_in_main", **kwargs)
        if(self.__not_str_print__(file_name, varID='file_name', **kwargs)):
            return False

        if(file_name not in self.FILENAME_LIST):
            self.FILENAME_LIST.append(file_name)
        else:
            return False
        self.FILEPATH_SET_DICT[file_name] = False
        self.FILEPATH_ERROR_DICT[file_name] = False

        if(auto_check):
            return self.file_check_in_main(file_name, **kwargs)
        return True


    def fold_check_in_main(self, fold_name, **kwargs):

        kwargs = self.__update_funcNameHeader__("fold_check_in_main", **kwargs)
        if(self.__not_str_print__(fold_name, varID='fold_name', **kwargs)):
            return False

        if(not self.INITIALIZATION or self.INTERNAL_CML_ERROR or not self.INTERNAL_CML_SET):
            return self.__err_print__("pathway must be set prior to adding internal directory structure", **kwargs)

        if(fold_name in self.FOLDNAME_LIST):
            self.FOLDPATH_DICT[fold_name] = self.joinNode(self.DIRPATH, fold_name)
            self.FOLDPATH_SET_DICT[fold_name] = True
            self.FOLDPATH_ERROR_DICT[fold_name] = False
            return True
        else:
            self.FOLDPATH_DICT[fold_name] = False
            self.FOLDPATH_SET_DICT[fold_name] = False
            self.FOLDPATH_ERROR_DICT[fold_name] = True
            return False


    def file_check_in_main(self, file_name, **kwargs):

        kwargs = self.__update_funcNameHeader__("file_check_in_main", **kwargs)
        if(self.__not_str_print__(file_name, varID='file_name', **kwargs)):
            return False

        if(not self.INITIALIZATION or self.INTERNAL_CML_ERROR or not self.INTERNAL_CML_SET):
            return self.__err_print__("pathway must be set prior to adding internal file structure", **kwargs)

        if(file_name in self.FILENAME_LIST):
            self.FILEPATH_DICT[file_name] = self.cmv.joinNode(self.DIRPATH,file_name)
            self.FILEPATH_SET_DICT[file_name] = True
            self.FILEPATH_ERROR_DICT[file_name] = False
            return True
        else:
            self.FILEPATH_DICT[file_name] = False
            self.FILEPATH_SET_DICT[file_name] = False
            self.FILEPATH_ERROR_DICT[file_name] = True
            return False


    def init_binary(self, bin_name, **kwargs):
        '''
        Description:

            Add the name of a binary file with the input 'bin_name'
            The binary will be assumed to be in the binary folder ('bin')
            Be sure to include any file extention (e.g. 'run.sh')

        Input(s):

            bin_name : [array of strings, string], corrosponding to the name(s) of the
                       binary file to be added to the binary file dictionary. It is
                       assumed that this file resides within the 'bin' directory

        Output(s):

            success : [bool], True if successful, else False
        '''

        kwargs = self.__update_funcNameHeader__("init_binary", **kwargs)

        if(self.BINPATH_ERROR or not self.BINPATH_SET):
            return self.__err_print__("pathway has not been set", varID=self.BINFOLD, **kwargs)

        if(isinstance(bin_name,(list,tuple))):
            if(self.__not_strarr_print__(bin_name, varID='bin_name', **kwargs)):
                return False
        elif(isinstance(bin_name, str)):
            bin_name = [bin_name]
        else:
            return self.__err_print__("type not recognizned : "+str(type(bin_name)), varID='bin_name', **kwargs)

        not_in_bin = []
        bincontent = self.contentPath(self.BINPATH, **kwargs)
        for bin in bin_name:
            if(bin in bincontent):
                self.BIN_DICT[bin] = self.joinNode(self.BINPATH,bin,**kwargs)
            else:
                not_in_bin.append(bin)
        if(len(not_in_bin) > 0):
            not_in_bin = ["The follow files were not found in '"+self.BINFOLD+"' folder"]+not_in_bin
            self.__err_print__(not_in_bin, heading='Warning', **kwargs)
        return True


    #---------------------------#----------------#---------------------------#
    # Debug and Error Functions #                # Debug and Error Functions #
    #---------------------------#----------------#---------------------------#

    # Self-contained error messages (don't use **kwargs or imprimerTemplate functions)

    def get_run_time(self, type='str'):
        self.time_end = time.time()
        run_time = self.time_end - self.time_start
        if(type == 'float'):
            return float(run_time)
        elif(type == 'int'):
            return int(run_time)
        else:
            return str(round(run_time,3))+" s"

    def exit_function(self, action_msg, failure=False, binlogfiles=None, delete_logfiles=True, signiture=True):
        if(isinstance(binlogfiles, str)):
            self.update_logfile_from_bin(binlogfiles, delete_logfiles, signiture)
        elif(isinstance(binlogfiles, (tuple, list))):
            if(all([isinstance(entry, str) for entry in binlogfiles])):
                self.update_logfile_from_bin(binlogfiles, delete_logfiles, signiture)
        else:
            pass

        if(failure):
            print("ExitError: '"+self.DIRNAME+"' failed "+action_msg)
        else:
            print(action_msg)
        print("Number of runs upon exit :  "+str(self.cycle))
        print("Script run-time :  "+self.get_run_time()+"\n")
        sys.exit()

    def assess_initialization(self):

        err0 = self.INTERNAL_CML_ERROR
        err1 = self.DIRPATH_ERROR
        err2 = self.SRCPATH_ERROR
        err3 = self.BINPATH_ERROR
        err4 = self.DATPATH_ERROR
        err5 = self.OPTPATH_ERROR
        err6 = self.LOGPATH_ERROR

        path0 = self.INTERNAL_CML_SET
        path1 = self.DIRPATH_SET
        path2 = self.SRCPATH_SET
        path3 = self.BINPATH_SET
        path4 = self.DATPATH_SET
        path5 = self.OPTPATH_SET
        path6 = self.LOGPATH_SET

        if(err0):
            print(self.space+"E0 Internal Command Line Test :      Failed")
        else:
            if(path0):
                print(self.space+"E0 Internal Command Line Test :      Succeeded") 
            else:
                print(self.space+"E0 Internal Command Line Test :      ...command line not set")     

        if(err1):
            print(self.space+"E1 Main Directory Path Test :        Failed")
        else:   
            if(path1):         
                print(self.space+"E1 Main Directory Path Test :        Succeeded") 
            else:
                print(self.space+"E1 Main Directory Path Test :        ...path not found")

        if(err2):
            print(self.space+"E2 Source Directory Path Test :      Failed")
        else:
            if(path2):
                print(self.space+"E2 Source Directory Path Test :      Succeeded") 
            else:
                print(self.space+"E2 Source Directory Path Test :      ...path not found")

        if(err3):
            print(self.space+"E3 Binary Directory Pathway Test :   Failed")
        else:
            if(path3):
                print(self.space+"E3 Binary Directory Pathway Test :   Succeeded")
            else:
                print(self.space+"E3 Binary Directory Pathway Test :   ...path not found")

        if(err4):
            print(self.space+"E4 Data Directory Path Test :        Failed")
        else:
            if(path4):
                print(self.space+"E4 Data Directory Path Test :        Succeeded")
            else:
                print(self.space+"E4 Data Directory Path Test :        ...path not found")

        if(err5):
            print(self.space+"E5 Option File Path Test :           Failed")
        else:
            if(path5):
                print(self.space+"E5 Option File Path Test :           Succeeded")
            else:
                print(self.space+"E5 Option File Path Test :           Skipped")

        if(err6):
            print(self.space+"E6 Log File Path Test :              Failed")
        else:
            if(path6):
                print(self.space+"E6 Log File Path Test :              Succeeded")
            else:
                print(self.space+"E6 Log File Path Test :              Skipped")

        print(" ")
        if(any((err0,err1,err2,err3,err4,err5,err6))):
            print(self.space+"Fatal Error Test: Failed\n")
            self.EXIT_ERROR = True
        else:
            print(self.space+"Fatal Error Test: Succeeded\n")

        return True


    #-----------------------#----------------#-----------------------#
    # File/Folder Utilities #                # File/Folder Utilities #
    #-----------------------#----------------#-----------------------#


    def clear_data_folder(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("clear_data_folder", **kwargs)
        if(not self.INTERNAL_CML_SET):
            return self.__err_print__("internal pathway has not yet been initialized", **kwargs)
        if(self.DATPATH_ERROR or not isinstance(self.DATPATH,str) or not self.DATPATH_SET):
            return self.__err_print__("data folder pathway was not set", varID=str(self.DATFOLD), **kwargs)
        return self.clearDir(self.DATFOLD, **kwargs)

    def get_options(self, **kwargs):
        '''
        Reads 'OPTFILE' data from the internal pathway.
        This function should only be called once.
        '''

        if(self.OPTPATH_SET == False or self.OPTPATH_ERROR == True):
            return self.__err_print__("pathway was not properly initialized", varID=self.OPTFILE, **kwargs)

        lines = iop.flat_file_grab(self.OPTPATH, scrub=True, **kwargs)
        return lines

    def get_logs(self, **kwargs):
        '''
        Reads 'OPTFILE' data from the internal pathway.
        This function should only be called once.
        '''

        if(self.LOGPATH_SET == False or self.LOGPATH_ERROR == True):
            return self.__err_print__("pathway was not properly initialized", varID=self.LOGFILE, **kwargs)

        lines = iop.flat_file_grab(self.LOGPATH, scrub=True, **kwargs)
        return lines

    def update_logfile_from_bin(self, binlogfile, delete_logfiles=True, signiture=False, **kwargs):
        if(isinstance(binlogfile, (list,tuple))):
            if(not self.__not_strarr_print__(binlogfile, varID='binlogfile', firstError=True, **kwargs)):
                return False
        elif(isinstance(binlogfile, str)):
            binlogfile = [binlogfile]
        else:
            return self.__err_print__("should be either a string or array of strings", varID='binlogfile', **kwargs)

        loglines = []
        logdict = self.read_files_from_folder(self.BINFOLD, binlogfile, clean=False, failPrint=False, **kwargs)
        if(logdict == False):
            return logdict
        lognames = sorted(list(logdict))

        for logfile in lognames:
            if(signiture):
                loglines+=["'"+logfile+"' content:\n","\n"]
            loglines+=["\n"]
            loglines+=logdict[logfile]
            if(delete_logfiles):
                logfilepath = self.joinNode(self.BINPATH, logfile, **kwargs)
                self.delFile(logfilepath, **kwargs)
        return iop.flat_file_append(self.LOGPATH, loglines, type_test=False, **kwargs)

    #---------------------------#----------------#--------------------------#
    # Executing Programs in BIN #                # Executing Program in BIN #
    #---------------------------#----------------#--------------------------#

    def run_commands(self, commands, **kwargs):

        kwargs = self.__update_funcNameHeader__("run_commands", **kwargs)

        failed_commands = []
        not_commands = []
        success = True

        if(isinstance(commands, (tuple, list))):
            for command in commands:
                if(isinstance(command, str)):
                    try:
                        subprocess.call("./"+command, shell=True)
                    except:
                        failed_commands.append(command)
                else:
                    not_commands.append(str(command))
        elif(isinstance(commands, str)):
            try:
                subprocess.call("./"+commands, shell=True)
            except:
                failed_commands.append(commands)
        else:
            not_commands.append(str(commands))

        if(len(failed_commands)>0):
            self.__err_print__(["The following commands failed to execute:"]+failed_commands, **kwargs)
            success = False

        if(len(not_commands)>0):
            self.__err_print__(["The following commands are not valid, no execution attempted:"]+not_commands, **kwargs)
            success = False

        return success


    def set_osdir(self, pathway=None, **kwargs):

        kwargs = self.__update_funcNameHeader__("set_osdir", **kwargs)

        if(isinstance(pathway, str)):
            pass
        else:
            pathway = self.DIRPATH

        try:
            os.chdir(pathway)
            return True
        except:
            return self.__err_print__(["failure to set os-dir:", str(pathway)], **kwargs)

    #------------------------#----------------#------------------------#
    # Program Loop Functions #                # Program Loop Functions #
    #------------------------#----------------#------------------------#


    def set_option_menu(self, lines, titleBanner=True, **kwargs):
        '''
            Description: Sets the lines to be printed for the program interface
        '''

        kwargs = self.__update_funcNameHeader__("set_option_menu", **kwargs)
        if(isinstance(lines,(list,tuple))):
            if(self.__not_strarr_print__(lines, varID='lines', **kwargs)):
                return False
        elif(isinstance(lines,str)):
            lines = [lines]
        else:
            return self.__err_print__("type not a recognizned : "+str(type(lines)), varID='lines', **kwargs)

        self.option_menu_lines = ['    ']+[self.space+line for line in lines]
        if(titleBanner):
            menu_title = strl.print_border(str(self.DIRNAME)+" menu", 
                                           newln=False,
                                           cushion=1,
                                           indt=4,
                                           **kwargs)
            self.option_menu_lines = menu_title+self.option_menu_lines    
        return True


    def print_option_menu(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("print_option_menu", **kwargs)
        if(self.option_menu_lines != []):
            try:
                print(" ")
                for line in self.option_menu_lines:
                    print(line)
                print(" ")
                return True
            except:
                return self.__err_print__("failure to print menu lines", **kwargs)
        else:
            return self.__err_print__("have not been set", varID='option_menu_lines', **kwargs)


    def input_from_console(self, input_msg, include_space=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("input_from_console", **kwargs)

        if(self.__not_str_print__(input_msg, varID='input_msg', **kwargs)):
            return False

        if(include_space):
            action = raw_input(self.space+input_msg)
        else:
            action = raw_input(input_msg)
        print('    ')

        try:
            formatted_action = strl.str_clean(action.lower())
        except:
            formatted_action = False
        finally:
            if(formatted_action == False or not isinstance(formatted_action, str)):
                self.__err_print__("could not be parsed into a string", varID='action', **kwargs)

        return formatted_action


    def values_from_console(self, input_msg, include_space=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("values_from_console", **kwargs)

        run = True
        value_list = []

        while(run):
            input_str = self.input_from_console(input_msg, include_space, **kwargs)
            if(not isinstance(input_str, str)):
                continue
            value_list = strl.str_to_list(input_str, filtre=True, **kwargs)
            if(not isinstance(input_str, list)):
                continue
            run = False

        return value_list


    def num_from_console(self, input_msg, value_type, free_and_accepted_values=None, include_space=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("num_from_console", **kwargs)

        if(value_type not in ('int', 'float')):
            return self.__err_print__("should be either 'int' or 'float' : '"+str(value_type)+"'", varID='value_type', **kwargs)

        run = True
        val = ''

        if(isinstance(free_and_accepted_values, (float, int, long))):
            free_and_accepted_values = [free_and_accepted_values]

        while(run):
            line = self.input_from_console(input_msg, include_space, **kwargs)
            clean_line = strl.str_clean(line, **kwargs)
            if(clean_line == 'exit' or clean_line == 'quit'):
                break
            try:
                if(value_type == 'int'):
                    val = int(float(clean_line))
                else:
                    val = float(clean_line)
                run = False
            except:
                val = ''
                self.__err_print__("Input could not be parsed into an '"+value_type+"': '"+str(line)+"'")
            if(isinstance(free_and_accepted_values, (list, tuple))):
                if(val not in free_and_accepted_values):
                    self.__err_print__("Input should be one of the following values: "+str(free_and_accepted_values))
                    run = True
                    continue
        return val


    def bool_from_console(self, input_msg, include_space=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("num_from_console", **kwargs)

        run = True
        val = ''

        while(run):
            line = self.input_from_console(input_msg, include_space, **kwargs)
            clean_line = strl.str_clean(line, **kwargs)
            if(clean_line == 'exit' or clean_line == 'quit'):
                break
            if(clean_line.lower() == 'true'):
                val = True
                run = False
            elif(clean_line.lower() == 'false'):
                val = False
                run = False
            else:
                self.__err_print__("Input could not be parsed into a boolean, try again")

        return val



    def program_loop(self, action_function, program_name='Main', binlogfiles=None, **kwargs):
        '''
        Description:

            A simple program loop template

        Input(s):

            action_function : [function], action_function must take one argument (string)
                              which will result in one action being completed. If
                              action_function returns the string 'quit' than the program
                              loop terminates. If action_function returns False, then an
                              error message is printed.

        Output(s):

            success : [bool], True if successfully exited, else False
        '''

        kwargs = self.__update_funcNameHeader__("program_loop", **kwargs)

        run = True

        success = self.print_option_menu()
        if(success == False):
            self.exit_function("failure to actualize option menu")

        while(run):

            formatted_action = self.input_from_console("Input a menu option ('menu' to show the menu): ", **kwargs)

            if(formatted_action == 'quit' or formatted_action == 'exit'):
                print(" ")
                run = False

            if(formatted_action == 'menu' or formatted_action == 'help'):
                self.print_option_menu(**kwargs)

            success = action_function(formatted_action)
            if(not success):
                self.__err_print__("is not a valid command", varID=str(formatted_action), **kwargs)
            continue
        return True
