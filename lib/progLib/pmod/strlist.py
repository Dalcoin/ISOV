#!/usr/bin/env python

import itertools
import collections
import re

import tcheck as check

'''
A python module which faciliates working with list, lists of strings and strings

function list:

    |---helper functions--------------------------

    __isArray__(array)
    __isNumeric__(array)

    |---array functions--------------------------- 

    array_duplicate_check(array)
    array_duplicates(array, inverse = False)

    array_filter(array, match, reverse=False)
    array_filter_spaces(array, filter_none=True)

    array_to_str(array, spc = ' ', print_bool=True)
    array_matrix_to_array_str(array, spc = '  ')

    array_nth_index(array, n, inverse_filter = False,list_form = True)
    array_flatten(array, safety = True, out_type = list)

    |---string functions--------------------------- 

    str_space_check(string, none_bool = False)
    str_to_list(string, split_val = ' ', filt = False, cut = None)

'''

#################################################################
# Error Printing Helper functions-------------------------------#
#################################################################

global printer

printer = check.imprimer()

def __err_print__(errmsg, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    printer.errPrint(errmsg, **pkwargs)
    return False

def __not_str_print__(var, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.strCheck(var, **pkwargs)

def __not_arr_print__(var, varID=None, style=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.arrCheck(var, style, **pkwargs)

def __not_num_print__(var, varID=None, style=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.numCheck(var, style, **pkwargs)

def __not_numarr_print__(var, varID=None, numStyle=None, arrStyle=None, firstError=False, descriptiveMode=False, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    if(descriptiveMode):
        return printer.numarrCheck(var, numStyle, arrStyle, firstError, descriptiveMode, **pkwargs)
    else:
        return not printer.numarrCheck(var, numStyle, arrStyle, firstError, **pkwargs)

def __not_strarr_print__(var, varID=None, firstError=False, descriptiveMode=False, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    if(descriptiveMode):
        return printer.strarrCheck(var, firstError, descriptiveMode, **pkwargs)
    else:
        return not printer.strarrCheck(var, firstError, **pkwargs)

def __update_funcName__(newFuncName, **pkwargs):
    pkwargs = printer.update_funcName(newFuncName, **pkwargs)
    return pkwargs

### Internal Helper Functions

def __isArray__(array):
    return isinstance(array, (tuple, list))

def __isNumeric__(num):
    return isinstance(num, (int,float,long))

#######################
### array functions ###
#######################

# checking and modifying arrays by content:

def array_duplicate_check(array, varID=None, **pkwargs):
    '''
    Description: Checks for duplicates in an array-like object
                 If duplicates are found, True is returned
                 Else, False is returned
                 If input is not an array, None is returned

    Inputs:

        'array' : a list or tuple to be checked for duplicates

    '''
    pkwargs = __update_funcName__("array_duplicate_check", **pkwargs)
    if(__not_arr_print__(array, varID, **pkwargs)):
        return None

    collection = []
    for entry in array:
        if entry in collection:
            return True
        else:
            collection.append(entry)
    return False


def array_duplicates(array, varID=None, inverse=False, count=False, index=False, **pkwargs):
    '''
    Description: Checks for duplicates in an array-like object
                 If duplicates are found, a list of the duplicate values is returned
                 Else an empty list is returned

    Warnings: Unhashable types are excluded

    Inputs:

        array : (list or tuple), The array which is to be checked for duplicates

        inverese : (bool) [False], Returns the non-duplicated values in the array

        count : (bool) [False], Returns a dictionary with each key index corrosponding
                                to each value in 'array' and the corrosponding value
                                index equal to the number of times that that key appears

        index : (bool) [False], Returns a dictionary with each key index corrosponding
                                to each value in 'array' and the corrosponding value
                                index equal to a list of integer indicies for which the
                                'array' entry appears within the array

    Returns:

        (ci, dup_list)

        ci : (tuple), a tuple containing index and/or count dictionary, else an empty tuple

        dup_list : (list), a list of duplicate objects in 'array', else an empty list

        False, if an error is detected

    |--------------------|
    |---exampli gratia---|
    |--------------------|

    array = [1,2,2,4,3,3,3]

    ci, dup_list = array_duplicates(array, count=True, index=True)
    indicies, counts = ci

    ---

    dup_list = [2,3]

    indicies = {1: [0],
                2: [1, 2],
                3: [4, 5, 6],
                4: [3]}

    counts = {1: 1,
              2: 2,
              3: 3,
              4: 1}
    '''

    pkwargs = __update_funcName__("array_duplicates", **pkwargs)
    if(__not_arr_print__(array, varID, **pkwargs)):
        return False

    s = []
    dupList = []
    inv = []

    countDict = {}
    indexDict = {}

    for i,entry in enumerate(array):
        if(not isinstance(entry, collections.Hashable)):
            continue
        if entry in s:
            if(entry not in dupList):
                dupList.append(entry)
            if(count and inverse==False):
                countDict[entry] = countDict[entry]+1
            if(index and inverse==False):
                indexDict[entry] = indexDict[entry]+[i]
        else:
            s.append(entry)
            if(count and inverse==False):
                countDict[entry] = 1
            if(index and inverse==False):
                indexDict[entry] = [i]
    if(inverse):
        for i,entry in enumerate(array):
            if(not isinstance(entry, collections.Hashable)):
                continue
            if(entry in s and entry not in dupList):
                inv.append(entry)
                if(count):
                    countDict[entry] = 1
                if(index):
                    indexDict[entry] = [i]
        if(count or index):
            if(count and not index):
                return (countDict, inv)
            elif(index and not count):
                return (indexDict, inv)
            else:
                return ((indexDict, countDict), inv)
        else:
            return ((), inv)
    else:
        if(count or index):
            if(count and not index):
                return (countDict, dupList)
            elif(index and not count):
                return (indexDict, dupList)
            else:
                return ((indexDict, countDict), dupList)
        else:
            return ((), dupList)


def array_filter(array, match, varID=None, inverse=False, index=False, **pkwargs):
    '''
    Description: returns input array filtered of any values found in 'match'

    Inputs:

        array : (tuple or list), an array to be filtered of 'match' entries

        match : (tuple, list or entry value), if 'match' is an array the
                entry of the arrays are filtered from 'array', else 'match'
                value is filtered from the array

        inverse : (bool) [False], if True every entry not equivalent to 'match'
                  is filtered from the array
    '''

    pkwargs = __update_funcName__("array_filter", **pkwargs)
    if(__not_arr_print__(array, varID, **pkwargs)):
        return False

    outArray = []
    if(inverse):
        if(__isArray__(match)):
            for i,entry in enumerate(array):
                if(entry not in match):
                    continue
                else:
                    if(not index):
                        outArray.append(entry)
                    else:
                        outArray.append((i,entry))
        else:
            for i,entry in enumerate(array):
                if(entry != match):
                    continue
                else:
                    if(not index):
                        outArray.append(entry)
                    else:
                        outArray.append((i,entry))
    else:
        if(__isArray__(match)):
            for i,entry in enumerate(array):
                if(entry in match):
                    continue
                else:
                    if(not index):
                        outArray.append(entry)
                    else:
                        outArray.append((i,entry))
        else:
            for i,entry in enumerate(array):
                if(entry == match):
                    continue
                else:
                    if(not index):
                        outArray.append(entry)
                    else:
                        outArray.append((i,entry))
    return outArray


def array_filter_spaces(array, varID=None, none_filter=True, inverse=False, **pkwargs):
    '''
    Description: Returns non-space string elements of 'array', in 'inverse'
                 is True, only space-string elements of 'array' are returned
    '''

    pkwargs = __update_funcName__("array_filter_spaces", **pkwargs)
    if(__not_arr_print__(array, varID=varID, **pkwargs)):
        return False

    nonSpaceList = []
    spaceList = []

    for entry in array:
        if(str(entry).isspace() or entry == ''):
            if(inverse):
                spaceList.append(entry)
        else:
            if(not inverse):
                nonSpaceList.append(entry)
    if(none_filter):
        if(inverse):
            return filter(None, SpaceList)
        else:
            return filter(None, nonSpaceList)
    else:
        if(inverse):
            return SpaceList
        else:
            return nonSpaceList


def array_to_str(array, varID=None, spc=' ', endline=False, filtre=False, front_spacing='', **pkwargs):
    '''
    Description: Turns array of string elements into a single string
                 each entry is space by 'spc' spacing value. If
                 'endline' is True then '\n' is added to the end of
                 the output string. If 'print_bool' is True, any
                 error's that are raised will print an error message
                 to the console. 

    Input:

        array : (list or tuple), A 1-D Python array object

        spc : (string) [' '],  A string object, usually spacing

        endline : (bool) [False], If True, a endline character is added to the output string

    Return:

        out_str : A string if success, False if failure
    '''

    pkwargs = __update_funcName__("array_to_str", **pkwargs)
    if(__not_arr_print__(array, varID=varID, **pkwargs)):
        return False

    out_str = ''

    if(filtre):
        array = filter(None, array)

    for i, entry in enumerate(array):
        if(i == 0):
            out_str = out_str+str(entry)
        else:
            out_str = out_str+str(spc)+str(entry)

    if(endline):
        out_str = out_str+"\n"
    if(front_spacing != '' and isinstance(front_spacing, str)):
        out_str = front_spacing+out_str

    return out_str


def array_nth_index(array, n, varID=None, inverse=False, byCount=False, **pkwargs):
    '''
    Description: Takes an input array and outputs a list corrosponding 
                 to the value found at every nth index of input array

    Input:

        array : (list or tuple), the array for entries to be selected by index

        n : (int), the integer corrosponding to the modulus determining which
            index values are selected from 'array'. Default includes the first
            entry in the array and then includes every nth value thereafter
            if "byCount" is True, every nth value in the list is returned

        inverese : (bool) [False], If true then the all values of 'array' are
                   returned except for those at each 'n'th value of the index.

    Return:
        out_array : A list of strs if success, False if failure
    '''

    pkwargs = __update_funcName__("array_nth_index", **pkwargs)
    if(__not_arr_print__(array, varID=varID, **pkwargs)):
        return False

    array_len = len(array)

    if(__not_num_print__(n, varID="n", style='int', **pkwargs)):
        return False
    else:
        if(n <= 1 or n>(array_len/2)):
            __err_print__("is only valid for 1 < n < len('array')/2: "+str(n), varID="n", **pkwargs)
            return False

    try:
        if(inverse):
            if(byCount):
                out_object = [entry for i,entry in enumerate(array) if (i+1)%n==0]
            else:
                out_object = itertools.ifilter(lambda x: array.index(x)%n, array)
        else:
            if(byCount):
                out_object = [entry for i,entry in enumerate(array) if (i+1)%n==0]
            else:
                out_object = itertools.ifilterfalse(lambda x: array.index(x)%n, array)
    except:
        __err_print__("could not be filtered", varID=varID, **pkwargs)
        return False

    out_list = [entry for entry in out_object]
    return out_list


def hack_flatten(array):
    str_array = str(array)
    ignore_tup = ('[',']',' ')
    final_str = ''

    string_str = ''
    strtrap = True
    strcount = 0
    comma=False

    for char in str_array:
        if(char != "'" and strtrap):
            if(char not in ignore_tup):
                if(char == ',' and comma):
                    continue
                elif(char != ',' and comma):
                    comma=False
                    final_str+=char
                    continue
                else:
                    final_str+=char
            if(char==","):
                comma=True
        else:
            if(strcount==0):
                add_str = "'"
                strtrap = False
            else:
                add_str = char
            string_str += add_str
            strcount+=1
            if(add_str == "'" and strcount>1):
                strtrap = True
                strcount = 0
                final_str += string_str
                string_str = ''
                comma=False
    if(len(final_str) > 0):
        if(final_str[0] == ","):
            final_str = final_str[1:]
        if(len(final_str) > 1):
            if(final_str[-1] == ","):
                final_str = final_str[:-1]
    
    exec("output_array = ["+final_str+"]")
    return output_array


def rec_flatten(array):
    iterm = iter(array)
    for item in iterm:
        if __isArray__(item):
            for initem in rec_flatten(item):
                yield initem
        else:
            yield item


def array_flatten(array, varID=None, method="hack", **pkwargs):
    '''
    Warning: this function uses 'exec' and is inherently insecure if input is allowed from the user.

    Description: Attempts to flatten (reduce dimension by one) input array.

    Inputs:

        array: (tuple or list), the tuple or list to be flattened

        method: (string)["hack"]

            "hack" : uses a non-standard method for flattening the input array

            "rec" : uses a standard recursive method for flattening the input array

            "twod" : assumes the input array is two-dimensional for simplicity and speed
    '''

    def twod_flatten(array):
        return [i for j in array for i in j]

    pkwargs = __update_funcName__("array_flatten", **pkwargs)
    if(__not_arr_print__(array, **pkwargs)):
        return False

    exe_dict = {'hack':hack_flatten, 'rec':rec_flatten, '2d':twod_flatten}

    try:
        flat_array = exe_dict[method.rstrip().lower()](array)
    except:
        __err_print__("could not be flattened, method: "+str(method), varID="array", **pkwargs)
        return False

    return flat_array


### string functions 

# string content

def str_space_check(string, varID=None, none_bool=False, space='    ', **pkwargs):
    '''
    Description: checks if a string is all empty spaces (endline characters included)
    '''
    pkwargs = __update_funcName__("str_space_check", **pkwargs)

    if(not isinstance(string, (str, type(None)))):
        __err_print__("should be string type, None type is allowed if 'none_bool' option : "+str(type(string)), varID="string", **pkwargs)
        return None
    else:
        if(none_bool and string==None):
            return True
        elif(string==None):
            __err_print__("should be string type, None type only allowed if 'none_bool' option : "+str(type(string)), varID="string", **pkwargs)
            return None
        else:
            pass

    try:
        checker = string.isspace() or string == ''
        return checker
    except:
        return None


def str_to_list(string, spc=' ', filtre=False, cut=None, **pkwargs):
    '''
    Description: parses input string into a list, default demarcation is by single spacing
    '''
    pkwargs = __update_funcName__("str_to_list", **pkwargs)

    if(not isinstance(string, str)):
        mod_string = str(string)
    else:
        mod_string = string

    try:
        if(filtre):
            return filter(cut, mod_string.split(spc))
        else:
            return mod_string.split(spc)
    except:
        __err_print__("could not be converted (split -> filtered) to list", varID="string", **pkwargs)
        return False


def str_to_fill_list(string,
                     lngspc='    ',
                     fill='NaN',
                     nval=False,
                     spc=' ',
                     numeric=False,
                     **pkwargs):
    '''
    Purpose : To turn python string, 'string', into a list of numeric characters, with support
              for blank entries, input options allow for compatability with multiple
              formatting situations and scenarios

    Inputs:

        string : a python 'str' object

        lngspc : a python 'str' object, intended to be the number of blank spaces denoting a blank entry
                 default : '    ', 4 blank spaces

        fill   : a python 'str' object, intended to be the filler value for blank entries
                 default : 'NaN', Not a Number string

        nval   : either boolean False, or an integer greater than zero, intended to be
                 the number of numeric and blank entries in 'string', also the length of the
                 array into which the function will attempt to coerce the string
                 default : False, boolean False

        spc    : a python string object, intended to be the value for which the seperated entries within
                 'string' are determined, possibly a delimiter character, note that non-entry empty spaces
                 are deleted upon splitting 'string'
                 default : ' ', a single space character

        numeric: a python 'bool' or python 'str' object, If True then non-filled spaces are mapped to floats
                 If 'numeric' is a string, it must corrospond to the type to which non-filled entries are
                 coerced into, valid options are 'str', 'int' and 'float'
                 default : False
    '''
    def __cut__(arr, n, fill):

        cut = True 
        while(cut):
            if(arr[-1] == fill and len(arr) > n):
                del arr[-1]
            else:
                cut = False 
        if(len(arr)>n):
            cut = True 
            while(cut):
                if(arr[0] == fill and len(arr) > n):
                    del arr[0]
                else:
                    cut = False                 
        if(len(arr) == n):
            return arr 
        else:
            print("Warning, output array could not be coerced into 'nval' number of entries")
            return arr

    # Function start
    spc1 = ' '

    pkwargs = __update_funcName__("str_to_fill_list", **pkwargs)

    if(__not_str_print__(string, varID="string", **pkwargs)):
        return False

    # Where all the machinery is
    replace_value = spc1+str(fill)+spc1
    try:
        newline = string.replace(lngspc,replace_value)
    except:
        __err_print__("failure to replace '"+str(lngspc)+"' with '"+replace_value+"'", varID="string", **pkwargs)
        return False

    try:
        newarr = filter(None, newline.split(spc))
    except:
        __err_print__("failure to filter 'None' values from'"+str(newline)+"'", varID="string:newline", **pkwargs)
        return False

    flatarr = array_flatten(newarr, varID="newarr", **pkwargs)
    if(flatarr == False):
        return False

    if(not isinstance(flatarr,list)):
        return flatarr

    if(isinstance(nval,int)):
        if(nval > 0 and len(flatarr) > nval):
            flatarr = __cut__(flatarr, nval, fill)

    # conditions bound by the numeric formatter
    if(numeric):
        try:
            flatarr = map(lambda x: float(x) if x != fill else x, flatarr)
        except:
            flatarr = False
    elif(isinstance(numeric, str)):
        if(numeric.lower() == 'float'):
            try:
                flatarr = map(lambda x: float(x), flatarr)
            except:
                flatarr = False
        elif(numeric.lower() == 'int'):
            try:
                flatarr = map(lambda x: int(x), flatarr)
            except:
                flatarr = False
    return flatarr


def str_filter_char(string, filtre, inverse=False, **pkwargs):
    '''
    Description: Filters single character 'filtre' string(s) out of 'string' 
                 string, if 'inverse' then the instances of 'filtre' are returned
                 else the entries not equivalent to 'filtre' are returned
    '''
    pkwargs = __update_funcName__("str_filter_char", **pkwargs)

    if(__not_str_print__(string, varID='string', **pkwargs)):
        return False

    out_list = []
    if(inverse):
        for i in string:
            if(__isArray__(filtre)):
                if(i in filtre):
                    out_list.append(i)
            else:
                if(i == filtre):
                    out_list.append(i)       
    else:
        if(__isArray__(filtre)):
            for i in string:
                if(i not in filtre):
                    out_list.append(i)
        else:
            for i in string:
                if(i != filtre):
                    out_list.append(i)

    out_str = array_to_str(out_list, spc = '', **pkwargs)
    return out_str


def str_clean(string, **pkwargs):
    '''
    Description : Removes all spaces, endline characters and newline characters from string
    '''
    pkwargs = __update_funcName__("str_clean", **pkwargs)

    if(__not_str_print__(string, varID='string', **pkwargs)):
        return False

    array = str_to_list(string.rstrip(), filtre=True, **pkwargs)
    if(__not_arr_print__(array, varID="array", **pkwargs)):
        return False

    out_string = array_to_str(array, spc = '', **pkwargs)
    return out_string


def str_set_spacing(string, space=' ', **pkwargs):
    '''
    Description: spaces non-space substrings by a set amount

    (e.g.)  'Hey,        Hello    World'  - becomes -  'Hey, Hello World'
    '''
    pkwargs = __update_funcName__("str_set_spacing", **pkwargs)

    try:
        if(__not_str_print__(string, varID='string', **pkwargs)):
            return False
        array = str_to_list(string, filtre=True, **pkwargs)
        if(__not_arr_print__(array, varID="array (array conversion)", **pkwargs)):
            return False
        output = array_to_str(array, spc=space, **pkwargs)
        return output
    except:
        return False





### Formatting and Printing Functions

def format_fancy(obj, header=None, newln=True, indt=4, err=True, list_return=False, **pkwargs):

    pkwargs = __update_funcName__("format_fancy", **pkwargs)

    if(newln):
        nl = '\n'
    else:
        nl = ''

    spc = indt*' '

    stylized_list = []

    if(__isArray__(obj)):
        if(list_return):
            stylized_list.append(' \n')
        else:
            print(' ')
        if(isinstance(header, str)):
            out_val = header+nl
            if(list_return):
                stylized_list.append(out_val)
            else:
                print(out_val)
        for entry in obj:
            out_val = spc+str(entry)+nl
            if(list_return):
                stylized_list.append(out_val)
            else:
                print(out_val)
        if(list_return):
            stylized_list.append(' \n')
            return stylized_list
        else:
            print(' ')
            return None

    elif(isinstance(obj,str)):
        if(list_return):
            stylized_list.append(' \n')
        else:
            print(' ')
        if(isinstance(header,str)):
            out_val = spc+header+nl
            if(list_return):
                stylized_list.append(out_val)
            else:
                print(out_val)
        out_val = obj+nl
        if(list_return):
            stylized_list.append(out_val)
            return stylized_list
        else:
            print(out_val)
            return None
    else:
        __err_print__("should be a 'str' type or 'arr' type, not "+str(type(obj)), varID="obj", heading="TypeError", **pkwargs)
        return False


def print_border(string, style=('-','|'), newln=True, cushion=0, indt=0, comment=None, autoprint=False, **pkwargs):

    pkwargs = __update_funcName__("print_border", **pkwargs)
    if(__not_str_print__(string, varID="string", **pkwargs)):
        return False

    n = len(string)

    if(newln):
        nl = '\n'
    else:
        nl = ''

    spr = 2*cushion+(cushion/1)*2+(cushion/2)*2+(cushion/4)*2
#    tnb = 4*style[0]+(n+2*cushion)*style[0]
    blnk= style[1]+(2+spr+n)*' '+style[1]
    tnb = len(blnk)*style[0]
    mid = style[1]+(1+spr/2)*' '+string+(1+spr/2)*' '+style[1]

    if(isinstance(indt,int) and indt >= 0):
        blnk = indt*' '+blnk
        tnb = indt*' '+tnb
        mid = indt*' '+mid

    if(isinstance(comment,str)):
        blnk = comment+blnk
        tnb = comment+tnb
        mid = comment+mid

    stylized_list = []
    if(autoprint):
        print(tnb)
    stylized_list.append(tnb+nl)
    for i in range(cushion):
        if(autoprint):
            print(blnk)
        stylized_list.append(blnk+nl)
    if(autoprint):
        print(mid)
    stylized_list.append(mid+nl)
    for i in range(cushion):
        if(autoprint):
            print(blnk)
        stylized_list.append(blnk+nl)
    if(autoprint):
        print(tnb)
    stylized_list.append(tnb+nl)

    return stylized_list       


def print_ordinal(n, **pkwargs):

    pkwargs = __update_funcName__("print_ordinal", **pkwargs)

    chg = ['1','2','3']
    dictn = {'1':'st','2':'nd','3':'rd'}

    if(__isNumeric__(n)):
        if(not isinstance(n,int)):
            n = int(n)
    elif(isinstance(n,str)):
        try:
            n = int(float(n))
        except:
            __err_print__("must be castable to an integer", varID='n', **pkwargs)
            return str(n)
    else:
        return str(n)

    if(str(n) in chg):
        return str(n)+dictn[str(n)]
    else:
        return str(n)+'th'



# String match functions

def replace_char(strings, characters, replacement, test=False, return_string=True, **pkwargs):
    pkwargs = __update_funcName__("replace_char", **pkwargs)
    if(test):

        if(__not_strarr_print__(strings, varID='strings', **pkwargs)):
            if(__not_str_print__(strings, varID='strings', **pkwargs)):
                return False
            else:
                strings = [strings]

        if(__not_strarr_print__(characters, varID='characters', **pkwargs)):
            if(__not_str_print__(characters, varID='characters', **pkwargs)):
                return False
            else:
                characters = [characters]

        if(__not_str_print__(replacement, varID='replacement', **pkwargs)):
            return False
    else:
        if(not isinstance(strings, (tuple,list))):
            strings = [strings]
        if(not isinstance(characters, (tuple,list))):
            characters = [characters]

    return_list = []
    for string in strings:
        if(any(character in string for character in characters)):
            if(return_string):
                return_list.append(array_to_str([replacement if entry in characters else entry for entry in string], spc=''))
            else:
                return_list.append([replacement if entry in characters else entry for entry in string])
        else:
            return_list.append(string)
    return return_list


def get_floats_from_str(string, option=None, **pkwargs):

    pkwargs = __update_funcName__("get_floats_from_str", **pkwargs)

    if(__not_str_print__(string, varID='string', **pkwargs)):
        return False

    if(option == None or option == 'charfloat'):
        return re.findall(recharffloat, string)
    elif(option == 'float'):
        return re.findall(reffloat, string)
    elif(option == 'integer' or option == 'int'):
        return re.findall(reint, string)
    else:
        return __err_print__("should be one of the following: ['charfloat', 'float', 'int']", varID='option', **pkwargs)