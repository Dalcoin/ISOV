#!/usr/bin/env python

'''

- This script goes in the PMOD folder

This script faciliates compiling binaries from source files 
within the source folder ('src'), this is accomplished by 
formatting and running a shell script.
and moving those binaries to the binaries folder ('bin').

A graphical example is shown below: this script is run within 'Main'

The input binaries string names are 'aux' and 'xeb_server'

         |-- 'bin'----|---'run.sh'
'Main' --|            |
         |-- 'src'-|  |---'...'  <-------<-------|
                   |                             |
                   |--'aux'     <--------|-->|   |
                   |                     |   |-->|  The script moves the binaries 'aux' and 'xeb_server'
                   |--'xeb_server'   <---|-->|      into the 'bin' folder from the 'src' folder
                   |                     |
                   |--'compile.sh'  -->--| 'compile.sh' creates 'aux' and 'xeb_server'


Info:

    - Change 'linux' to 'windows' for the osFormat variable if running on windows


Inputs:

    bin_list : [string or array of strings], The strings corrospond to the names of the binary files

    SRC_SCRIPT : [string] corrosponds to the name of the script which
                          generates the binaries named in 'bin_list

    BIN_SCRIPT : [string] corrosponds to the name of the script which
                          runs the binary files within the binary directory

    DIR_NAME : [string] ("Main"), corrosponds to the name of the program folder

    osFormat : [string] ("linux"), The OS on which the program is ran

    SRC_NAME : [string] ("src"), The name of the source folder

    BIN_NAME : [string] ("bin"), The name of the binary directory

    SPC : [string] ("    "), Indention spaces for more legable printing


Output:

    Boolean: "True" if success, else "False" if failure.

'''

import sys
import os
import subprocess
import time

from pmod import cmdutil as cmu
from pmod import ioparse as iop
from pmod import strlist as strl



class progComp(cmu.cmdUtil):

    def __init__(self,
                bin_list,
                src_script = "compile.sh",
                bin_script = "run.sh",
                dir_name = "Main",
                src_name = "src",
                bin_name = "bin",
                osFormat='linux',
                newPath=None,
                rename=False,
                debug=True,
                shellPrint=False,
                colourPrint=True,
                space='    ',
                endline='\n',
                moduleNameOverride="compile",
                **kwargs):

        super(progComp, self).__init__(osFormat,
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

        # Internal Variables

        self.failError = False

        self.DIR_NAME    = ""
        self.SRC_NAME    = ""
        self.BIN_NAME    = ""

        self.DIRPATH = ""
        self.SRCPATH = ""
        self.BINPATH = ""

        self.SRC_SCRIPT  = ""
        self.BIN_SCRIPT  = ""

        self.SRC_SCRIPT_PATH  = ""
        self.BIN_SCRIPT_PATH  = ""

        self.SRC_CONTENT = []
        self.BIN_CONTENT = []

        self.move_dict = {}

        # Initialization (Any failure will result in 'failError' being set to True
        # If failError evaluates to True upon initialization, fix the errors before
        # attempting to call the compile function, else fatal errors will likely occur

        if(self.__not_strarr_print__(bin_list, varID='bin_list')):
            self.failError = True
        else:
            self.move_dict = dict([(i,False) for i in bin_list])

        self.input_string_list = {'SRC_SCRIPT':src_script,
                                  'BIN_SCRIPT':bin_script,
                                  'DIR_NAME':dir_name,
                                  'SRC_NAME':src_name,
                                  'BIN_NAME':bin_name}

        for entry in self.input_string_list:
            if(self.__not_str_print__(self.input_string_list[entry], varID=entry, **kwargs)):
                self.failError = True
            else:
                exec("self."+entry+"="+repr(self.input_string_list[entry]))

        if(len(self.varPath_List) > 0 and self.DIR_NAME != '' and isinstance(self.DIR_NAME, str)):
            if(self.varPath_List[-1] != self.DIR_NAME):
                self.__err_print__("this current directory is not the same as the input directory name...", **kwargs)
                self.failError = True
        else:
            self.__err_print__("current directory name could not be resolved", **kwargs)
            self.failError = True

        if(self.SRC_NAME not in self.varPath_Folders):
            self.__err_print__("source folder not found in current directory", varID=self.SRC_NAME, **kwargs)
            self.failError = True
        else:
            self.SRCPATH = self.joinNode(self.varPath, self.SRC_NAME, **kwargs)

        if(self.BIN_NAME not in self.varPath_Folders):
            self.__err_print__("binary folder not found in current directory", varID=self.BIN_NAME, **kwargs)
            self.failError = True
        else:
            self.BINPATH = self.joinNode(self.varPath, self.BIN_NAME, **kwargs)

        if(self.SRCPATH != ''):
            self.SRC_CONTENT = self.contentPath(self.SRCPATH, objType='file', **kwargs)

            if(self.SRC_SCRIPT not in self.SRC_CONTENT):
                self.__err_print__("script file not found in '"+self.SRC_NAME+"' directory", varID=self.SRC_SCRIPT, **kwargs)
                self.failError = True
            else:
                self.SRC_SCRIPT_PATH = self.joinNode(self.SRCPATH, self.SRC_SCRIPT, **kwargs)

        if(self.BINPATH != ''):
            self.BIN_CONTENT = self.contentPath(self.BINPATH, objType='file', **kwargs)

            if(self.BIN_SCRIPT not in self.BIN_CONTENT):
                self.__err_print__("script file not found in '"+self.BIN_NAME+"' directory", varID=self.BIN_SCRIPT, **kwargs)
                self.failError = True
            else:
                self.BIN_SCRIPT_PATH = self.joinNode(self.BINPATH, self.SRC_SCRIPT, **kwargs)


    def compileFunc(self, safety_bool=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("compileFunc", **kwargs)

        if(self.failError or safety_bool):
            return self.__err_print__("was detected; the compile function will now exit...", varID='failError')

        print(" ")
        print("The compiler is now starting...runtime messesges will be printed below:\n")

        # Check for pre-existing binary files and remove any if the exist
        for entry in self.move_dict:
            if(entry in self.BIN_CONTENT):
                errmsg = ["An already existing file is present in the binary folder",
                          "Attempting to overwrite this file : '"+entry+"'"]
                self.__err_print__(errmsg, heading='Warning', parSpace=False, blankLine=False)
                bin_node = self.joinNode(self.BINPATH, entry)
                success = self.delFile(bin_node, **kwargs)
                if(not success):
                    errmsg = ["failure to delete file","newly compiled binary '"+entry+"' may be placed in the '"+DIR_NAME+"' folder"]
                    self.__err_print__(errmsg, parSpace=False, blankLine=False)

        # Ensure that the compiling shell script has UNIX endline characters
        success = self.filesEndlineConvert(self.SRC_SCRIPT, foldName=self.SRC_NAME, **kwargs)
        if(success == False):
            self.__err_print__("not properly formatted: errors may result...", varID=self.SRC_SCRIPT, heading='Warning', parSpace=False) 

        # Check for pre-existing binary files in the source folder (src) and remove any that are found
        for entry in self.move_dict:
            if(entry in self.SRC_CONTENT):
                errmsg = ["An already existing file is present in the binary folder",
                          "Attempting to delete this file : '"+entry+"'"]
                self.__err_print__(errmsg, heading='Warning', parSpace=False, blankLine=False)
                src_node = self.joinNode(self.SRCPATH, entry)
                success = self.delFile(src_node, **kwargs)
                if(not success):
                    errmsg = ["Failure to delete existing file : '"+entry+"'",
                              "Conflict may occur when attempting to recompile this binary file"]
                    self.__err_print__(errmsg, heading='Warning', parSpace=False, blankLine=False)

        # Move system directory to source folder (src)
        try:
            os.chdir(self.SRCPATH)
        except:
            errmsg = ["Failure to set the shell pathway to the source folder",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Change the mode on the shell script to an exceutable
        try:
            subprocess.call("chmod +x "+self.SRC_SCRIPT, shell=True)
        except:
            errmsg = ["Failure to set the shell script to an exceutable",
                      "Shell script name : '"+self.SRC_SCRIPT+"'",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Run the compiling shell script
        try:
            subprocess.call("./"+self.SRC_SCRIPT, shell=True)
        except:
            errmsg = ["Failure to exceute the shell script",
                      "Shell script name : '"+self.SRC_SCRIPT+"'",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Get content of source folder (src) after running compiling script
        self.SRC_CONTENT = self.contentPath(self.SRCPATH, objType='file', **kwargs)

        # Check contents of source folder (src) for binary(ies)
        for entry in self.move_dict:
            if(entry in self.SRC_CONTENT):
                self.__err_print__("binary file, has been found after compiling", varID=entry, heading="Success", parSpace=False)
                self.move_dict[entry] = True
                newpath = self.joinNode(self.SRCPATH, entry)
                if(isinstance(newpath, str)):
                    self.moveObj(newpath, self.BINPATH, **kwargs)
            else:
                self.__err_print__("binary file, was not found upon compilation", varID=entry, heading="Failure", parSpace=False)

        # Ensure that the running shell script has UNIX endline characters
        success = self.filesEndlineConvert(self.BIN_SCRIPT, foldName=self.BIN_NAME, **kwargs)
        if(success == False):
            self.__err_print__("not properly formatted: errors may result...", varID=self.BIN_SCRIPT, heading='Warning',parSpace=False)

        # Move system directory to binary directory (bin)
        try:
            os.chdir(self.BINPATH)
        except:
            errmsg = ["Failure to set the shell pathway back to the program folder",
                      "Program folder name : '"+self.BIN_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Change the mode on the shell script to an exceutable
        try:
            subprocess.call("chmod +x "+self.BIN_SCRIPT,shell=True)
        except:
            errmsg = ["Failure to set the binary script to an exceutable",
                      "Shell script name : '"+self.BIN_SCRIPT+"'",
                      "Binary folder name : '"+self.BIN_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Get content of binary folder (bin) after running compiling script
        self.BIN_CONTENT = self.contentPath(self.BINPATH, objType='file', **kwargs)

        # Move binaries into the binary directory
        bin_fail = False
        mb = 0
        for entry in self.move_dict:
            if(entry in self.BIN_CONTENT):
                self.__err_print__("The '"+entry+"' binary is accounted for in the binary folder", heading="Success", parSpace=False)
            elif(self.move_dict[entry] == False):
                self.__err_print__("The '"+entry+"' binary was not moved into the binary folder", heading="Failure", parSpace=False)
                bin_fail = True
                mb += 1
            else:
                self.__err_print__("The '"+entry+"' binary could not be accounted for", heading="Failure", parSpace=False)
                bin_fail = True
                mb += 1
        if(bin_fail):
            self.__err_print__(str(mb)+" missing binary files...program will not work as intended!", heading="Failure", parSpace=False)
        return True