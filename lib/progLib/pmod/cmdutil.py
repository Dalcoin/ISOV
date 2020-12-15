import os
import sys
import subprocess

import ioparse as iop
from cmdline import PathParse


# File Utility Functions
#
#def convert_endline(file, style='dos2unix', space='    '):
#
#    lines = iop.flat_file_read(file)
#    if(lines == False):
#        print("could not read input 'file' : "+str(file))
#        return False
#
#    if(style == 'dos2unix'):
#        end_Line = "\n"
#    elif(style == 'unix2dos'):
#        end_Line = "\r\n"
#    elif(style == None):
#        end_Line = ""
#    else:
#        print(space+"[convert_endline] Error: 'style' not reconginzed")
#        return False  
#     
#    out_Lines = [i.rstrip()+end_Line for i in lines]  
#    return out_Lines



class cmdUtil(PathParse):
      
    def __init__(self,
                 osFormat,
                 newPath=None,
                 rename=False,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    ',
                 endline='\n',
                 moduleNameOverride="cmdUtil",
                 **kwargs):

        super(cmdUtil, self).__init__(osFormat,
                                      newPath,
                                      rename,
                                      debug,
                                      shellPrint,
                                      colourPrint,
                                      space,
                                      endline,
                                      moduleNameOverride,
                                      **kwargs)

    ############################################################33##


    ############################################################33##
                                                                   #
    ### File Functions                                             #
                                                                   # 
    ############################################################33##

    # Changing the endline character of text files

    def endlineConvert(self, lines, style='dos2unix', **kwargs):

        kwargs = self.__update_funcNameHeader__("endlineConvert", **kwargs)

        if(self.__not_strarr_print__(lines, varID='lines', firstError=True, **kwargs)):
            return False

        if(style == 'dos2unix'):
            endLine = b"\n"
        elif(style == 'unix2dos'):
            endLine = b"\r\n"
        elif(style == None):
            endLine = ""
        else:
            return self.__err_print__("not reconginzed: use 'dos2unix' or 'unix2dos'", varID='style', **kwargs)

        out_Lines = [line.rstrip()+endLine for line in lines]
        return out_Lines


    def filesEndlineConvert(self, files, style='dos2unix', foldName=None, **kwargs):

        kwargs = self.__update_funcNameHeader__("filesEndlineConvert", **kwargs)

        # checking 'files' input for proper formatting
        if(isinstance(files,str)):
            files = [files]
        elif(isinstance(files, (list,tuple))):
            if(self.__not_strarr_print__(files, varID='files', firstError=True, **kwargs)):
                return False
        else:
            return self.__err_print__("type must be either string or list of strings: "+str(type(files)), varID='files', **kwargs)

        # checking 'style' variable
        if(style != None and not isinstance(style, str)):
            return self.__err_print__("must be either a string or None type : "+str(type(style)), varID='style', **kwargs)
        else:
            if(isinstance(style, str)):
                if(style not in ['dos2unix', 'unix2dos']):
                    self.__err_print__("must be either 'dos2unix' or 'unix2dos' if a string : '"+style+"'", varID='style', **kwargs)

        # actions based upon 'foldName' input
        if(foldName == None):
            for file in files:
                if(file in self.varPath_Files):
                    pathway = self.joinNode(self.varPath, file, **kwargs)
                    if(pathway == False):
                        self.__err_print__("could not be joined to the current pathway", varID=str(file), **kwargs)
                        continue
                    lines = iop.flat_file_read(pathway, **kwargs)
                    if(lines == False):
                        self.__err_print__("lines could not be joined to the current pathway", varID=str(file), **kwargs)
                        continue
                    newlines = self.endlineConvert(lines, style, **kwargs)
                    if(newlines == False):
                        self.__err_print__("endlines could not be converted", varID=str(file), **kwargs)
                        continue
                    success = iop.flat_file_write(pathway, add_list=newlines, ptype='wb', **kwargs)
                    if(success == False):
                        self.__err_print__("converted lines could not be rewritten to file", varID=str(file), **kwargs)
                        continue
            return True
        elif(foldName in self.varPath_Folders):
            fold_node = self.joinNode(self.varPath, foldName)
            if(fold_node == False):
                return self.__err_print__("could not be joined to current pathway", varID=str(foldName), **kwargs)
            fold_contents = self.contentPath(fold_node, objType='file')
            if(fold_contents == False):
                return self.__err_print__("content could not be retrieved", varID=str(foldName), **kwargs)

            for file in files:
                if(file in fold_contents):
                    pathway = self.joinNode(fold_node, file, **kwargs)
                    if(pathway == False):
                        self.__err_print__("could not be joined to the '"+fold_node+"' pathway", varID=str(file), **kwargs)
                        continue
                    lines = iop.flat_file_read(pathway, **kwargs)
                    if(lines == False):
                        self.__err_print__("lines could not be joined to the '"+fold_node+"' pathway", varID=str(file), **kwargs)
                        continue
                    newlines = self.endlineConvert(lines, style, **kwargs)
                    if(newlines == False):
                        self.__err_print__("endlines could not be converted", varID=str(file), **kwargs)
                        continue
                    success = iop.flat_file_write(pathway, add_list=newlines, ptype='wb', **kwargs)
                    if(success == False):
                        self.__err_print__("converted lines could not be rewritten to file", varID=str(file), **kwargs)
                        continue
            return True
        else:
            return self.__err_print__("not reconginzed: '"+str(foldName)+"'", varID='foldName', **kwargs)

    # Generating a complimentary string for file name

    def name_compliment(self, name, comp_dict, **kwargs):

        kwargs = self.__update_funcNameHeader__("name_compliment", **kwargs)

        if(self.__not_str_print__(name, varID='name', **kwargs)):
            return False

        if(not isinstance(comp_dict, dict)):
            return self.__err_print__("should be a dictionary type : "+str(type(comp_dict)), varID='comp_dict', **kwargs)

        name_compliments = []
        for entry in comp_dict:
            if(len(name.split(str(entry)))==2):
                add_val = str(comp_dict[entry])
                base_val = name.split(str(entry))
                if(base_val[0] == ''):
                    new_name = add_val+base_val[1]
                    base_id = (base_val[1],)
                else:
                    new_name = base_val[0]+add_val+base_val[1]
                    base_id = (base_val[0], base_val[1])
                name_compliments.append((new_name, base_id),)

        return name_compliments

    ############################################################33##
                                                                   #
    ### Directory Functions                                        #
                                                                   #
    ############################################################33##


    def clearDir(self, dirs, select='all', style=None, **kwargs):
        '''
        Notes:

            Action: Deletes the contents of a directory accessible from 
                    the current pathway. The directory is preserved in the 
                    process. 

            Variables:

                dirs : string, corresponding to a file name
                select : (string), narrows files to be deleted
                style : string or (None), selects objects to be deleted by name or file type

            Valid 'select' values:

                'all'
                'file'
                'files'
                'directory'
                'directories'
                'dir'
                'dirs'
                'folder'
                'folders'

        '''
        kwargs = self.__update_funcNameHeader__("clearDir", **kwargs)

        select_array = ['all']+self.dirNames+self.fileNames

        if(isinstance(select,str)):
            select = select.rstrip().lower()
            if(select not in select_array):
                errmsg = ["should be in a valid object name:",
                          "Files : "+str(self.fileNames),
                          "Directory : "+str(self.dirNames),
                          "Both : 'all'"]
                return self.__err_print__(errmsg, varID='select', **kwargs)
            opt = 'str'
        elif(self.strarrCheck(select, varName='select', failPrint=False, **kwargs)):
            opt = 'arr'
        else:
            return self.__err_print__("should be either a string or an array of strings", varID='select', **kwargs)

        # dirs parsed as a array of string(s)
        if(self.strarrCheck(dirs, varName='dirs', failPrint=False, **kwargs)):
            pass
        elif(isinstance(dirs, str)):
            dirs = [dirs]
        else:
            return self.__err_print__("should be either a string or array of strings, not "+str(type(dirs)), varID='dirs', **kwargs)

        # delete items according to 'select'
        dirs_to_empty = []
        not_dirs = []
        for dir in dirs:
            if(dir in self.varPath_Folders):
                dirs_to_empty.append(dir)
            else:
                not_dirs.append(dir)

        if(len(not_dirs) > 0):
            self.__err_print__(["The following entries are not directories in the current pathway:"]+not_dirs, **kwargs)

        # Delete files from directories
        fail_dirs = []
        for dir in dirs_to_empty:
            dirPath = self.joinNode(self.varPath, dir, **kwargs)
            if(dirPath == False):
                continue
            if(opt == 'str'):
                if(select == 'all'):
                    if(isinstance(style, str)):
                        contents = self.contentPath(dirPath, **kwargs)
                        if(contents == False):
                            fail_dirs.append(dir)
                            continue
                        for obj in contents:
                            if(style in obj):
                                pass
                            else:
                                continue
                            objPath = self.joinNode(dirPath, obj, **kwargs)
                            if(objPath == False):
                                fail_dirs.append(dir+self.delim+obj)
                                continue
                            if(os.path.isfile(objPath)):
                                try:
                                    os.remove(objPath)
                                except:
                                    continue
                            elif(os.path.isdir(objPath)):
                                try:
                                    shutil.rmtree(objPath)
                                except:
                                    continue
                            else:
                                fail_dirs.append(dir+self.delim+obj)
                    else:
                        success = self.delDir(dirPath, **kwargs)
                        if(success):
                            success = self.makeDir(dirPath, **kwargs)
                        if(not success):
                            fail_dirs.append(dir)
                elif(select in self.fileNames):
                    contents = self.contentPath(dirPath, objType='file', **kwargs)
                    if(contents == False):
                        fail_dirs.append(dir)
                        continue
                    if(isinstance(style, str)):
                        for obj in contents:
                            if(style in obj):
                                pass
                            else:
                                continue
                            objPath = self.joinNode(dirPath, obj, **kwargs)
                            if(objPath == False):
                                fail_dirs.append(dir+self.delim+obj)
                                continue
                            success = self.delFile(objPath, **kwargs)
                            if(success == False):
                                fail_dirs.append(dir+self.delim+obj)
                    else:
                        for obj in contents:
                            objPath = self.joinNode(dirPath, obj, **kwargs)
                            if(objPath == False):
                                fail_dirs.append(dir+self.delim+obj)
                                continue
                            success = self.delFile(objPath, **kwargs)
                            if(success == False):
                                fail_dirs.append(dir+self.delim+obj)
                elif(select in self.dirNames):
                    contents = self.contentPath(dirPath, objType='dir', **kwargs)
                    if(contents == False):
                        fail_dirs.append(dir)
                        continue
                    if(isinstance(style, str)):
                        for obj in contents:
                            if(style in obj):
                                pass
                            else:
                                continue
                            objPath = self.joinNode(dirPath, obj, **kwargs)
                            if(objPath == False):
                                fail_dirs.append(dir+self.delim+obj)
                                continue
                            success = self.delDir(objPath, **kwargs)
                            if(success == False):
                                fail_dirs.append(dir+self.delim+obj)
                    else:
                        for obj in contents:
                            objPath = self.joinNode(dirPath, obj, **kwargs)
                            if(objPath == False):
                                fail_dirs.append(dir+self.delim+obj)
                                continue
                            success = self.delDir(objPath, **kwargs)
                            if(success == False):
                                fail_dirs.append(dir+self.delim+obj)
            elif(opt == 'arr'):
                contents = self.contentPath(dirPath, **kwargs)
                if(contents == False):
                    fail_dirs.append(dir)
                    continue
                for obj in select:
                    if(obj in contents):
                        objPath = self.joinNode(dirPath, obj, **kwargs)
                        if(objPath == False):
                            fail_dirs.append(dir+self.delim+obj)
                            continue
                        success = self.delObj(objPath, **kwargs)
                        if(success == False):
                            fail_dirs.append(dir+self.delim+obj)
                    else:
                        fail_dirs.append(dir+self.delim+obj)
        if(len(fail_dirs) > 0):
            errmsg = ["The following objects could not be cleared:"]+fail_dirs
            self.__err_print__(errmsg, **kwargs)
        return True


    def transfer_folder_content(self, start_dir, end_dir, select='all', style=None, copy=False, **kwargs):

        kwargs = self.__update_funcNameHeader__("transfer_folder_content", **kwargs)

        option = None
        if(isinstance(select, str)):
            if(select.lower() in self.dirNames or select.lower() in self.fileNames or select.lower() == 'all'):
                select = select.lower()
                option = 'str'
            else:
                select = [select]
                option = 'arr'
        elif(self.strarrCheck(select, failPrint=False)):
            option = 'arr'
        else:
            return self.__err_print__("should be either a string or array of strings", varID='select', **kwargs)

        if(self.__not_str_print__(start_dir, varID='start_dir', **kwargs)):
            return False

        if(self.__not_str_print__(end_dir, varID='start_dir', **kwargs)):
            return False

        if(start_dir not in self.varPath_Folders):
            return self.__err_print__("not a folder in the current directory", varID=start_dir, **kwargs)
        if(end_dir not in self.varPath_Folders):
            return self.__err_print__("not a folder in the current directory", varID=end_dir, **kwargs)

        start_path = self.joinNode(self.varPath, start_dir, **kwargs)
        if(start_path == False):
            return False

        end_path = self.joinNode(self.varPath, end_dir, **kwargs)
        if(end_path == False):
            return False

        if(option == 'str'):
            if(select == 'all'):
                start_content = self.contentPath(start_path, **kwargs)
                if(start_content == False):
                    return self.__err_print__(["content could not be retrieved", "'start_dir' : "+start_dir], varID='start_dir', **kwargs)
            elif(select in self.fileNames):
                start_content = self.contentPath(start_path, objType='file', **kwargs)
                if(start_content == False):
                    return self.__err_print__(["content could not be retrieved", "'start_dir' : "+start_dir], varID='start_dir', **kwargs)
            elif(select in self.dirNames):
                start_content = self.contentPath(start_path, objType='dir', **kwargs)
                if(start_content == False):
                    return self.__err_print__(["content could not be retrieved", "'start_dir' : "+start_dir], varID='start_dir', **kwargs)
            else:
                return self.__err_print__("which files to transfer could not be resolved", **kwargs)

            failure_to_move = []
            for entry in start_content:
                start_obj_path = self.joinNode(start_path, entry, **kwargs)
                if(start_path == False):
                    failure_to_move.append(entry)
                    continue
                end_obj_path = self.joinNode(end_path, entry, **kwargs)
                if(end_path == False):
                    failure_to_move.append(entry)
                    continue
                if(copy):
                    if(os.path.isfile(start_obj_path)):
                        move_success = self.copyFile(start_obj_path, end_obj_path, **kwargs)
                    elif(os.path.isdir(start_obj_path)):
                        move_success = self.copyDir(start_obj_path, end_obj_path, **kwargs)
                    else:
                        failure_to_move.append(entry)
                else:
                    move_success = self.moveObj(start_obj_path, end_obj_path, **kwargs)
                if(move_success == False):
                    failure_to_move.append(entry)
            if(len(failure_to_move) > 0):
                self.__err_print__(["Below is a list of objects reporting error(s) during the move operation:"]+failure_to_move, **kwargs)
        elif(option == 'arr'):
            failure_to_move = []
            for entry in select:
                start_obj_path = self.joinNode(start_path, entry, **kwargs)
                if(start_path == False):
                    failure_to_move.append(entry)
                    continue
                end_obj_path = self.joinNode(end_path, entry, **kwargs)
                if(end_path == False):
                    failure_to_move.append(entry)
                    continue
                if(copy):
                    if(os.path.isfile(start_obj_path)):
                        move_success = self.copyFile(start_obj_path, end_obj_path, **kwargs)
                    elif(os.path.isdir(start_obj_path)):
                        move_success = self.copyDir(start_obj_path, end_obj_path, **kwargs)
                    else:
                        failure_to_move.append(entry)
                else:
                    move_success = self.moveObj(start_obj_path, end_obj_path, **kwargs)
                if(move_success == False):
                    failure_to_move.append(entry)
            if(len(failure_to_move) > 0):
                self.__err_print__(["Below is a list of objects which encoutered an error during the move operation:"]+failure_to_move, **kwargs)
        else:
            return self.__err_print__("which files to transfer could not be resolved", **kwargs)
        return True


    def read_files_from_folder(self, directory, files_to_read, clean=False, **kwargs):

        kwargs = self.__update_funcNameHeader__("read_files_from_folder", **kwargs)

        if(self.__not_str_print__(directory, varID='directory', **kwargs)):
            return False

        if(isinstance(files_to_read, str)):
            files_to_read = [files_to_read]
        elif(self.strarrCheck(files_to_read, failPrint=False)):
            pass
        else:
            return self.__err_print__("should be either a string or an array of strings", varID='files_to_read', **kwargs)

        if(directory not in self.varPath_Folders):
            return self.__err_print__("not a folder in the current directory", varID=directory, **kwargs)

        filepathway = self.joinNode(self.varPath, directory, **kwargs)
        if(filepathway == False):
            return False

        filetext_dict = {}
        failure_to_read = []

        for file in files_to_read:
            entrypathway = self.joinNode(filepathway, file, **kwargs)
            if(entrypathway == False):
                failure_to_read.append(file)
                continue
            if(clean):
                lines = iop.flat_file_grab(entrypathway, scrub=True, **kwargs)
            else:
                lines = iop.flat_file_grab(entrypathway, **kwargs)
            if(lines == False):
                failure_to_read.append(file)
                continue
            else:
                filetext_dict[file] = lines
        if(len(failure_to_read) > 0):
            msg = "Below is a list of files which encoutered an error during the read operation:"
            self.__err_print__([msg]+failure_to_read, **kwargs)
        return filetext_dict

