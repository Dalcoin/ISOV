#!/usr/bin/env python
'''
Description: Functions for performing basic IO functions on flat (text) files.


Below is a list of the functions this class offers (w/ input):

    flat_file_read(file_in, ptype='r')

    flat_file_write(file_out, add_list, par=False, ptype='w+')

    flat_file_replace(file_out, grab_list, change_list, count_offset=True, par=True, ptype='w')

    flat_file_grab(file_in, grab_list, scrub=False, repeat=False, count_offset=True, ptype='r')

    flat_file_copy(file_in, file_out, grab_list, repeat=False, group=0, ptype='w')

    flat_file_intable(file_in, header=False)

    flat_file_skewtable(file_in)

'''

import tcheck as check
import pinax as px
import strlist as strl

# Global object intialization
global ptype_list, ptype_read, ptype_write

ptype_list = ['r','r+','rb','w','w+','wb','wb+','a','ab','a+','ab+']
ptype_read = ['r','r+','rb']
ptype_write = ['w','w+','wb','wb+','a','ab','a+','ab+']

printer = check.imprimer()


#################################################################
# Helper functions----------------------------------------------#
#################################################################

def __err_print__(errmsg, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    printer.errPrint(errmsg, **pkwargs)
    return False

def __warn_print__(errmsg, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    printer.warnPrint(errmsg, **pkwargs)
    return False

def __not_str_print__(var, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.strCheck(var, **pkwargs)

def __not_arr_print__(var, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.arrCheck(var, **pkwargs)

def __update_varName__(varName, **pkwargs):
    return printer.update_varName(varName, **pkwargs)

def __update_funcName__(newFuncName, **pkwargs):
    pkwargs = printer.update_funcName(newFuncName, **pkwargs)
    return pkwargs



def __io_test_fail__(ptype, io, **pkwargs):

    pkwargs = printer.update_funcName("__io_test_fail__", **pkwargs)

    success = False
    msg = None

    if(io == 'read'):
        if(ptype not in ptype_read):
            msg = "'"+str(ptype)+"' is not a valid 'ptype' option for reading from a file"
    elif(io == 'write'):
        if(ptype not in ptype_write):
            msg = "'"+str(ptype)+"' is not a valid 'ptype' option for writing to a file"
    else:
        msg = "'"+str(io)+"' is not a valid 'io' option"

    if(isinstance(msg, str)):
        __err_print__(msg, **pkwargs)
        success = True

    return success


def __grab_list_fail__(grab_list, m, repeat=False, change_list=None, **pkwargs):

    pkwargs = printer.update_funcName("__grab_list_fail__", **pkwargs)

    if(__not_arr_print__(grab_list, **pkwargs)):
        return True
    if(change_list != None):
        if(__not_arr_print__(change_list, **pkwargs)):
            return True

    n = len(grab_list)

    # Checks that each entry in 'change_list' is a string
    if(change_list != None):
        for i,entry in enumerate(change_list):
            if(not isinstance(entry, str)):
                pkwargs["varName"] = "change_list"
                __err_print__("input is not a string for array index, "+str(i)+" : "+str(type(entry)), **pkwargs)
                return True
        ngrab = len(change_list)
        nchng = len(change_list)
        if(len(grab_list) != len(change_list)):
            pkwargs["varName"] = "change_list"
            __err_print__("input must be equal in length to 'grab_list'", **pkwargs)
            return True
        if(nchng <= 0):
            pkwargs["varName"] = "change_list"
            __err_print__("no lines selected for change", **pkwargs)
            return True

    if(repeat):
        saut = grab_list[1:-1]
        if(strl.array_duplicate_check(saut)):
            pkwargs["varName"] = "saut"
            __err_print__("values must be unique; see 'help for 'repeat' option details", **pkwargs)
            return True
    else:
        if(strl.array_duplicate_check(grab_list)):
            pkwargs["varName"] = "grab_list"
            __err_print__("values must be unique", **pkwargs)
            return True

    if(n>m):
        pkwargs["varName"] = "grab_list"
        __err_print__("has more values than the number of lines found in the input file", **pkwargs)
        return True
    if(m<(max(grab_list)+1)):
        pkwargs["varName"] = "grab_list"
        __err_print__(": number of line(s) index selected is greater than the number of lines in input files", **pkwargs)
        return True

    if(change_list != None):
        if(n != len(change_list)):
            pkwargs["varName"] = "grab_list"
            __err_print__("; number of replacement lines must be equal to number of lines found in 'change_list'", **pkwargs)
            return True
    return False


def __list_repeat__(grab_list, file_lines, scrub, **pkwargs):
    '''

    variables:

        grab_list : list (int), list of ints for formatting according to 'repeat'

        file_lines : list (str), list of strs which are selected according to 'repeat'

        scrub : True to remove end line and carriage return

        rules for the 'repeat' format for 'grab_list':

    Rules for "repeat": 

        1) The first value of the grab_list is 'bnd' (bind): corrosponding
           to the spacing (binding) the grouped lines togeather: grab_list[0]

        2) The next values of the grab_list are 'saut' (sauter): the first repeat
           instances to be selected from, according to line number: grab_list[1:-1]

        3) The last value of grab_list is 'n' (number): the number of groups to be
           generated. Spacing between groups corrosponds to 'bnd', while
           the grouped values start from the 'saut' line values.

    '''

    pkwargs = printer.update_funcName("__list_repeat__", **pkwargs)

    if(len(grab_list)<3):
        pkwargs["varName"] = "grab_list"
        __err_print__("must have at least 3 entries when using 'repeat' option: "+str(len(grab_list)), **pkwargs)
        return False

    lim = len(file_lines)

    bnd = grab_list[0]+1
    saut = grab_list[1:-1]
    n = grab_list[-1]+1

    if(bnd < 1):
        pkwargs["varName"] = "bnd"
        __err_print__(" (first value of 'grab_list'), must be equal to or greater than 1: "+str(bnd), **pkwargs)
        return False
    if(len(saut) > lim):
        pkwargs["varName"] = "saut"
        __err_print__("(grab_list[1:-1]), must be fewer than the number of file lines"+str(len(saut)), **pkwargs)
        return False
    for i in saut:
        if(i<0):
            pkwargs["varName"] = "saut"
            __err_print__("(grab_list[1:-1]) values should not be negative"+str(i), **pkwargs)
    if(lim < max(saut)+bnd*(n-1)):
        pkwargs["varName"] = "grab_list"
        __err_print__("evaluated with 'repeat' option, exceeds the length of the input file", **pkwargs)
        return False

    raw_lines = []
    for i in range(n):
        for j in saut:
            line_tag = j+bnd*i
            if(scrub):
                raw_lines.append(file_lines[line_tag].rstrip())
            else:
                raw_lines.append(file_lines[line_tag])
    return raw_lines


#########################
#---IOParse functions---#
#########################

def flat_file_read(file_in, ptype='r', type_test=True, **pkwargs):
    '''
    Description: Writes a list of strings (1 line per string) from an input file, various options for parsing

    (e.g.) :

        flat_file_read('file.in', ptype='r')

    Variables:

        'file_in': (str), file string pathway, if only a single node is given, current (path) directory is assumed

        'ptype': (str)['r'], a string corrosponding to a read 'ptype' option, found in the 'ptype_read' list

        'type_test': (bool)[True], If true, the input values will be checked for type and style errors

    Output: List of strings corrosponding to lines of 'file_in', False if error occurs

    '''

    pkwargs = printer.update_funcName("flat_file_read", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(type_test):
        if(__io_test_fail__(ptype, 'read', **pkwargs)):
            return False
        if(__not_str_print__(file_in, varID="file_in",**pkwargs)):
            return False

    try:
        with open(file_in, ptype) as file_in:
            file_lines = file_in.readlines()
        return file_lines
    except:
        pkwargs = __update_varName__("file_in", **pkwargs)
        __err_print__(["could not be read","Filepath : '"+file_in+"'"], **pkwargs)
        return False


def flat_file_write(file_out, add_list=[], par=False, ptype="w+", checkall_addlist=False, type_test=True, **pkwargs):
    '''
    Description: Writes a list of strings to an output file, various options for parsing

    (e.g.)

        flat_file_write('file.in', ["This is the first line!","This is line #2!"])

    Variables:

        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'add_list': (array)[[]] list of strings, each string is a separate line, order denoted by the index
                    if the 'add_list' is empty then an empty file is created

        'par': (bool)[False] True if endline character is to be added to each output string, execpt the last one, else False

        'ptype': (str)['r'] a string corrosponding to a write 'ptype' option, found in the 'ptype_write' list

        'checkall_addlist': (bool)[False] cycles through 'add_list' instead of returning False once a non-string is encountered

        'type_test': (bool)[True], If True, the input values will be checked for type and style errors

    Output: Success Boolean
    '''

    pkwargs = printer.update_funcName("flat_file_write", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(type_test):
        if(__io_test_fail__(ptype, 'write', **pkwargs)):
            return False
        if(__not_str_print__(file_out, varID="file_out", **pkwargs)):
            return False
        if(__not_arr_print__(add_list, varID="add_list", **pkwargs)):
            return False
    n = len(add_list)

    #if(not all([isinstance(entry, str) for entry in add_list]):
    #    return False

    # Write content to file
    try:
        with open(file_out, ptype) as fout:
            for i,entry in enumerate(add_list):
                # Checks that each entry in 'add_list' is a string
                if(not isinstance(entry, str)):
                    pkwargs = __update_varName__("add_list", **pkwargs)
                    __err_print__("input is not a string for array index, "+str(i)+" :"+str(type(entry)) , **pkwargs)
                    if(checkall_addlist):
                        continue
                    else:
                        return False
                if(par):
                    if(i < n-1):
                        fout.write(entry+"\n")
                    else:
                        fout.write(entry)
                else:
                    fout.write(entry)
        return True
    except:
        pkwargs = __update_varName__("file_out", **pkwargs)
        __err_print__(["could not be written to using entries in 'add_list'","Filepath : '"+file_out+"'"], **pkwargs)
        return False


def flat_file_append(file_out, add_list, par=False, newline=True, checkall_addlist=False, type_test=True, **pkwargs):
    '''
    Description: Appends a list of strings to the end of an output file

    (e.g.)

        flat_file_append('file.in', ["\n","This is the second to last line!", "This is the last line!"])

    Variables:

        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'add_list': (array) list of strings, each string is a separate line, order denoted by the index

        'par': (bool)[False] True if endline character is to be added to each output string, else False

        'type_test': (bool)[True], If True, the input values will be checked for type and style errors

    Output: Success Boolean
    '''

    ptype = 'a+'

    pkwargs = printer.update_funcName("flat_file_append", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(type_test):
        if(__io_test_fail__(ptype, 'write', **pkwargs)):
            return False
        if(__not_str_print__(file_out, varID="file_out", **pkwargs)):
            return False
        if(__not_arr_print__(add_list, varID="add_list", **pkwargs)):
            return False

    #if(not all([isinstance(entry, str) for entry in add_list]):
    #    return False

    if(newline):
        add_list = ["\n"]+add_list
    n = len(add_list)

    # Print content to file
    try:
        with open(file_out, ptype) as fout:
            for i,entry in enumerate(add_list):
                # Checks that each entry in 'add_list' is a string
                if(not isinstance(entry, str)):
                    pkwargs = __update_varName__("add_list", **pkwargs)
                    __err_print__("input is not a string for array index, "+str(i)+" :"+str(type(entry)) , **pkwargs)
                    if(checkall_addlist):
                        continue
                    else:
                        return False
                if(par):
                    if(i < n-1):
                        if(newline and i==0):
                            fout.write(entry)
                        else:
                            fout.write(entry+"\n")
                    else:
                        fout.write(entry)
                else:
                    fout.write(entry)
        return True
    except:
        pkwargs = __update_varName__("file_out", **pkwargs)
        __err_print__(["could not be written to using entries in 'add_list'","Filepath : '"+file_out+"'"], **pkwargs)
        return False


def flat_file_replace(file_out, grab_list, change_list, count_offset=True, par=False, type_test=True, **pkwargs):
    '''
    Description: In the file 'file_out', the lines in 'grab_list' are replaced with the strings in 'change_list'

   (e.g.)

       flat_file_replace('file.in', [1,2], ["This is the first line!","This is line #2!"])

    Variables:

        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start

        'change_list': list of strings, each string is a separate line

        'par': [*] True if endline character is to be added to each output string, else False.

        'count_offset': [*] True if values in grab_list corrospond to line numbers, else values corrospond to list index

        'ptype': [*] a string in found in the ptype_write list.

        'type_test': (bool)[True], If True, the input values will be checked for type and style errors

    Output: Success Boolean
    '''

    ptype='w'

    pkwargs = printer.update_funcName("flat_file_replace", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(type_test):
        if(__io_test_fail__(ptype, 'write', **pkwargs)):
            return False
        if(__not_str_print__(file_out, varID="file_out", **pkwargs)):
            return False

        for i,entry in enumerate(grab_list):
            if(not isinstance(entry, int)):
                pkwargs = __update_varName__("grab_list", **pkwargs)
                __err_print__("input is not a string for array index, "+str(i)+" :"+str(type(entry)), **pkwargs)
                return False

    # Accounts for the difference between line number (starting at 1) and python indexing (starting at 0)
    if(count_offset):
        grab_list = [x-1 for x in grab_list]

    #if(not all([isinstance(entry, int) for entry in grab_list]):
    #    return False
    #if(not all([isinstance(entry, str) for entry in change_list]):
    #    return False

    # Read in file
    file_lines = flat_file_read(file_out, type_test=False, **pkwargs)
    if(file_lines == False):
        return False
    else:
        m = len(file_lines)

    # Checking "grab_list" and "change_list" for errors
    if(__grab_list_fail__(grab_list, m, repeat=False, change_list=change_list, **pkwargs)):
        return False

    # Make modifications
    for i in grab_list:
        j = grab_list.index(i)
        if(par):
            file_lines[i] = change_list[j]+"\n"
        else:
            file_lines[i] = change_list[j]

    # Write modifications to file
    result = flat_file_write(file_out, file_lines, ptype=ptype, type_test=False, **pkwargs)
    if(result == False):
        pkwargs = __update_varName__("add_list", **pkwargs)
        __err_print__("couldn't write replacement lines to"+str(file_out), **pkwargs)
    return result


def flat_file_grab(file_in, grab_list=[], scrub=False, repeat=False, count_offset=True, ptype='r', type_test=True, **pkwargs):
    '''
    Description: Grabs the lines in 'grab_list' as strings from the file 'file_in'

   (e.g.)

       flat_file_replace('file.in', [1,2], ["This is the first line!","This is line #2!"])

    Variables:

        'file_in': file string pathway, if only a single node is given, current (path) directory is assumed

        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start

        'scrub': [bool] (False), Removes end and return line characters from each grabbed string

        'repeat': [bool] (False), if True, then 'grouping' formatting is used

        'count_offset': [bool] (True), shifts 'grab_list' values by 1 to align line numbers with python indices

        'ptype': [string] ('r'), reading mode

        'type_test': (bool)[True], If True, the input values will be checked for type and style errors

    Output: List of Strings; Output: Success Boolean
    '''

    pkwargs = printer.update_funcName("flat_file_grab", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    # Testing proper variable types
    if(type_test):
        if(__io_test_fail__(ptype, 'read', **pkwargs)):
            return False
        if(__not_str_print__(file_in, varID="file_in", **pkwargs)):
            return False

        for i,entry in enumerate(grab_list):
            if(not isinstance(entry, int)):
                pkwargs = __update_varName__("grab_list", **pkwargs)
                __err_print__("input is not a string for array index, "+str(i)+" :"+str(type(entry)) , **pkwargs)
                return False

    # Accounts for the difference between line number (starting at 1) and python indexing (starting at 0)
    if(count_offset):
        grab_list = [x-1 for x in grab_list]

    # Read in file
    file_lines = flat_file_read(file_in, type_test=False, **pkwargs)
    if(file_lines == False):
        return False
    else:
        if(scrub):
            file_lines = [entry.rstrip() for entry in file_lines]
#            for i,entry in enumerate(file_lines):
#                file_lines[i] = entry.rstrip()
    if(grab_list == []):
        return file_lines
    m = len(file_lines)

    # Testing the grab_list
    if(__grab_list_fail__(grab_list, m, repeat=repeat, **pkwargs)):
        return False

    # Parse and return file_lines through 'repeat' option:
    out_lines = []

    if(repeat):
        out_lines = __list_repeat__(grab_list, file_lines, scrub, **pkwargs)
        if(out_lines == False):
            return False
    else:
        for index in grab_list:
            if(scrub):
                out_lines.append(file_lines[index].rstrip())
            else:
                out_lines.append(file_lines[index])
    if(scrub):
        filter(None, out_lines)
    return out_lines


def flat_file_copy(file_in, file_out, grab_list=[], repeat=False, group=0, count_offset=True, ptype='w', type_test=True, **pkwargs):
    '''
    Description: Grabs the lines in 'grab_list' as strings from the file 'file_in'
                 the lines in grab_list are then printed to file_out

   (e.g.)

       flat_file_copy('file.in', 'file.out', [1,2])

    Variables:

        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start

        'repeat': [bool] (False), if True, then 'grouping' formatting is used

        'count_offset': [bool] (True), shifts 'grab_list' values by 1 to align line numbers with python indices

        'ptype': [string] ('w'), writing mode

        'type_test': (bool)[True], If True, the input values will be checked for type and style errors

    Output: List of Strings; Output: Success Boolean
    '''

    pkwargs = printer.update_funcName("flat_file_copy", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    # Testing proper variable types
    if(type_test):
        if(__io_test_fail__(ptype, 'write', **pkwargs)):
            return False
        if(__not_str_print__(file_in, varID="file_in", **pkwargs)):
            return False
        if(__not_str_print__(file_out, varID="file_out", **pkwargs)):
            return False
        if(not isinstance(group,int)):
            pkwargs = __update_varName__("group", **pkwargs)
            __err_print__("must be an interger: "+str(type(group)), **pkwargs)

        for i,entry in enumerate(grab_list):
            if(not isinstance(entry, int)):
                pkwargs = __update_varName__("grab_list", **pkwargs)
                __err_print__("input is not a string for array index, "+str(i)+" :"+str(type(entry)), **pkwargs)
                return False

    # Grab appropriate lines (as specified from grab_list and repeat) from 'file_in'
    lines = flat_file_grab(file_in, grab_list, scrub=False, repeat=repeat, count_offset=True, type_test=False, **pkwargs)
    if(lines == False):
            return False

    # Parse and return 'out_lines' through 'repeat' and 'group' options
    out_lines = []
    if(group>0):
        for i,entry in enumerate(lines):
            out_lines.append(entry)
            if(i>0 and (i+1)%group == 0):
                out_lines.append("\n")
    else:
        out_lines = lines

    result = flat_file_write(file_out, out_lines, ptype=ptype, **pkwargs)
    return result


def flat_file_numeric(file_in, option='float', clean=True, float_convert=False, **pkwargs):
    '''
    Purpose: To read in a well constrained table from a text file.

    Inputs:

        file_in : string, corrosponding to a file pathway

        option : string, type of numeric data to be parsed from each line of 'file_in'

    '''

    pkwargs = printer.update_funcName("flat_file_innumeric", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    table_lines = flat_file_grab(file_in, scrub=True, **pkwargs)
    if(table_lines == False):
        return False

    try:
        numeric_lines = map(lambda x: strl.get_floats_from_str(x, option, **pkwargs), table_lines)
    except:
        return __err_print__("failure extract numeric values from '"+str(file_in)+"' line strings", **pkwargs)

    if(clean):
        for i,line in enumerate(numeric_lines):
            if(isinstance(line, (list,tuple))):
                numeric_lines[i] = [strl.replace_char([entry],('d','D'),'e')[0] if 'd' in entry.lower() else entry for entry in line]
    if(float_convert):
        numeric_lines = map(lambda x : [float(entry) for entry in x] if isinstance(x,(list,tuple)) else x, numeric_lines)
    return numeric_lines


def flat_file_intable(file_in, header=False, entete=False, transpose=True, genre=float, **pkwargs):
    '''
    Purpose: To read in a well constrained table from a text file.

    Inputs:

        file_in : python string, corrosponding to a file pathway

        header  : (bool)[False] If True, the first string in the file is treated as a header string

        entete  : (bool)[False] If True and header is True, then the header values are included in the output

        transpose : (bool)[True] If True, lists of the data value are returned by column, else data values are returned by row

        genre   : (type)[float] The variable type of the entries in the table

    '''

    pkwargs = printer.update_funcName("flat_file_intable", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    table_lines = flat_file_grab(file_in, scrub=True, **pkwargs)
    if(table_lines == False):
        return False

    table_num = px.table_str_to_numeric(table_lines, header=header, entete=entete, transpose=transpose, genre=genre, **pkwargs)
    return table_num


def flat_file_skewtable(file_in, 
                        space = '    ', 
                        fill='NULL', 
                        nval = False,
                        numeric = True,
                        header = False, 
                        entete = False, 
                        transpose = True, 
                        nanopt = True, 
                        nantup = (True,True,True),
                        spc = ' ',
                        genre = float,
                        debug = True,
                        **pkwargs):
    '''
    Purpose: To read in a skewed table from a text file. 

    Inputs:

        file_in : python string, corrosponding to a file pathway

        see 'table_str_to_fill_numeric' in the pinax.py file for details on the options
    '''

    pkwargs = printer.update_funcName("flat_file_skewtable", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    table_lines = flat_file_grab(file_in, scrub=True, **pkwargs)
    if(table_lines == False):
        return False

    table_num = px.table_str_to_fill_numeric(table_lines, 
                                             space = space,
                                             fill = fill, 
                                             nval = nval,
                                             header = header, 
                                             entete = entete, 
                                             transpose = transpose, 
                                             nanopt = nanopt, 
                                             nantup = nantup,
                                             spc = spc, 
                                             genre = genre,
                                             debug = True,
                                             **pkwargs)
    return table_num


def iop_help(string, **pkwargs):
    '''

    '''
    pkwargs = printer.update_funcName("iop_help", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(__not_str_print__(string, varID='string')):
        return None

    string = strl.str_filter(string.lower()," ")

    help_list = ['help',
                 'flat_file_read',
                 'flat_file_write',
                 'flat_file_replace',
                 'flat_file_grab',
                 'flat_file_copy',
                 'flat_file_intable',
                 'flat_file_skewtable',
                 'repeat',
                ]

    help_action = [None,

                   "(Input: path string, output: list) Reads the content of a \n"+
                   "flat (text) file line-by-line, each entry in output list\n"+
                   " corrosponds to a line in the file",

                   "(Input: path string; list of strs, output: bool) Writes the\n"+
                   "contents of a list of strings to a file line-by-line so that\n"+
                   "the string index (+1) corrosponds to the file line at the\n"+
                   "path string.\n",

                   "(Input: path string; list of ints; list of strs, output: bool)\n"
                   "Replaces lines at line numbers found in grab_list with entries\n"
                   "found in change_list.\n",

                   "(Input: path string; list of ints, output: list of strs)\n"+     
                   "Grabs the line numbers as text strings as specified in the grab_list\n"+
                   "and returns them as a list of strings. Option 'repeat' for advanced\n"+  
                   "selection of repeating group of lines spaced by a constant\n"+  
                   "number of lines.\n",
  
                   "(Input: path_string; path_string; list of ints, output: bool)\n"+
                   "copies lines from 'file_in' to 'file_out'. The lines which are\n"+ 
                   "copied are deterined by 'grab_list' and 'repeat' options. An\n"+ 
                   "empty grab_list list results in the entire 'file_in' being copied.\n",

                   "(Input: file_in; header = False)\n"+                        
                   "Reads in values from a text file, attempts to formate the results\n"+
                   "as a 'pinax' table.\n"
                   ]

    help_dict = dict(zip(help_list, help_action))

    if(string == 'help'):
        strl.print_fancy(help_list, header = "Valid 'help' strings: ")
        return None
    else:
        try: 
            strl.print_fancy(help_dict[string], header = string+" documentation:")
            return None 
        except:
            print("Error : input string '"+string+"' could not be evaluated, use 'help' for input suggestions")
            return None
            
        