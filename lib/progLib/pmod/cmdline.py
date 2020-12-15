#!/usr/bin/env python
'''

0---------0
| Summary |
0---------0

A module containing a class which allows for linux command-line inspired
strings to be passed as commands to a class-function. Options for moving
copying, deleting, creating and modifying files and directories.


Warnings:

    Changes from the previous 'cmdline' module:

        1) 'cmd' spacings are now by spaces instead of the ';' character
        2) object names can no longer contain spaces
        3) 'help' is no longer an internal command, instead use the python help function
        4) 'PathParse' is now a 'imprimerTemplate' subclass
        5) 'cmd' uses regex parsing of the input

0--------------0
| Dependencies |
0--------------0

This module is dependent on the following internal dependencies:

    os     : Retrieving/Resolving/Parsing System Pathways
    shutil : Moving/Coping/Deleting Files and Directories
    re     : regex parsing

This module is dependent on the following PMOD dependencies:

    tcheck  : PathParse is a subclass of 'imprimerTemplate'
    ioparse : used for file reading/writing
    strlist : used for parsing strings and arrays


0-------------0
| Description |
0-------------0

       Consists of 'PathParse', which is a class to call commands within python
    scripts, allowing functionality in the image of Linux command-line inputs.
    Perform manipulations on the location of files and directories from within
    python scripts.

       The main function in the class is 'cmd' : PathParse.cmd(). This
    function allows commands to be passed which, among other things, return the
    contents of the current stored directory string, change the current stored
    directory string, move files between directories and delete files and
    directories. The class allows for pathway information to be stored and
    returned as string objects.

    The most common options are as follows:

        rename : Set to true to ensure that moved files are automatically renamed if
                 the file name conflicts

        shellPrint : prints complete debugging information to the console for each
                     call of the 'cmd' function

0-------------0
| Guidelines: |
0--------------

1) Dundar functions use the internal pathway, non-Dundar functions do not.
2) Functions performing file and pathway manipulations take full pathways.
3) Path functions contain the word 'Path' and modify and manipulate the form of a pathway.
4) Node functions modify and manipulate the nodes within a pathway.
5) Non-Path functions should return a boolean value when their operation does not 
   require a value to be returned (e.g. moving, copying or deleting objects) which is 
   dependent on the success of the operation. 
6) For each Path operation available through the 'cmd' function,
   there should be a corrosponding means of accomplishing the same
   task through non-Dundar function.



Naming Convention: Variables

    * Internal pathways variables start with 'var'
    * Internal non-pathway variables must not start with 'var'

'''

import os
import shutil
import re

from tcheck import imprimerTemplate
import ioparse as iop
import strlist as strl

class PathParse(imprimerTemplate):

    '''
    PathParse(osFormat, newPath=None, debug=False, colourPrint=True)

    -----------
    | Inputs: |
    -----------

    osFormat = 'windows' or 'linux'
    newPath = None (by default), else [string]

        if [None]   : the directory from which the script is run becomes the
                      default .path variable.
        if [string] : the input string becomes the default .path variable

    colourPrint = True [default] :
                  If True, directory variable names are denoted by color when printed


    *Style note: ``Camel'' style names are used for this class
                 The style dictates that first or only words in
                 variable names are all lower-case, all proceeding
                 other words start with a capital letter.

    varPath : corrosponds to the string pointing to the current (path) directory
              *Style note: all addition current (path) pathway information is
              indicated by the addition of and underscore and a descriptive word
              starting with a capital letter (e.g. files in the current (path)
              directory are stored as a list of strings with the variable: varPath_Files)
    '''

    def __init__(self,
                 osFormat,
                 newPath=None,
                 rename=False,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    ',
                 endline='\n',
                 moduleNameOverride=None,
                 **kwargs
                ):

        '''
        --------
        | init |
        --------

        Inputs :

            osFormat    = 'windows' or 'linux'
            newPath     = None    (by default)
            colourPrint = True    (by default)
            space       = '    '  (by default)
            endline     = '\n'    (by default)

        Path :

            .varPath          : A string of the path in which the script is run
            .varPath_List     : A list of strings with values of the directory hiearchy in .path
            .varPath_Head     : A string containing the primary (home) directory
            .varPath_Contains : A list of strings with values of the contents of .path
            .varPath_Files    : A list of strings with values of the files found in the current directory.
            .varPath_Folders  : A list os strings with values of the subdirectories in the current directory.

        Other:

            .varOS      :  A string to specify the operating system, this determines the path file format
            .varCol     :  True for color Escape code when printing, False by default
        '''

        # initilize imprimerTemplate class
        super(PathParse, self).__init__(space, endline, debug, **kwargs)

        # Set debug info for __init__
        if(isinstance(moduleNameOverride, str)):
            self.__set_funcNameHeader__(moduleNameOverride, **kwargs)
        else:
            self.__set_funcNameHeader__("PathParse", **kwargs)
        kwargs = self.__update_funcNameHeader__("init", **kwargs)

        # initilize class variables
        self.SET_INIT_PATH = False
        self.HELP_DICT_INIT = False

        self.cdList = ['ls', 'pwd', 'dir', 'cd', 'chdir', 'mv', 'rm', 'cp',
                       'mkdir','rmdir', 'find', 'match', 'vi']

        self.singleCommandList = ['ls', 'pwd']
        self.singlePathListNoGroup = ['cd', 'chdir', 'vi']
        self.singlePathListGroup = ['rm', 'rmdir', 'mkdir', 'dir', 'find', 'match']
        self.doublePathList = ['mv', 'cp', 'cpdir']

        self.dirNames = ['dir', 'dirs', 'directory', 'directories', 'folder', 'folders']
        self.fileNames = ['file', 'files']

        self.typeList = ['arr','array','list','tup','tuple']
        self.typeStr = ['str','string']

        self.cmdDict = {'pwd'   : 'self.cmd_pwd',
                        'ls'    : 'self.cmd_ls',
                        'dir'   : 'self.cmd_dir',
                        'cd'    : 'self.cmd_cd',
                        'chdir' : 'self.cmd_chdir',
                        'mv'    : 'self.cmd_mv',
                        'rm'    : 'self.cmd_rm',
                        'cp'    : 'self.cmd_cp',
                        'mkdir' : 'self.cmd_mkdir',
                        'rmdir' : 'self.cmd_rmdir',
                        'cpdir' : 'self.cmd_cpdir',
                        'find'  : 'self.cmd_find',
                        'match' : 'self.cmd_match',
                        'vi'    : 'self.cmd_vi'}

        self.rename = rename
        self.varOS = str(osFormat).lower()
        self.shellPrint = shellPrint
        self.varCol = colourPrint

        self.varPath          = None
        self.varPath_List     = None
        self.varPath_Head     = None
        self.varPath_Contains = None
        self.varPath_Files    = None
        self.varPath_Folders  = None

        if(self.varOS in ('windows', 'web', 'net', 'internet')):
            self.delim = '\\'
        elif(self.varOS in ('linux', 'unix')):
            self.delim = '/'
        elif(self.varOS == 'classic'):
            self.delim = ':'
        elif(self.varOS in ('tcl', 'tacl')):
            self.delim = '.'
        else:
            self.__err_print__(": '"+str(self.varOS)+"', is not recognized, setting to default", varID='varOS', heading="Warning", **kwargs)
            self.delim = '/'
            self.SET_INIT_PATH = False

        if(isinstance(newPath, str)):
            self.varPath = newPath
            success = True
        else:
            try:
                self.varPath = os.getcwd()
                success = True
            except:
                self.__err_print__("failure to resolve current pathway", **kwargs)
                self.SET_INIT_PATH = False
                success = False

        if(success):
            updateTest = self.__updatePath__(self.varPath, **kwargs)
            if(updateTest == False):
                self.SET_INIT_PATH = False
            else:
                self.SET_INIT_PATH = True

        if(self.SET_INIT_PATH == False):
            self.__err_print__("initilization failed in part or whole", **kwargs)


    def __cmdInputParse__(self, string, **kwargs):
        '''
        ---------------------
        | __cmdInputParse__ |
        ---------------------

        Description:

            An updated string parsing function. Takes an input string and
            converts it to a cmd tuple. If the string cannot be properly
            parsed, then the tuple, ('',[],''), is returned.

        Input:

            string : a string, formatted for use in the .cmd() function

        output:

            outInst : a tuple formatted for parsing in the .cmd() function
                       takes the form: (cmdInst, [objStrs], destStr)
            cmdInst : a string, corrosponding to a valid cmd command
            objStrs: one or more strings, corrosponding to instances
                        upon which the cmdInst acts
            destStr : a string, corrosponding to a valid destination
                       (used only when applicable)

        '''

        cmd_list = re.findall(r'(\S+)\s*', string)
        
        if(len(cmd_list) < 1):
            self.__err_print__(["could not be parsed into a 'cmd' tuple:", "'string' : '"+string+"'"], varID='string', **kwargs)
            return ('',[],'')

        cmdInst = cmd_list[0].lower()

        if(cmdInst in self.singleCommandList):
            return (cmdInst, [], '')

        elif(cmdInst in self.singlePathListNoGroup):
            if(len(cmd_list) < 2):
                errmsg = ["command must contain an additional target object:", "'string' : '"+string+"'", "'cmd_list' : '"+str(cmd_list)+"'"]
                self.__err_print__(errmsg, varID='cmd_list', **kwargs)
                return ('',[],'')
            tarVal = cmd_list[1]
            if(cmdInst != 'vi'):
                return (cmdInst, [], tarVal)
            else:
                return (cmdInst, [tarVal], '')

        elif(cmdInst in self.singlePathListGroup):
            if(len(cmd_list) < 2):
                errmsg = ["command must contain an additional target object:", "'string' : '"+string+"'", "'cmdInst' : '"+cmdInst+"'"]
                self.__err_print__(errmsg, varID='cmdInst', **kwargs)
                return ('',[],'')
            tarVal = cmd_list[1:]
            return (cmdInst, tarVal, '')

        elif(cmdInst in self.doublePathList):
            if(len(cmd_list) < 3):
                errmsg = ["command must contain an additional target object:", "'string' : '"+string+"'", "'cmdInst' : '"+cmdInst+"'"]
                self.__err_print__(errmsg, varID='cmdInst', **kwargs)
                return ('',[],'')
            tarVal = cmd_list[1:-1]
            destVal = cmd_list[-1]
            return (cmdInst, tarVal, destVal)

        else:
            errmsg = ["not recognized:", "'string' : '"+string+"'", "'cmdInst' : '"+cmdInst+"'"]
            self.__err_print__(errmsg, varID=str(cmdInst), **kwargs)
            return ('',[],'')



#    def __cmdInputParse__(self, string, **kwargs):
#        '''
#        ---------------------
#        | __cmdInputParse__ |
#        ---------------------
#
#        Input:
#
#            string : a string, formatted for use in the .cmd() function
#
#        output:
#
#            outInst : a tuple formatted for parsing in the .cmd() function
#                       takes the form: (cmdInst, [objStrs], destStr)
#            cmdInst : a string, corrosponding to a valid cmd command
#            objStrs: one or more strings, corrosponding to instances
#                        upon which the cmdInst acts
#            destStr : a string, corrosponding to a valid destination
#                       (used only when applicable)
#
#        '''
#
#        def combine_list_str(array, span, ignore=None, space=False):
#
#            out_string = ''
#            count = 0
#            if(ignore != None):
#                for i in array:
#                    if(count not in ignore):
#                        if(space):
#                            if(count < len(array)-len(ignore)-1):
#                                out_string = out_string+i+' '
#                            else:
#                                out_string = out_string+i
#                        else:
#                            out_string = out_string+i
#                    count+=1
#                return out_string
#            else:
#                if(span[1] == 'End' or span[1] == 'end' or span[1] == '' or span[1] == -1):
#                    abridged_list = array[span[0]:]
#                else:
#                    abridged_list = array[span[0]:span[1]]
#
#                count = 0
#                for i in abridged_list:
#                    if(space):
#                        if(count < len(abridged_list)-1):
#                            out_string = out_string+i+' '
#                        else:
#                            out_string = out_string+i
#                    else:
#                        out_string = out_string + i
#                    count += 1
#                return out_string
#
#        # Function Start
#        if(self.__not_str_print__(string, varID="cmd input", **kwargs)):
#            return ('', [], '')
#
#        inputList = filter(lambda entry: entry != '',string.split(" "))
#        cmdInst = inputList[0]
#
#        if(cmdInst in self.singleCommandList):
#            outInst = (cmdInst, [], '')
#            return outInst
#
#        if(cmdInst in self.singlePathListNoGroup):
#            outInst_str = combine_list_str(inputList,[1,'End'],space=True)
#            if(cmdInst != 'vi'):
#                outInst = (cmdInst, [], outInst_str)
#            else:
#                outInst = (cmdInst, [outInst_str], '')
#            return outInst
#
#        if(cmdInst in self.singlePathListGroup):
#            if(';' in string):
#                inst_str = combine_list_str(inputList, [1,'End'], space=True)
#                outInst_list = inst_str.split(';')
#                outInst_list = filter(lambda l: l != '', outInst_list)
#                outInst = (cmdInst, outInst_list, '')
#                return outInst
#            else:
#                outInst_str = combine_list_str(inputList, [1,'End'], space=True)
#                outInst = (cmdInst, [outInst_str], '')
#                return outInst
#
#        if(cmdInst in self.doublePathList):
#            if(';' in string):
#                dest_list = []
#                while(';' not in inputList[-1]):
#                    dest_list.append(inputList.pop(-1))
#                dest_list = dest_list[::-1]
#                destStr = combine_list_str(dest_list, [0,'End'], space=True)
#                inst_str = combine_list_str(inputList, [1,'End'], space=True)
#                outInst_list = inst_str.split(';')
#                outInst_list = filter(lambda l: l != '', outInst_list)
#                outInst = (cmdInst, outInst_list, destStr)
#                return outInst
#            else:
#                if(len(inputList) == 3):
#                    outInst = (cmdInst, [inputList[1]], inputList[2])
#                elif('.' in string):
#                    dest_list = []
#                    while('.' not in inputList[-1]):
#                        dest_list.append(inputList.pop(-1))
#                    print(inputList)
#                    dest_list = dest_list[::-1]
#                    destStr = combine_list_str(dest_list,[0,'End'], space=True)
#                    inst_str = combine_list_str(inputList,[1,'End'], space=True)
#                    outInst = (cmdInst, [inst_str], destStr)
#                else:
#                    errarray = ["The input spaceing or object style created ambiguity for the indexer:"]
#                    errarray.append("'"+string+"'")
#                    __err_print__(errarray, **kwargs)
#                    outInst = (cmdInst, [], '')
#
#                return outInst
#
#        self.__err_print__("not recognized, use 'help' to view available functions", varID=str(cmdInst), **kwargs)
#        return ('',[],'')


    def joinNode(self, oldPath, newNode, **kwargs):
        '''
        Description: Adds a new node onto a string Pathway

        Input :

            oldPath : [string], pathway formatted string
            newPath : [string], node

        Output : [string], pathway formatted string
        '''

        kwargs = self.__update_funcNameHeader__("joinNode", **kwargs)
        if(self.__not_str_print__(oldPath, varID='oldPath', **kwargs)):
            return False
        if(self.__not_str_print__(newNode, varID='newNode', **kwargs)):
            return False
        if(self.__not_str_print__(self.delim, varID='delim', **kwargs)):
            return self.__err_print__("The internal delimiter needs to be set to a string value", **kwargs)

        newPath = oldPath+self.delim+newNode
        return newPath


    def Arr2Str(self, inPath, **kwargs):
        '''
        Convert pathway, 'inPath', from array format to string format
        '''

        kwargs = self.__update_funcNameHeader__("Arr2Str", **kwargs)

        if(self.__not_arr_print__(inPath, varID='inPath', **kwargs)):
            return False
        else:
            inPath = filter(None, inPath)
            if(len(inPath) < 1):
                return self.__err_print__("must contain at least one pathway entry", varID='inPath', **kwargs)

        for i,node in enumerate(inPath):
            if(i == 0):
                outPath = str(node)
                if(self.varOS == 'linux'):
                    outPath = '/'+outPath
            else:
                outPath = self.joinNode(outPath, str(node), **kwargs)
                if(outPath == False):
                    errmsg = "could not join the"+strl.print_ordinal(i+1)+" entry"
                    return self.__err_print__(errmsg, varID='inPath', **kwargs)

        if(self.varOS == 'windows' and len(inPath)==1):
            outPath = outPath+"\\"

        return outPath


    def Str2Arr(self, inPath, **kwargs):
        '''
        Convert pathway, 'inPath', from string format to array format
        '''

        kwargs = self.__update_funcNameHeader__("Str2Arr", **kwargs)

        if(self.__not_str_print__(inPath, varID='inPath', **kwargs)):
            return False
        else:
            try:
                return filter(None, inPath.split(self.delim))
            except:
                return self.__err_print__("could not be converted to a pathway list", varID='inPath', **kwargs)


    def convertPath(self, inPath, outType='str', **kwargs):
        '''
        --------------
        | convertPath |  :  Convert Pathway
        --------------

        description : converts between list formatted pathways and str formatted pathways

        Inputs :

            inPath : a pathway (formatted as either a string or array)
            outType : [string] (Default value : 'str'), corrosponding to a python data-type

        Output : Path formatted list or string
        '''

        kwargs = self.__update_funcNameHeader__("convertPath", **kwargs)

        if(self.__not_str_print__(outType, varID='outType', **kwargs)):
            return False
        else:
            outType = outType.lower()

        if(isinstance(inPath, (list, tuple))):
            if(outType in self.typeList):
                if(outType == 'arr' or outType == 'array'):
                    return inPath
                elif(outType == 'list'):
                    return list(inPath)
                else:
                    return tuple(inPath)
            elif(outType in self.typeStr):
                return self.Arr2Str(inPath, **kwargs)
            else:
                return self.__err_print__("not recognized", varID='outType', **kwargs)
        elif(isinstance(inPath, str)):
            if(outType in self.typeStr):
                return inPath
            elif(outType in self.typeList):
                if(outType == 'arr' or outType == 'array' or outType == 'list'):
                    return self.Str2Arr(inPath, **kwargs)
                else:
                    return tuple(self.Str2Arr(inPath, **kwargs))
            else:
                return self.__err_print__("not recognized", varID='outType', **kwargs)
        else:
            return self.__err_print__("not of a recognized type, should be a 'Str' or an 'Array'", varID='inPath', **kwargs)
        return self.__err_print__("path conversion failed", **kwargs)


    def contentPath(self, inPath, objType='all', fileStyle=None, **kwargs):
        '''
        ---------------
        | contentPath |
        ---------------

        Description: Returns a list of strings corrosponding to the contents of
                     the an input path's directory. Option for selecting only a
                     specific object (folder, file or file extension). 

        Input:

            'inPath'   : A Pathway; may be in either string or array format.

            'objType'  : Type of object, may be 'all', 'file' or 'folder'. Note
                         that 'objType' takes precedent over 'fileStyle'.

            'fileStyle': [string], (None), A string corrosponding to a file extension
                                           type. Note that 'objType' must be set to 'file'
                                           for 'fileStyle' to take effect.

        Return:

            'output': [list], A list of strings corrosponding to all the files
                              in the current (path) directory matching the
                              'fileStyle' extension, if 'fileStyle' == None, then all
                              file names are included in 'file_list'.
        '''

        kwargs = self.__update_funcNameHeader__("contentPath", **kwargs)

        if(isinstance(inPath, str)):
            path = inPath
        elif(isinstance(inPath, (list,tuple))):
            path = self.Arr2Str(inPath, **kwargs)
            if(path == False):
                return False
        else:
            return self.__err_print__("must be either an 'Array' or 'Str' type : "+str(type(inPath)), varID='inpath', **kwargs)

        if(os.path.isdir(path) == False):
            errmsg = ["does not corrospond to a directory", "Pathway : "+str(path)]
            return self.__err_print__(errmsg, varID = 'inPath', **kwargs)

        if(self.__not_str_print__(objType, varID='objType', heading='Warning', **kwargs)):
            self.__err_print__("will be defaulted to a value of : 'all'", varID='objType', heading='Warning', **kwargs)
            objType = 'all'
        else:
            objType = objType.lower()

        try:
            pathContents = os.listdir(path)
        except:
            return self.__err_print__(["content is irretrievable","pathway: "+path], varID='inPath' **kwargs)

        if(objType.lower() == 'all'):
            output = pathContents
        elif(objType.lower() in self.fileNames):
            if(fileStyle == None or not isinstance(fileStyle,(str,tuple,list))):
                output = [entry for entry in pathContents if os.path.isfile(self.joinNode(path, entry, **kwargs))]
            else:
                file_List = []
                if(isinstance(fileStyle, str)):
                    fileType = '.'+fileStyle
                    for entry in pathContents:
                        if(fileType in entry):
                            file_List.append(entry)
                    output = file_List
                else:
                    for ending in fileStyle:
                        fileType = '.'+str(ending)
                        for entry in pathContents:
                            if(fileType in entry):
                                file_List.append(entry)
                    output = file_List
        elif(objType.lower() in self.dirNames):
            output = [entry for entry in pathContents if os.path.isdir(self.joinNode(path, entry, **kwargs))]
        else:
            output = False

        return output


    def __updatePath__(self, newPath, **kwargs):
        '''
        ------------------
        | __updatePath__ |
        ------------------

        Description: Formats a path-formatted list into a path-formatted string,
                     the new path then replaces the old path directory along with
                     replacing the old path variables with those of the new path.

        Input:

            'newPath': [list,tuple], A path-formatted list

        Output : [Bool], success
        '''
        kwargs = self.__update_funcNameHeader__("__updatePath__", **kwargs)

        if(isinstance(newPath, str)):
            if(newPath == ''):
                return self.__err_print__("is an empty string", varID='newPath', **kwargs)
            if(os.path.isdir(newPath)):
                self.varPath = newPath
            else:
                errmsg = ["does not corrospond to a valid directory pathway", "'newPath' : "+str(newPath)]
                return self.__err_print__(errmsg, varID='newPath', **kwargs)
            __oldval__ = self.varPath_List
            self.varPath_List = self.Str2Arr(newPath, **kwargs)
            if(self.varPath_List == False):
                self.varPath_List = __oldval__
                return self.__err_print__("failed to be updated", varID='varPath_List', **kwargs)
        elif(isinstance(newPath, (list,tuple))):
            if(len(newPath) < 1):
                return self.__err_print__("is an empty array", varID='newPath', **kwargs)

            __oldval__ = self.varPath
            self.varPath = self.Arr2Str(newPath, **kwargs)
            if(self.varPath == False):
                self.varPath = __oldval__
                return self.__err_print__("failed to be updated", varID='varPath', **kwargs)

            if(os.path.isdir(self.varPath)):
                self.varPath_List = list(newPath)
            else:
                self.varPath = __oldval__
                errmsg = ["does not corrospond to a valid directory pathway", "'newPath' : "+str(newPath)]
                return self.__err_print__(errmsg, varID='newPath', **kwargs)
        else:
            return self.__err_print__("not a recognized type", varID='newPath', **kwargs)

        self.varPath_Head = self.varPath_List[0]
        if(self.varOS == 'windows'):
            self.varPath_Head = self.varPath_Head+"\\"
        self.varPath_Dir  = self.varPath_List[-1]

        self.varPath_Contains = self.contentPath(self.varPath, 'all', **kwargs)
        if(self.varPath_Contains == False):
            self.varPath_Contains = None
            self.varPath_Files = None
            self.varPath_Folders = None
            return self.__err_print__("failure to get contents from current pathway", **kwargs)

        self.varPath_Files = self.contentPath(self.varPath, 'files', **kwargs)
        if(self.varPath_Files == False):
            self.varPath_Files = None
            self.varPath_Folders = None
            return self.__err_print__("failure to get files and directories from current pathway")

        self.varPath_Folders = self.contentPath(self.varPath, 'folders', **kwargs)
        if(self.varPath_Folders == False):
            self.varPath_Folders = None
            return self.__err_print__("failure to get directories from current pathway", **kwargs)

        return True


    def uniqueName(self, destPath, objName, uniqueNameLimit=500, **kwargs):
        '''
        Description: 

        Inputs: 

            destPath : [string], [array],
                       A pathway formatted string or array which points to a directory

            objName  : [string]
                       A string corrosponding to an object,
                       The string will be checked against
                       the names of objects in the destPath
                       directory, if there is overlap the
                       a indexer number will be added until
                       there is no overlap or index limit
                       number is exceeded.

        output: A string if no error is detected, else False
        '''

        kwargs = self.__update_funcNameHeader__("uniqueName", **kwargs)

        contents = self.contentPath(destPath, **kwargs)
        if(contents == False):
            return self.__err_print__("must be a valid directory pathway", varID='destPath', **kwargs)

        nameList = strl.str_to_list(objName, spc='.', **kwargs)
        if(nameList == False):
            return self.__err_print__("was not properly parsed", varID='objName', **kwargs)

        name = ''

        # Checks if there is a file ending on 'objName', if there isn't one unique name is determined
        if(len(nameList) > 1):
            pass
        elif(len(nameList) == 1):
            name = nameList[0]
            if(len(name) > 0):
                count = 1
                outName = name
                while(outName in contents):
                    if(count > uniqueNameLimit):
                        return self.__err_print__("name ID overflow; too many files with the same name ID", **kwargs)                   
                    outName = name+"_"+str(count)
                    count += 1
                return outName
            else:
                return self.__err_print__("is empty; should be string corrosponding to new object name", varID='objName', **kwargs)
        else:
            return self.__err_print__("is empty; should be string corrosponding to the new object name", varID='objName', **kwargs)

        # If there is a file ending attached to 'objName', the unique name is generated
        count = 1
        name = objName
        pad = nameList[-2]
        while(name in contents):
            if(count > uniqueNameLimit):
                return self.__err_print__("name ID overflow; too many files with the same name ID", **kwargs)
            nameList[-2] = pad+"_"+str(count)
            name = strl.array_to_str(nameList, spc='.', **kwargs)
            count+=1
        return name


    def delNode(self, oldPath, nodeID=None, **kwargs):
        '''
        Description: deletes node from a pathway, starting at the end

        Input :

            oldPath : [string], pathway formatted string
            nodeID  : [None or Int], nodes to be deleted from end

        Output : [string], pathway formatted string
        '''

        kwargs = self.__update_funcNameHeader__("delNode", **kwargs)

        oldPath = self.convertPath(oldPath, outType="list", **kwargs)
        if(oldPath == False):
            return False

        n = len(oldPath)

        if(n < 1):
            return self.__err_print__("contains an empty pathway", varID='oldPath', **kwargs)
        elif(n == 1):
            self.__err_print__("home directory reached, cannot delete home node", heading='warning', **kwargs)
            return self.convertPath(oldPath, **kwargs)
        else:
            pass

        if(nodeID == -1 or nodeID == None):
            newPath = oldPath[:-1]
            strPath = self.Arr2Str(newPath, **kwargs)
            return strPath
        elif(isinstance(nodeID, int)):
            try:
                if(nodeID != 0):
                    newPath = oldPath[:nodeID]
                else:
                    newPath = oldPath
                strPath = self.Arr2Str(newPath, **kwargs)
            except:
                strPath = self.__err_print__("is out of range", varID='nodeID', **kwargs)
            return strPath
        else:
            return self.__err_print__("is not recognized", varID='nodeID', **kwargs)
        return False


    def getNode(self, inPath, nodeID=None, **kwargs):

        kwargs = self.__update_funcNameHeader__("getNode", **kwargs)

        pathList = self.convertPath(inPath, outType='list')
        if(pathList == False):
            return False

        if(nodeID == None or nodeID == -1):
            if(len(pathList) > 0):
                return pathList[-1]
            else:
                return self.__err_print__("does not contain a valid pathway", varID='inPath', **kwargs)
        elif(isinstance(nodeID, int)):
            try:
                nodeValue = pathList[nodeID]
                return nodeValue
            except:
                return self.__err_print__("is out of range", varID='nodeID', **kwargs)
        else:
            return self.__err_print__("is not recognized: '"+str(nodeID)+"'", varID='nodeID', **kwargs)
        return False


    def climbPath(self, oldpath, node, **kwargs):
        '''
        Description : if 'node' is a node in the default (current) pathway
                      that the default (current) pathway directory is moved
                      up to that node, else False is returned

        Input:

            'node' : [string], corrosponding to a node within the current pathway

        The overhead and updating of class path info is taken care of with this function
        '''

        kwargs = self.__update_funcNameHeader__("climbPath", **kwargs)

        if(isinstance(oldpath, str)):
            path = self.convertPath(oldpath, outType='list', **kwargs)
            if(path == False):
                return self.__err_print__(["failed to convert to a list", "pathway : '"+oldpath+"'"], varID='oldpath', **kwargs)
        elif(isinstance(oldpath, (list, tuple))):
            path = list(oldpath)
        else:
            return self.__err_print__("must be a path string or path array", varID='oldPath', **kwargs)

        newPath_List = []
        if(node in path):
            for entry in path:
                if(entry != node):
                    newPath_List.append(entry)
                else:
                    break
            newPath_List.append(node)
            return newPath_List
        else:
            return self.__err_print__(["not found in pathway hierarchy '", "pathway : "+str(oldpath), "node : "+str(node)], varID='node', **kwargs)


    def __climbPath__(self, node, **kwargs):
        '''
        Description : if 'node' is a node in the default (current) pathway
                      that the default (current) pathway directory is moved to

        Input:

            'node' : [string], corrosponding to a node within the current pathway

        The overhead and updating of class path info is taken care of with this function
        '''

        newPath_List = self.climbPath(self.varPath_List, node, **kwargs)
        if(newPath_List == False):
            return False

        output = self.__updatePath__(newPath_List, **kwargs)
        return output


    def renamePath(self, originPath, destPath, objName=None, climbPath_Opt=True, **kwargs):
        '''
        Description : Takes an input pathway and an destination pathway along 
                      options for the object's name and climbing pathway if
                      destination path terminates with a non-folder object.

                      The final node of the input pathway determines the original
                      name of the object. If 'objName' is a string then the new
                      path of the object will replace the object's original name

        Usage: This function is useful when working with the pathways of objects
               to be moved or copied between directories; ensures that the no
               error will occured due to duplicated file names

        Input :

            originPath : [string], A complete object pathway, the final node may be either a file or directory
            destPath   : [string], A directory pathway for the destination, the final node must be a directory
            objName    : [string] (None), If a string, this string will be the final node in 'newPath' output
            climbPath_Opt  : [bool] (False), If true then if 'destPath' does have a directory as the final node,
                                         the node will be climbed unitil a directory is found or the home
                                         directory is reached

        Output : [Bool], success
        '''

        def __create_path__(novPath, novName, **kwargs):

            dNode = self.uniqueName(novPath, novName, **kwargs)
            if(dNode == False):
                return self.__err_print__("Failure to generate a unique name from input path", **kwargs)
            return self.joinNode(novPath, dNode, **kwargs)

        kwargs = self.__update_funcNameHeader__("renamePath", **kwargs)

        destNode = self.getNode(originPath, **kwargs)
        originPath = self.convertPath(originPath, **kwargs)
        destPath = self.convertPath(destPath, **kwargs)

        if(destNode == False):
            return self.__err_print__("failed to yield terminating node", varID='originPath', **kwargs)

        # If the objName variable is changed to a string
        if(isinstance(objName,str)):
            if(os.path.isdir(destPath)):
                pass
            else:
                errmsg = ["does not point to a directory"]
                errmsg.append("If 'objName' is set, then the 'destPath' pathway must point to a directory")
                errmsg.append("'destPath' : "+str(destPath))
                return self.__err_print__(errmsg, varID='destPath', **kwargs)
            newPath = __create_path__(destPath, objName, **kwargs)
            if(newPath == False):
                self.__err_print__("new pathway could not be established", **kwargs)
            return newPath

        # Default method: will attempt to establish a unique pathway
        else:
            if(os.path.isdir(destPath)):
                newPath = __create_path__(destPath, destNode, **kwargs)
                if(newPath == False):
                    self.__err_print__("new pathway could not be established", **kwargs)
                return newPath

            # climbPath_Opt ----option----
            if(climbPath_Opt):
                parentPath = self.delNode(destPath, **kwargs)
                while(self.convertPath(parentPath, **kwargs) != self.varPath_Head):
                    if(parentPath == False):
                        return self.__err_print__("pathway could not be climbed", varID='destPath', **kwargs)
                    if(os.path.isdir(parentPath)):
                        destNode = self.uniqueName(parentPath, destNode, **kwargs)
                        newPath = self.joinNode(parentPath, destNode, **kwargs)
                        if(newPath == False):
                            return self.__err_print__("could not accept directory name node", varID='destPath', **kwargs)
                        return newPath
                    else:
                        return self.__err_print__(["is not a valid destination pathway", "'destPath': "+str(destPath)], varID='destPath', **kwargs)
                    parentPath = self.delNode(parentPath)
                self.__err_print__("couldn't find valid destination before reaching the 'home' directory", **kwargs)
            self.__err_print__("is not a valid pathway destination", varID='destPath', **kwargs)
        return False


    ###########################################################
    # Move File and Directories from one Directory to another #
    ###########################################################

    def moveObj(self, objPath, destPath, objName=None, renameOverride=None, **kwargs):
        '''
        Description : Moves and renames file and directory objects

        Input :

            objPath  : [string] [array], 
                       A complete object pathway, either string or array. 
                       The final node may be either a file or directory.

            destPath : [string] [array], 
                       A complete directory pathway, either string or array.
                       The final node must be a directory.

            objName  : [string] [None by default], 
                       If a string, then the object will be renamed to the string.

            renameOverride : [Bool] [None by default], 
                             If a boolean then will override the 'self.rename' option.

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("moveObj", **kwargs)

        #Parse object pathway into the string format
        if(isinstance(objPath, (list,tuple))):
            objPath = self.convertPath(objPath, **kwargs)
            if(objPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID='objPath', **kwargs)
        elif(isinstance(objPath, str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='objPath', **kwargs)

        #Parse destination pathway into the string format
        if(isinstance(destPath, (list,tuple))):
            destPath = self.convertPath(destPath, **kwargs)
            if(destPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID='destPath', **kwargs)
        elif(isinstance(destPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='destPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(objPath, destPath, objName=objName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(objName,str)):
                destPath = self.joinNode(destPath, objName, **kwargs)
            else:
                destPath = destPath

        #Move contents of 'objPath' to the 'destPath' destination
        try:
            shutil.move(objPath, destPath)
            success = True
        except:
            errmsg = ["object could not be moved:", "File pathway: "+str(objPath), "Destination pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, **kwargs)

        return success


    def __moveObj__(self, objPath, newPath, objName=None, renameOverride=None, **kwargs):

        success = self.moveObj(objPath, newPath, objName=objName, renameOverride=renameOverride, **kwargs)
        if(not success):
            return self.__err_print__("failure to perform move operation", **kwargs)

        try:
            startDir = self.convertPath(objPath, "list", **kwargs)[-2]
        except:
            return self.__err_print__("failure to parse object folder from 'objPath'", **kwargs)

        try:
            finalDir = self.convertPath(newPath,"list")[-1]
        except:
            return self.__err_print__("failure to find folder for the new pathway", **kwargs)

        if(startDir == self.varPath_Dir or finalDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                self.__err_print__("failure to update pathway", **kwargs)
        else:
            success = False
        return success


    ############################
    # Delete File from Pathway #
    ############################

    def delFile(self, delPath, **kwargs):
        '''
        Description : Attempts to delete the content at the location of the input pathway

        Input:

            delPath : A complete pathway string pointing to a file

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("delFile", **kwargs)

        if(isinstance(delPath, (list,tuple))):
            delPath = self.convertPath(delPath, **kwargs)
            if(delPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'delPath', **kwargs)
        elif(isinstance(delPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='delPath', **kwargs)

        if(os.path.isfile(delPath)):
            pass
        else:
            errmsg = ["is not a file pathway", "Pathway: "+str(delPath)]
            return self.__err_print__(errmsg, varID='delPath', **kwargs)

        try:
            os.remove(delPath)
        except:
            errmsg = ["Failure to delete file", "File pathway: "+str(delPath)]
            return self.__err_print__(errmsg, **kwargs)
        return True


    def __delFile__(self, delPath, **kwargs):

        success = self.delFile(delPath, **kwargs)
        if(not success):
            return self.__err_print__(["failure to perform file delete operation"], **kwargs)

        try:
            startDir = self.convertPath(delPath, "list", **kwargs)[-2]
        except:
            return self.__err_print__("failure to find the folder containing the object in 'delPath' pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return False

    #############################################
    # Copy object from one directory to another #
    #############################################

    def copyFile(self, filePath, destPath, objName=None, renameOverride=None, **kwargs):
        '''
        Description : Attempts to copy a file from the 'filePath' full pathway
                      to the full directory pathway 'destPath', with a name
                      given by 'objName'

        Input :

            filePath : [string] corrosponds to full pathway of the location of the file to be copied
            destPath : [string], corrosponds to the pathway of the copied file
            objName  : [string] (Default : None), corrosponds to full pathway of the location of the copy             

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("copyFile", **kwargs)

        if(isinstance(filePath,(list,tuple))):
            filePath = self.convertPath(filePath, **kwargs)
            if(filePath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'filePath', **kwargs)
        elif(isinstance(filePath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='filePath', **kwargs)

        if(isinstance(destPath,(list,tuple))):
            destPath = self.convertPath(destPath, **kwargs)
            if(destPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'destPath', **kwargs)
        elif(isinstance(destPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='destPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(filePath, destPath, objName=objName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(objName, str)):
                destPath = self.joinNode(destPath, objName, **kwargs)
            else:
                destPath = destPath

        try:
            shutil.copyfile(filePath, destPath)
            success = True
        except:
            errmsg = ["file could not be copied", "File pathway: "+str(filePath), "Destination pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, **kwargs)
        return success


    def __copyFile__(self, objPath, newPath, objName=None, renameOverride=None, **kwargs):

        success = self.copyFile(objPath, newPath, objName, renameOverride, **kwargs)
        if(not success):
            return self.__err_print__("failure to perform copy operation", **kwargs)

        try:
            if(isinstance(objName, str)):
                startDir = self.convertPath(objPath, "list")[-1]
            else:
                startDir = self.convertPath(objPath, "list")[-2]
        except:
            return self.__err_print__("failure to find folder for object pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return False


    ######################
    # Make new directory #
    ######################
 
    def makeDir(self, dirPath, dirName=None, renameOverride=None, **kwargs):
        '''
        Description : Attempts to create a folder at the full pathway string, 'dirPath'.
                      If 'dirName' is a a string, then this string will be appended onto
                      the pathway and used as the new folder name

        Input :

            dirPath : [string] corrosponds to full pathway of the location of the file to be copied
            fileName  : [string] (Default : None), corrosponds to full pathway of the location of the copy

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("makeDir", **kwargs)

        if(isinstance(dirPath,(list,tuple))):
            dirPath = self.convertPath(dirPath, **kwargs)
            if(dirPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'dirPath', **kwargs)
        elif(isinstance(dirPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='dirPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(dirPath, dirName, objName=dirName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(dirName, str)):
                destPath = self.joinNode(dirPath, dirName, **kwargs)
            else:
                destPath = dirPath

        try:
            os.mkdir(destPath)
            success = True
        except:
            errmsg = ["directory could not be created", "Directory pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, **kwargs)
        return success


    def __makeDir__(self, dirPath, dirName=None, renameOverride=None, **kwargs):

        success = self.makeDir(self, dirPath, dirName, renameOverride, **kwargs)
        if(not success):
            return self.__err_print__("failure to perform move operation")

        try:
            if(isinstance(dirName,str)):
                newDir = dirName
            else:
                newDir = self.convertPath(dirPath,"list")[-2]
        except:
            return self.__err_print__("failure to find new pathway directory")

        if(newDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return True


    ##############################
    # Delete directory from path #
    ##############################

    def delDir(self, delPath, **kwargs):
        '''
        Description : Recursively removes content and directory at pathway 'delPath'

        Input : 

            delPath : [string], corrosponds to path containing directory to be deleted

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("delDir", **kwargs)

        if(isinstance(delPath, (list,tuple))):
            delPath = self.convertPath(delPath, **kwargs)
            if(delPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'delPath', **kwargs)
        elif(isinstance(delPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='delPath', **kwargs)

        if(os.path.isdir(delPath)):
            pass
        else:
            errmsg = ["is not a directory pathway", "pathway: "+str(delPath)]
            return self.__err_print__(errmsg, varID='delPath', **kwargs)

        try:
            shutil.rmtree(delPath)
            success = True
        except:
            errmsg = ["directory could not be deleted", "pathway: "+str(delPath)]
            success = self.__err_print__(errmsg, varID='delPath', **kwargs)
        return success


    def __delDir__(self, delPath, **kwargs):

        success = self.delFile(delPath, **kwargs)
        if(not success):
            return self.__err_print__("failure to perform delete operation", **kwargs)

        try:
            startDir = self.convertPath(delPath,"list")[-2]
        except:
            return self.__err_print__("failure to find folder for object pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return True


    ##########################################
    # Copy directory from path to a new path #
    ##########################################

    def copyDir(self, dirPath, destPath, dirName=None, renameOverride=None, **kwargs):
        '''
        Description : Attempts to copy contents from 'dirPath' full pathway
                      to the full directory pathway 'destPath', optional, the
                      string found in 'dirName' will be the name of the new
                      directory, else the new directory will have the same
                      name as the old one.

        Input :

            dirPath : [string] corrosponds to full pathway of the location of the file to be copied
            destPath  : [string], corrosponds to the pathway of the newly created copy directory
            dirName  : [string] (Default : None), corrosponds to full pathway of the location of the copy

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("copyDir", **kwargs)

        if(isinstance(dirPath, (list,tuple))):
            dirPath = self.convertPath(dirPath, **kwargs)
            if(dirPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'dirPath', **kwargs)
        elif(isinstance(dirPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='dirPath', **kwargs)

        if(isinstance(destPath, (list,tuple))):
            destPath = self.convertPath(destPath, **kwargs)
            if(destPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'destPath', **kwargs)
        elif(isinstance(destPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='destPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(dirPath, destPath, objName=dirName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(dirName, str)):
                destPath = self.joinNode(destPath, dirName, **kwargs)
            else:
                destPath = destPath

        try:
            shutil.copytree(dirPath, destPath)
            success = True
        except:
            errmsg = ["directory could not be copied", "Directory pathway: "+str(dirPath), "Destination pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, varID='dirPath', **kwargs)
        return success


    def __copyDir__(self, dirPath, destPath, dirName=None, renameOverride=None, **kwargs):

        success = self.copyDir(dirPath, destPath, dirName, renameOverride)
        if(not success):
            return self.__err_print__("failure to perform move operation", **kwargs)

        try:
            if(isinstance(dirName, str)):
                startDir = self.convertPath(destPath, "list")[-1]
            else:
                startDir = self.convertPath(destPath, "list")[-2]
        except:
            return self.__err_print__("failure to find folder for object pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return True


    def delObj(self, delPath, **kwargs):
        '''
        Description : Attempts to delete the content at the location of the input pathway

        Input:

            delPath : A complete pathway string pointing to a file or folder

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("delObj", **kwargs)

        if(isinstance(delPath, (list,tuple))):
            delPath = self.convertPath(delPath, **kwargs)
            if(delPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'delPath', **kwargs)
        elif(isinstance(delPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='delPath', **kwargs)

        if(os.path.isfile(delPath)):
            opt = 'file'
        elif(os.path.isdir(delPath)):
            opt = 'fold'
        else:
            errmsg = ["is not a file pathway", "Pathway: "+str(delPath)]
            return self.__err_print__(errmsg, varID='delPath', **kwargs)

        try:
            if(opt == 'file'):
                os.remove(delPath)
            elif(opt == 'fold'):
                shutil.rmtree(delPath)
            else:
                errmsg = ["Failure to delete object", "File pathway: "+str(delPath)]
                return self.__err_print__(errmsg, **kwargs)
        except:
            errmsg = ["Failure to delete object", "File pathway: "+str(delPath)]
            return self.__err_print__(errmsg, **kwargs)
        return True


    #############################
    # find object(s) in pathway #
    #############################

    def find(self, objName, dirPath, objType='all', **kwargs):
        '''
        Description : Searches an input directory for an object name

        Input :

            objName : [string or list of strings], Name of file(s) to be searched for
            dirPath : [string], pathway of directory for which 'objName' is to be searched
            objType : [string] (Default : 'all'), type of object to be searched for

        Output : False if error occurs, else a dictionary 
                 The output dictionary contains the input object names as keys and 
                 the truth value of their existance in the input directory as values 
        '''

        kwargs = self.__update_funcNameHeader__("find", **kwargs)

        contents = self.contentPath(dirPath, objType, **kwargs)
        if(contents == False):
            return self.__err_print__("pathway contents could not be resolved", varID='dirPath', **kwargs)

        if(isinstance(objName, str)):
            if(objName in contents):
                within = True
            else:
                within = False
            return {objName:within}
        elif(isinstance(objName, (list, tuple))):
            outDict = {}
            for obj in objName:
                if(obj in contents):
                    within = True
                else:
                    within = False
                outDict[obj] = within
            return outDict
        else:
            return self.__err_print__("must be either a string or an array", varID='objName', **kwargs)
        return False


    def __find__(self, objName, objType='all', **kwargs):

        outDict = self.find(objName, self.varPath, objType)
        if(outDict == False):
            return self.__err_print__("failure to complete 'find' operation")
        else:
            return outDict


    #################################################
    # find object(s) containing fragment in pathway #
    #################################################

    def match(self, fragment, dirPath, objType='all', **kwargs):
        '''
        Description : Searches an input directory for any object containing a specific string 

        Input :

            fragment : [string or list of strings], string fragment to be matched
            dirPath : [string], pathway of directory for which 'fragment' is to be searched
            objType : [string] (Default : 'all'), type of object to be searched for

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("match", **kwargs)

        contents = self.contentPath(dirPath, objType, **kwargs)
        if(contents == False):
            return self.__err_print__("pathway contents could not be resolved", varID='dirPath', **kwargs)

        if(isinstance(fragment, str)):
            capList = []
            for entry in contents:
                if(fragment in entry):
                    capList.append(entry)
            return {fragment:capList}
        elif(isinstance(fragment, (list, tuple))):
            outDict = {}
            for frag in fragment:
                capList = []
                for entry in contents:
                    if(frag in entry):
                        capList.append(entry)
                outDict[frag] = capList
            return outDict
        else:
            return self.__err_print__("must be either a string or an array", varID='fragment', **kwargs)
        return False

    def __match__(self, fragment, objType='all', **kwargs):

        outDict = self.match(fragment, self.varPath, objType, **kwargs)
        if(outDict == False):
            return self.__err_print__("failure to complete 'match' operation", **kwargs)
        else:
            return outDict


    ######################
    # printing functions #
    ######################


    def __fancyPrint__(self, colour=False):
        '''
        Description : Stylized printing of path information

        Input :
            colour : [Bool], color option for distinguishing folders from files

        Output : [Bool], success
        '''
        if(colour):
            blue = '\033[38;5;4m'
            black = '\033[38;5;0m'
            if(self.varOS == 'unix' or self.varOS == 'linux'):
                black = '\033[38;5;2m'
        else:
            blue,black=('','')

        headln = self.space+"The current pathway is: "+self.endline
        bodyln = self.space+'The content of the current directory is as follows: '+self.endline

        print(headln)
        print(self.doubleSpace+"'"+str(self.varPath)+"'"+self.endline)

        try:
            spc = self.varPath_Contains
            spf = self.varPath_Files
            print(bodyln)
            for i in spc:
                if(i in spf):
                    print(black+self.doubleSpace+i)
                else:
                    print(blue+self.doubleSpace+i)
            print(black)
            return True
        except:
            return False


    def __runFancyPrint__(self):
        if(self.shellPrint):
            try:
                ecrive = self.__fancyPrint__(self.varCol)
                return ecrive
            except:
                return False
        else:
            return True


    def __fancyPrintList__(self,array):

        print(self.endline)
        for i in array:
            print(self.space+str(i))
        print(self.endline)
        return True


    ############################################################
    #                                                          #
    #   ####################################################   #   
    #   # cmd Function: String-to-Command Parsing Function #   #
    #   ####################################################   #
    #                                                          #
    ############################################################

    def __headCheck__(self, **kwargs):                  
        if(len(self.varPath_List) == 1):
            self.__err_print__("cannot move up pathway; home directory reached", heading = 'Warning', **kwargs)
            return True
        else:
            return False

    def __cmdPrintFunc__(self, test, **kwargs):
        success = True
        if(test):
            ptest = self.__runFancyPrint__()
            if(ptest):
                return True
            else:
                return self.__err_print__("failure to generate error message...", **kwargs)
        else:
            return self.__err_print__("failure to update current pathway", **kwargs)

    def __cmdUpdater__(self, newPath, value=None, noPrint=False, **kwargs):
        utest = self.__updatePath__(newPath, **kwargs)
        if(noPrint):
            success = utest
        else:
            success = self.__cmdPrintFunc__(utest, **kwargs)
        result = (success, value)
        return result

#    def __cmd_current_files__(self, fileList, cmdInst=None, **kwargs):
#
#        if(fileList == []):
#            return []
#        outfiles = []
#
#        errlist = []
#        for file in fileList:
#            if(file not in self.varPath_Files and cmdInst not in self.singlePathListGroup and cmdInst not in self.singlePathListNoGroup):
#                errlist.append(str(file))
#            else:
#                outfiles.append(file)
#        if(len(outfiles) == 0):
#            self.__err_print__("none of the files were found in the current directory", heading='Warning', **kwargs)
#        if(len(errlist) > 0):
#            self.__err_print__(["the following files were not found in the current directory"]+errlist, **kwargs)        
#        return outfiles

    def cmd_pwd(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_pwd", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        value = self.varPath
        if(value == False or value == None):
            self.__err_print__("Current pathway could not be resolved", **kwargs)

        result = (success, value)
        return result

    def cmd_ls(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_ls", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        value = self.varPath_Contains
        if(value == False or value == None):
            value = None
            success = self.__err_print__("current directory contents could not be obtained", **kwargs)

        result = (success, value)
        return result

    def cmd_dir(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_dir", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        new_file_list = []

        values = self.__find__(file_list, **kwargs)
        if(values == False):
            self.__err_print__("failure when searching current directory", **kwargs)
            return (values, value)

        errlist = []
        for file in file_list:
            if(values[file]):
                new_file_list.append(self.joinNode(self.varPath, file, **kwargs))
            else:
                errlist.append(str(file))
        value = new_file_list

        if(len(errlist)>0 and self.shellPrint):
            kwargs['funcName'] = None
            self.__err_print__(["The following objects were not found in the current directory:"]+errlist, heading='Warning', **kwargs)

        if(len(value)>0 and self.shellPrint):
            kwargs['funcName'] = None
            self.__err_print__(["The following object pathways were found in the current directory:"]+value, heading="Info", **kwargs)

        return (True, value)


    def cmd_cd(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_cd", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        if(destStr == '..'):
            # move up one node
            if(self.__headCheck__(**kwargs)):
                return (success,value)
            else:
                try:
                    temp_list = list(self.varPath_List)
                except:
                    self.__err_print__("failure within internal pathway", **kwargs)
                    return (False, None)
                if(len(temp_list) > 0):
                    up_path_list = temp_list[:-1]
                else:
                    self.__err_print__("failure within internal pathway", **kwargs)
                    return (False, None)
            result = self.__cmdUpdater__(up_path_list, value, **kwargs)

        elif(destStr in self.varPath_Contains):
            # move down one node
            dest_loc = self.joinNode(self.varPath, destStr)
            if(os.path.isdir(dest_loc)):
                newPath_list = list(self.varPath_List)
                newPath_list.append(destStr)
            else:
                errmsg = ["is not a folder within the current directory", "pathway : "+str(dest_loc)]
                success = self.__err_print__(errmsg, varID='dest_loc', **kwargs)
                return (success, value)
            result = self.__cmdUpdater__(newPath_list, value, **kwargs)

        elif(destStr[0] == '/' or destStr[0] == '\\'):
            # jump upwards to a given node
            destStr = destStr[1:]
            ctest = self.__climbPath__(destStr, failPrint=False, **kwargs)
            if(ctest):
                result = (ctest, value)
            else:
                path_piece = self.Str2Arr(destStr, **kwargs)
                if(path_piece == False):
                    success = self.__err_print__(["failed parsing", "destStr : "+str(destStr)], varID='destStr', **kwargs)
                    return (success, value)
                path_piece_str = self.Arr2Str(list(self.varPath_List)+path_piece, **kwargs)
                if(path_piece_str == False):
                    success = self.__err_print__(["failed parsing", "destStr : "+str(destStr)], varID='destStr', **kwargs)
                    return (success, value)
                if(os.path.isdir(path_piece_str)):
                    result = self.__cmdUpdater__(path_piece_str, **kwargs)
                else:
                    success = self.__err_print__("failure to find '"+str(destStr)+"' while climbing current pathway", **kwargs)
                return (success, value)

        elif(destStr == '~'):
            # jump to home directory
            result = self.__cmdUpdater__(self.varPath_Head, value)

        else:
            success = self.__err_print__("'"+str(destStr)+"' not a valid destination", **kwargs)
            result = (success, value)

        return result


    def cmd_chdir(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_chdir", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        success, value = self.__cmdUpdater__(destStr, **kwargs)
        if(success == False):
            self.__err_print__(["is not a valid pathway:","'destStr' : "+str(destStr)], varID='destStr', **kwargs)
        return (success, value)


    def cmd_mv(self, tup, **kwargs):

        def __move_object_2_path__(dest_path_list, move_file_list, rename=False, **kwargs):
            success = True

            dest_path_str = self.convertPath(dest_path_list, **kwargs)
            newname = dest_path_list[-1]

            if(rename):
                path_has = self.contentPath(self.varPath)
            else:
                path_has = self.contentPath(dest_path_str)

            if(newname in path_has and self.rename == False):
                return self.__err_print__("[cmd_mv] Error: '"+str(newname)+"' already exists in target directory", funcAdd = 'cmd')

            for entry in move_file_list:
                init_path = self.joinNode(self.varPath, entry, **kwargs)
                if(rename):
                    mtest = self.__moveObj__(init_path, self.varPath, objName=newname, **kwargs)
                else:
                    mtest = self.__moveObj__(init_path, dest_path_str, **kwargs)
                if(not mtest):
                    success = self.__err_print__(["pathway contents could not be moved:", "Pathway: "+str(init_path)], **kwargs)
            return success

        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_mv", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        rename = False
        dpath_list = []

        # parsing destination in list format
        if(destStr == '..'):
            if(self.__headCheck__()):
                self.__err_print__("'home' directory reached, no action taken", heading='Warning', **kwargs)
                return (success, value)
            else:
                dpath_list = list(self.varPath_List)
                dpath_list = dpath_list[:-1]

        elif(destStr in self.varPath_Folders):
            dpath_list = list(self.varPath_List)
            dpath_list.append(destStr)

        elif(destStr[0] == '/' or destStr[0] == '\\'):
            destStr = destStr[1:]
            dpath_list = self.climbPath(self.varPath, destStr)
            if(dpath_list == False):
                self.__err_print__("failure to find '"+str(destStr)+"' while climbing current pathway", **kwargs)
                return (False, value)

        elif(len(file_list) == 1 and destStr not in self.varPath_Folders):
            dpath_list = list(self.varPath_List)
            dpath_list.append(destStr)
            rename = True

        elif(destStr == '~'):
            dpath_list = [self.varPath_Head]

        else:
            success = self.__err_print__("invalid formatting, no action taken", **kwargs)
            return (success, value)

        # Move file(s) to destination
        if(len(dpath_list) == 0):
            success = self.__err_print__("destination pathway list could not be parsed", **kwargs)
            return (success, value)
        __move_object_2_path__(dpath_list, file_list, rename=rename, **kwargs)

        # Update
        return self.__cmdUpdater__(self.varPath_List, value, **kwargs)


    def cmd_rm(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_rm", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        if(not isinstance(self.varPath_Files, (list, tuple))):
            success = self.__err_print__("pathway files have not been set, no action taken", **kwargs)
            return (success, value)

        errlist = []
        for file in file_list:
            if(file in self.varPath_Files):
                file_path_str = self.joinNode(self.varPath, file, **kwargs)
                dtest = self.delFile(file_path_str)
                if(not dtest):
                    success = self.__err_print__(["'"+str(file)+"' not properly deleted:","Pathway: '"+str(file_path_str)+"'"])
            else:
                errlist.append("'"+str(file)+"'")

        if(len(errlist)>0):
            self.__err_print__(["The following files were not found in the current directory"]+errlist, **kwargs)

        result = self.__cmdUpdater__(self.varPath_List, value)
        return result


    def cmd_cp(self, tup, **kwargs):

        def parse_file_name(file_name, **kwargs):
            file_name_list = filter(None, file_name.split('.'))
            if(len(file_name_list) == 2):
                return file_name_list
            elif(len(file_name_list) > 2):
                self.__err_print__("'"+str(file_name)+"' does not match proper file naming conventions", heading="Warning", **kwargs)
                new_file_name = strl.array_to_str(file_name[:-1], spc='_', **kwargs)
                if(self.__not_str_print__(new_file_name, varID='generated file name', **kwargs)):
                    return False
                return [new_file_name, file_name_list[-1]]
            else:
                return self.__err_print__("'"+str(file_name)+"' does not match proper file naming conventions", **kwargs)

        def help_func(file_list, path_str, **kwargs):

            success = True
            value = None

            for file in file_list:
                new_file_name = parse_file_name(file)
                if(new_file_name == False):
                    self.__err_print__("The file name, '"+str(file)+"', could not be properly parsed", **kwargs)
                    continue

                old_inst = self.joinNode(self.varPath, file)
                cp_inst = new_file_name[0]+"."+file_inst_list[1]
                ctest = self.__copyFile__(old_inst, path_str, objName=cp_inst, **kwargs)
                if(not ctest):
                    success = self.__err_print__("The file, '"+str(file)+"', could not be copied", **kwargs)
            if(self.varPath == path_str):
                result = self.__cmdUpdater__(self.varPath_List, value, **kwargs)
            else:
                result = self.__cmdUpdater__(self.varPath_List, value, noPrint=True, **kwargs)
            return result

        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_cp", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        if(destStr == '.'):
            return help_func(file_list, self.varPath)

        elif(destStr == '..'):
            if(self.__headCheck__()):
                return (success,value)
            else:
                up_path_list = list(self.varPath_List)[:-1]
            up_path_str = self.convertPath(up_path_list, **kwargs)
            return help_func(file_list, up_path_str)

        elif(destStr in self.varPath_Contains):
            path_str = self.joinNode(self.varPath, destStr, **kwargs)
            return help_func(file_list, path_str)

        elif(destStr[0] == '/' or destStr[0] == '\\'):
            node_inst = destStr[1:]
            path_str = self.__climbPath__(node_inst, **kwargs)
            if(path_str == False):
                success = self.__err_print__("the folder: '"+str(node_inst)+"' was not found within the current pathway", **kwargs)
                return (success,value)
            return help_func(file_list, path_str)

        elif(destStr == '~'):
            path_str = self.varPath_Head
            try:
                path_has = self.contentPath(path_str, objType='files', **kwargs)
            except:
                success = self.__err_print__("directory could not be accessed", varID='home', **kwargs)
                return (success, value)
            return help_func(file_list, path_str)
        else:
            success = self.__err_print__("is not a valid destination", varID=str(destStr), **kwargs)
        return (success, value)


    def cmd_mkdir(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_mkdir", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        for file in file_list:
            file_path_str = self.joinNode(self.varPath, file)
            ctest = self.makeDir(file_path_str)  
            if(not ctest):
                success = self.__err_print__("directory could not be created", varID=str(file), **kwargs)

        return self.__cmdUpdater__(self.varPath_List, value, **kwargs)


    def cmd_rmdir(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_rmdir", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        for file in file_list:
            if(file in self.varPath_Folders):
                file_path_str = self.joinNode(self.varPath, file)
                output = self.delDir(file_path_str)
                if(output == False):
                    self.__err_print__("'"+str(file)+"' could not be deleted", **kwargs)
            else:
                self.__err_print__("'"+str(file)+"' does not corrospond to a folder in the current directory", **kwargs)

        return self.__cmdUpdater__(self.varPath_List, value)


    def cmd_cpdir(self, tup, **kwargs):

        def parse_dir_name(file_name, **kwargs):
            if(not isinstance(file_name, str)):
                return False
            if('.' in file_name):
                return self.__err_print__("contains '.'", varID=file_name, heading="Warning", **kwargs)
            if('\\' in file_name or '/' in file_name):
                return self.__err_print__("contains pathway delimiter", varID=file_name, heading="Warning", **kwargs)
            return file_name

        def help_func(dir_list, path_str, **kwargs):

            success = True
            value = None

            for dir in dir_list:
                new_dir_name = parse_dir_name(dir)
                if(new_dir_name == False):
                    self.__err_print__("The folder name, '"+str(dir)+"', could not be properly parsed", **kwargs)
                    continue

                old_inst = self.joinNode(self.varPath, dir)
                ctest = self.__copyDir__(old_inst, path_str, dirName=new_dir_name, **kwargs)
                if(not ctest):
                    success = self.__err_print__("The folder, '"+str(dir)+"', could not be copied", **kwargs)

            if(path_str == self.varPath):
                return self.__cmdUpdater__(self.varPath_List, value, **kwargs)
            else:
                return self.__cmdUpdater__(self.varPath_List, value, noPrint=True, **kwargs)

        # cmd_cpdir MAIN
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_cpdir", **kwargs)
        try:
            cmdInst, dir_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        if(destStr == '.'):
            result = help_func(dir_list, self.varPath, **kwargs)
            return result

        elif(destStr == '..'):
            if(self.__headCheck__()):
                return (success,value)
            else:
                up_path_list = list(self.varPath_List)[:-1]
            up_path_str = self.convertPath(up_path_list, **kwargs)
            return help_func(dir_list, up_path_str, **kwargs)

        elif(destStr in self.varPath_Contains):
            path_str = self.joinNode(self.varPath, destStr, **kwargs)
            return help_func(dir_list, path_str, **kwargs)

        elif(destStr[0] == '/' or destStr[0] == '\\'):
            node_inst = destStr[1:]
            path_str = self.__climbPath__(node_inst, **kwargs)
            if(path_str == False):
                success = __err_print__("not found in the current pathway", varID=node_inst, **kwargs)
                return (success,value)
            return help_func(dir_list, path_str, **kwargs)

        elif(destStr == '~'):           
            path_str = self.varPath_Head                     
            return help_func(dir_list, path_str, **kwargs)

        else:
            success = __err_print__("is not a valid destination", varID=destStr, **kwargs)         
        result = (success, value)
        return result 


    def cmd_find(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_find", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        value = self.__find__(file_list, **kwargs)
        if(value == False):
            success = self.__err_print__("failure to parse 'find' values", **kwargs)
            return (success, value)

        if(self.shellPrint):
            kwargs['funcName'] = None
            if(all(i == True for i in value)):
                self.__err_print__("All searched objects have been found in the current directory!", heading='Info', **kwargs)
            else:
                not_found = []
                for found in value:
                    if(value[found] == False):
                        not_found.append(found)
                if(len(not_found) > 0):
                    print_list = ["The following objects were not found in the current directory:"]+not_found
                    self.__err_print__(print_list, heading='Info', **kwargs)

        result = (success, value)
        return result


    def cmd_match(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_match", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        match_dict = self.__match__(file_list, **kwargs)
        if(match_dict == False):
            success = self.__err_print__("failure to parse 'match' values", **kwargs)
            return (success, value)

        if(self.shellPrint):
            if(len(match_dict) == 0):
                self.__err_print__("No matches found", heading='Info', **kwargs)
            else:
                for frag in match_dict:
                    infomsg = ["The following matches were found for the string, '"+str(frag)+"' :"]+match_dict[frag]
                    self.__err_print__(infomsg, heading='Info', **kwargs)
        result = (success, match_dict)
        return result


    def cmd_vi(self, tup, **kwargs):
        # 'cmd' Function preamble
        kwargs = self.__update_funcNameHeader__("cmd_vi", **kwargs)
        try:
            cmdInst, file_list, destStr = tup
        except:
            self.__err_print__(["could not be parsed into the three required input objects", "input: "+str(tup)], varID='tup', **kwargs)
        success, value = self.__cmdUpdater__(self.varPath_List, noPrint=True, **kwargs)
        if(success == False):
            return (False, None)
        # Function start

        if(len(file_list) > 1):
            self.__err_print__("Only one file can be grabbed at a time", heading='Warning', **kwargs)         

        file_name = file_list[0]
        file_path_str = self.joinNode(self.varPath, file_name, **kwargs)

        if(file_name in self.varPath_Files):
            try:
                value = iop.flat_file_grab(file_path_str, **kwargs)
            except:
                success = __err_print__("contents could not be retrieved", varID=file_name, **kwargs)
        elif(file_name not in self.varPath_Contains):
            try:
                value = iop.flat_file_write(file_path_str, **kwargs)
            except:
                success = self.__err_print__("[cmd_vi] Error: The file '"+str(file_name)+"' could not be opened", **kwargs)
        else:
            success = self.__err_print__("not found in the current directory", varID=file_name, **kwargs)

        result = self.__cmdUpdater__(self.varPath_List, value, **kwargs)
        return result


    def cmd(self, cmd_string, **kwargs):

        '''
        -------
        | cmd |
        -------
        
        Input: 

            cmd_string : a string, must be formated according to the specifications below.

        Valid Commands: 

            'ls' : returns list of strings containing the contents of the present directory

            'dir': returns pathway for file in the current directory

            'pwd'  : Returns current directory pathway as string; equivalent to 'self.varPath'

            'cd' : moves into the input directory, note: input directory must be in current directory
                   ('..' to move upwards) ('\\' or '/' to specify directory in root directory)
                   ('~' moves to home directory)

            'chdir' : moves to the directory input, input must be full directory pathway 

            'mv' : moves file(s) from current directory into another directory 
                   which is accessible to the current path
                   (format note: 'mv file_path.file Directory_Name') [file extension must be included]

            'rm' : remove input file(s) from current directory

            'cp' : copies file(s) to destination

            'mkdir' : make new director(y)ies with name equalivalent to input string

            'rmdir' : delete subdirector(y)ies (equiv. to 'rm -rf Directory_Name')

            'cpdir' : copy directory from current directory

            'find' : Searches the current directory for the input file(s) string and returns boolean

            'match' : Searches the current directory for the input pattern and returns list of matches

            'vi'   : Returns a list of strings corrosponding to the contents of a file
        
        '''

        ##################
        # Function: Main #
        ##################

        kwargs = self.__update_funcNameHeader__("cmd", **kwargs)

        result = (False,None)

        # Dummy test
        if(self.__not_str_print__(cmd_string, **kwargs)):
            return result
        if(cmd_string == '' or cmd_string.isspace()):
            errmsg = ["must be a properly formated string","No action taken, see 'help' for more info on proper 'cmd' formatting"]
            self.__err_print__(errmsg, varID='cmd_string', **kwargs)
            return result

        cmd_tuple = self.__cmdInputParse__(cmd_string, **kwargs)
        if(cmd_tuple == ('', [], '')):
            if(self.shellPrint):
                errmsg = ["could not be properly parsed. Below is a summary of the input/output:",
                          "'cmd_string' = '"+str(cmd_string)+"'",
                          "'cmdInst' = '"+str(cmdInst)+"'",
                          "'cmd_tuple' = '"+str(cmd_tuple)+"'"]
                self.__err_print__(errmsg, varID='cmd_string', **kwargs)
            return result

        cmdInst, fileList, destStr = cmd_tuple
        cmdCmd = self.cmdDict.get(cmdInst)

        if(isinstance(cmdCmd, str)):
            exec_string = "result = "+cmdCmd+"(cmd_tuple, **kwargs)"
            exec(exec_string)
        else:
            if(self.shellPrint):
                errmsg = ["could not be properly parsed. Below is a summary of the input/output:",
                          "'cmd_string' = '"+str(cmd_string)+"'",
                          "'cmdInst' = '"+str(cmdInst)+"'",
                          "'cmd_tuple' = '"+str(cmd_tuple)+"'"]
                self.__err_print__(errmsg, varID='cmd_string', **kwargs)
        return result