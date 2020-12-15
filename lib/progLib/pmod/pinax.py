import re

import strlist as strl
import tcheck as check
import mathops as mops

global printer
global re_space
global nan_list, inf_list, null_list, truth, nil, truth_dict, match_dict

nan_list = ['nan', 'NaN', 'NAN', '-nan', '-NaN', '-NAN']
inf_list = ['inf', 'Inf', 'INF', '-inf', '-Inf', '-INF']
null_list = ['null', 'Null', 'NULL', '-null', '-Null', '-NULL']

truth = ('nan','inf','null')
nil = (nan_list, inf_list, null_list)

match_dict = dict(zip(truth,nil))

re_space = re.compile("^\s+$")

printer = check.imprimer()

#################################################################
# Helper functions----------------------------------------------#
#################################################################

def __err_print__(errmsg, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    printer.errPrint(errmsg, **kwargs)

def __not_str_print__(var, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    return not printer.strCheck(var, **kwargs)

def __not_arr_print__(var, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    return not printer.arrCheck(var, **kwargs)

def __not_num_print__(var, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    return not printer.numCheck(var, **kwargs)

####################                         ####################
#  line functions  ###########################  line functions  #
####################                         ####################

###################
#  NAN functions  #
###################

def __nan_func__(check_list):
    check_type = []
    truth_dict = dict(zip(truth,check_list))
    for i in truth:
        if(truth_dict[i]):
            check_type+=match_dict[i]
    return check_type


def nan_check(string, nan=True, inf=True, null=True, **pkwargs):

    if(not isinstance(string, str)):
        try:
            string = str(string)
        except:
            pkwargs["varName"] = "string"
            __err_print__("is not castable to a python 'str'", **pkwargs)
            return False

    check_list = (nan, inf, null)
    check_type = __nan_func__(check_list)
    
    if(string in check_type):
        return True
    else:
        return False


def line_nan_check(array, nan=True, inf=True, null=True, **pkwargs):

    if(__not_arr_print__(array, varID="array", **pkwargs)):
        return False

    check_list = (nan, inf, null)
    check_type = __nan_func__(check_list)

    index_list = []
    for i,entry in enumerate(array):
        if(entry in check_type):
            index_list.append(i)
        else:
            pass

    if(len(index_list) > 0):
        return index_list
    else:
        return False


###################                           ###################
# table functions ############################# table functions #
###################                           ###################

# Table (pinax) functions
# These functions are the main function to be used on matrix arrays.

# Format:
#
# The format for tables takes the following basic form: [[],[]]
#
# Functions:
#
# table_trans  ([[1,2,3],[4,5,6]])  =>  [[1,4],[2,5],[3,6]]


def ismatrix(n, typeRestriction=None, matrixName=None, **pkwargs):
    '''
    Description:

    Inputs:

        typeRestriction:
            if 'str' : each element is checked as a string, False is returned if any element is a non-string
            if 'num' : each element is checked as a numeric, False is returned if any element is a non-numeric

        matrixName : If a string, then error messages use this string as the name of the input matrix
    '''

    pkwargs = printer.update_funcName("ismatrix", **pkwargs)

    mID=''
    if(isinstance(matrixName, str)):
        mID = matrixName
    else:
        mID = "n"

    if(__not_arr_print__(n, varID=mID, **pkwargs)):
        return False

    string=False
    numeric=False

    if(isinstance(typeRestriction, str)):
        if(typeRestriction.lower() == 'str'):
            string=True
        elif(typeRestriction.lower() == 'num'):
            numeric=True
        else:
            pass

    lang = 0
    err = False
    for i,entry in enumerate(n):
        if(__not_arr_print__(entry, varID="The "+strl.print_ordinal(i+1)+" entry of '"+mID+"'", **pkwargs)):
            return False
        else:
            if(i == 0):
                lang = len(entry)

            if(numeric):
                err_arr = [str(j) for j in entry if not check.isNumeric(j)]
            elif(string):
                err_arr = [str(j) for j in entry if not isinstance(j, str)]
            else:
                err_arr = [str(j) for j in entry if not check.isNumeric(j) and not isinstance(j, str)]

            if(len(err_arr)>0):
                err_msg = ["Below is the invalid content in the "+strl.print_ordinal(i+1)+" entry of "+mID+":"]+err_arr
                __err_print__(err_msg, **pkwargs)
                err=True
            if(len(entry) != lang):
                errString_p1 = "length of the "+strl.print_ordinal(i+1)+" entry of '"+mID
                __err_print__(errString_p1+"' doesn't match the length of the first entry", **pkwargs)
                err=True
                continue
    if(err):
        return False
    else:
        return True


def coerce_to_matrix(n, fill="NULL", matrixName=None, **pkwargs):
    '''
    Description : Attempts to convert an array of arrays into a rectangular array of arrays
                  Filling is added to the ending of each array
    '''

    pkwargs = printer.update_funcName("coerce_to_matrix", **pkwargs)

    mID=''
    if(isinstance(matrixName, str)):
        mID = matrixName
    else:
        mID = "n"

    if(__not_arr_print__(n, varID=mID, **pkwargs)):
        return False

    newn = list(n)
    maxl = 0

    err = False
    for i,entry in enumerate(newn):
        if(__not_arr_print__(entry, varID="The "+strl.print_ordinal(i+1)+" entry of '"+mID+"'", **pkwargs)):
            err = True
            continue
        if(len(entry) > maxl):
            maxl = len(entry)
    if(err):
        return False

    for i,entry in enumerate(newn):
        if(len(entry) < maxl):
            while(len(newn[i]) < maxl):
                newn[i].append(fill)
    return newn

#**********************
def matrix_to_str_array(array,
                        spc='  ',
                        matrixName=None,
                        endline=False,
                        frontSpacing='',
                        roundUniform=False,
                        strOpt=True,
                        pyver='2.7',
                        **pkwargs):
    '''
    Description: Takes a matrix (2-D array of arrays) and returns a 1-D array; 'outArray'
                 Each entry in 'outArray' is a string corrosponding to the original entry
                 in 'array' parsed through the function 'array_to_str'

    Input:
        array   : A 2-D Python array (list or tuple) object
        spc [*] : A string object, usually spacing
        matrixName [*] : A string object, used for the name of the variable when printing error messages
        endline [*] : If True then the endline character '\n' is added to the end of each string
        frontSpacing [*] : A string object to be added to the beginning of each string
        strOpt [*] : 
        roundUniform [*] : Round each numeric value in the matrix to a uniform length of 8 characters

    Return:
        out_array : A list of strs if success, False if failure
    '''

    pkwargs = printer.update_funcName("matrix_to_str_array", **pkwargs)

    mID=''
    if(isinstance(matrixName, str)):
        mID = matrixName
    else:
        mID = "n"

    if(__not_arr_print__(array, varID=mID, **pkwargs)):
        return False

    outArray = []

    for i,entry in enumerate(array):
        if(roundUniform):
            line = strl.array_to_str(mops.round_uniform_array(entry, pyver, failPrint=False, **pkwargs),
                                     spc=spc, endline=endline, front_spacing=frontSpacing, **pkwargs)
            if(isinstance(line,str)):
                outArray.append(line)
            else:
                msg = "failure to create a string of rounded numerics from the "+strl.print_ordinal(i)+" entry of 'array'"
                __err_print__(msg, **pkwargs)
        elif(strOpt):
            if(isinstance(entry, str)):
                outArray.append(entry)
            elif(check.isArray(entry)):
                string = strl.array_to_str(entry, spc=spc, endline=endline, front_spacing=frontSpacing)
                if(string == False or string == None):
                    __err_print__(strl.print_ordinal(i+1)+" entry, could not be converted to string", varID=mID, **pkwargs)
                    return False
                outArray.append(string)
            else:
                __err_print__(strl.print_ordinal(i+1)+" entry, is not an array", varID=mID, **pkwargs)
                return False
        else:
            if(__not_arr_print__(array, varID="The "+strl.print_ordinal(i+1)+" entry of '"+mID+"'", **pkwargs)):
                return False
            else:
                string = strl.array_to_str(entry, spc=spc, endline=endline, front_spacing=frontSpacing)
                if(string == False or string == None):
                    __err_print__(strl.print_ordinal(i+1)+" entry, could not be converted to string", varID=mID, **pkwargs)
                    return False
                outArray.append(string)
    return outArray


def table_trans(n, test_matrix=True, coerce=False, fill='NULL', typeRestriction=None, matrixName=None, **pkwargs):

    pkwargs = printer.update_funcName("table_trans", **pkwargs)

    matrix_assert = True
    if(test_matrix):
        if(coerce):
            if(not isinstance(pkwargs.get("failPrint"), bool)):
                pkwargs["failPrint"] = False
                oldval=None
            else:
                pkwargs["failPrint"] = False
                oldval=pkwargs["failPrint"]
        if(not ismatrix(n, typeRestriction=typeRestriction, matrixName=matrixName, **pkwargs)):
            matrix_assert = False
        if(coerce):
            pkwargs["failPrint"] = oldval

    if(coerce and not matrix_assert):
        n = coerce_to_matrix(n, fill=fill, matrixName=matrixName, **pkwargs)
        if(n == False):
            return False
    elif(not matrix_assert):
        return False
    else:
        pass

    nrow = len(n[0])
    new_matrix, new_row = [],[]

    for k in range(nrow):
        for i in n:
            new_row.append(i[k])
        new_matrix.append(new_row)
        new_row=[]

    return new_matrix


def table_from_str_array(table_list, test_matrix=True, spc=' ', transpose=True, matrixName=None, string=False, **pkwargs):

    mID=''
    if(isinstance(matrixName, str)):
        mID = matrixName
    else:
        mID = "table_list"

    pkwargs = printer.update_funcName("table_from_str_array", **pkwargs)

    if(test_matrix):
        if(not ismatrix(table_list, numeric=False, string=string, matrixName=matrixName, **pkwargs)):
            return False

    for i,entry in enumerate(table_list):
        try:
            table_list[i] = filter(None, entry.split(spc))
        except:
            __err_print__(strl.print_ordinal(i+1)+" entry, is not an array", varID=mID, **pkwargs)
            return False
        if(len(table_list[i]) == 0 or (len(table_list[i]) == 1 and table_list[i][0].isspace())):
            del table_list[i]

    if(transpose):
        return table_trans(table_list, **pkwargs)
    else:
        return table_list


def table_str_to_numeric(table_list,
                         header=False,
                         entete=False ,
                         transpose=True,
                         nanopt=True,
                         nantup=(True,True,True),
                         spc=' ',
                         genre=float,
                         matrixName=None,
                         debug=True,
                         **pkwargs):
    '''
    Input Variables:

        table_list : A python array (list or tuple) of strings which form a numeric table (header option allowed)
        header    : If True, treats the first line in the input array as a header and not with the data
        entete    : If header, attempts to return the header with the output numeric table
        transpose : If True, attempts to return transposed data parsed from 'table_list'
        nanopt    : If True, 'NaN' values do not return error values
        nantup    : A tuple in the form (nan,inf,null), each value is true if it is allowed
        spc       : string, seperator for numeric values in the input table (',' for CSV, space ' ' is default)
        genre     : A python object function: attempts to coerce object type to 'genre', float is default (str, int)
        debug     : If True, checks performs dummy-check on input data, returns printing of point or location of failure

    Purpose:

        Takes a list of strings and attempts to convert into a table of numeric values
        Useful if working with formatted data tables
    '''

    pkwargs = printer.update_funcName("table_str_to_numeric", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(isinstance(matrixName, str)):
        tableID = matrixName
    else:
        tableID = "table_list"

    try:
        nan,inf,null = nantup
    except:
        __err_print__("incorrectly formatted; should be a tuple of three bools", varID="nantup", **pkwargs)
        return False

    if(debug):
        if(__not_arr_print__(table_list, varID=tableID, **pkwargs)):
            return False

        for i,entry in enumerate(table_list):
            if(__not_str_print__(entry, varID=strl.print_ordinal(i)+" entry of "+tableID, **pkwargs)):
                return False

        if(not isinstance(genre, type)):
            genre = float

    new_table_list = strl.array_filter_spaces(table_list)
    if(new_table_list == False):
        __err_print__("couldn't be filtered", varID=tableID, **pkwargs)
        return False

    if(header):
        head = new_table_list[0]
        new_table_list = new_table_list[1:]
        head = strl.str_to_list(head, spc=spc, filtre=True)
        if(head == False):
            __err_print__("couldn't be parsed with a header (first) entry; failure to convert to 'list'", varID=tableID, **pkwargs)
            return False

    nanopt_test = False
    for i,entry in enumerate(new_table_list):
        new_table_list[i] = strl.str_to_list(entry, spc=spc, filtre=True)
        if(new_table_list[i] == False):
            __err_print__(strl.print_ordinal(i)+" table entry; couldn't be converted to list", varID=tableID, **pkwargs)
            return False
        for j,value in enumerate(new_table_list[i]):
            try:
                if(nanopt):
                    nanopt_test = nan_check(value, nan, inf, null)
                if((genre == int or genre == long) and not nanopt_test):
                    new_table_list[i][j] = genre(float(value))
                elif((genre == float or genre == str) and not nanopt_test):
                    new_table_list[i][j] = genre(value)
                elif(nanopt_test):
                    new_table_list[i][j] = value
                else:
                    ordi = strl.print_ordinal(i)
                    ordj = strl.print_ordinal(j)
                    __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                    return False
            except:
                ordi = strl.print_ordinal(i)
                ordj = strl.print_ordinal(j)
                __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                return False

    if(header and entete):
        try:
            new_table_list.insert(0, head)
        except:
            __err_print__("failure to incorporate header...", varID=tableID, **pkwargs)

    if(transpose):
        return table_trans(new_table_list, test_matrix=False, matrixName=tableID, **pkwargs)
    else:
        return new_table_list


def table_str_to_fill_numeric(table_list,
                              space = '    ',
                              fill  = 'NULL',
                              nval  = False,
                              header=False,
                              entete=True,
                              transpose=True,
                              nanopt=True,
                              nantup=(True,True,True),
                              spc=' ',
                              genre=float,
                              matrixName=None,
                              debug=True,
                              **pkwargs):

    '''
    Description:

        Takes a list of strings and attempts to convert into a table of numeric values
        Useful if working with formatted data tables

    Input Variables:

        table_list : A array (list or tuple) of strings which form a numeric table (header option allowed)

        space     : A string of spaces, corrosponds to the number of spaces required for an empty entry

        fill      : A string, corrosponds to the value which will be added in the place of an empty entry

        nval      : An integer, corrosponds to the number of values in a row, to which the table will be coerced
                    If False, the table is read according to parsed spaces

        header    : If True, treats the first line in the input array as a header and not with the data

        entete    : If header is True, attempts to return the header with the output numeric table

        transpose : If True, attempts to return lists of each transpose of data, rather than each rows as found in 'table_list'

        nanopt    : If True, NaN style strings values do not return error values as specified in nantup

        nantup    : A tuple in the form (nan,inf,null), each value is true if it is allowed

        sep       : A string, seperator for numeric values in the input table (',' for CSV, space ' ' is default)

        genre     : A python object function: attempts to coerce object type to 'genre', float is default

        debug     : If True, checks performs dummy-check on input data, returns printing of point or location of failure

    '''
    pkwargs = printer.update_funcName("table_str_to_fill_numeric", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    if(isinstance(matrixName, str)):
        tableID = matrixName
    else:
        tableID = "table_list"

    try:
        nan,inf,null = nantup
    except:
        __err_print__("incorrectly formatted; should be a tuple of three bools", varID="nantup", **pkwargs)
        return False
    null = True

    if(debug):
        if(__not_arr_print__(table_list, varID=tableID, **pkwargs)):
            return False

        for i,entry in enumerate(table_list):
            if(__not_str_print__(entry, varID=strl.print_ordinal(i)+" entry of "+tableID, **pkwargs)):
                return False

        if(not isinstance(genre, type)):
            genre = float

    if(header):
        head = table_list[0]
        new_table_list = table_list[1:]
        head = strl.str_to_list(head, spc=spc, filtre=True)
        if(head == False):
            __err_print__("couldn't be parsed with a header (first) entry; failure to convert to 'list'", varID=tableID, **pkwargs)
            return False
    else:
        new_table_list = list(table_list)

    # Parsing list of lines
    for i,entry in enumerate(new_table_list):
        temp = strl.str_to_fill_list(entry, lngspc=space, fill=fill, nval=nval, spc=spc, numeric=False)

        # Parsing numeric values found in each list
        if(nanopt):
            nan_list = line_nan_check(temp,nan=nan,inf=inf,null=null)
            if(nan_list > 0):
                for j,value in enumerate(temp):
                    if(value not in nan_list and value != fill):
                        try:
                            temp[j] = genre(temp[j])    
                        except:
                            ordi = strl.print_ordinal(i)
                            ordj = strl.print_ordinal(j)
                            __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                            return False
        else:
            nan_list = line_nan_check(temp, False, False, True)
            if(nan_list > 0):
                for j,value in enumerate(temp):
                    if(value not in nan_list and value != fill):
                        try:
                            temp[j] = genre(temp[j])    
                        except:
                            ordi = strl.print_ordinal(i)
                            ordj = strl.print_ordinal(j)
                            __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                            return False
        new_table_list[i] = temp

    if(header and entete):
        try:
            new_table_list.insert(0, head)
        except:
            __err_print__("failure to incorporate header...", varID=tableID, **pkwargs)

    if(transpose):
        output = table_trans(new_table_list, test_matrix=True, coerce=True, matrixName=tableID, **pkwargs)
        if(output == False):
            return False
        else:
            return output
    else:
        return new_table_list


def skew_str_table_to_matrix(array, header = False, split_str = '  '):

    new_list = list(array)
    for i in range(len(new_list)):
        new_list[i] = new_list[i].split(split_str)
    
    if(header):
        header = new_list[0]
        new_list = new_list[1:-1]
    
    for i in range(len(new_list)):
        for j in range(len(new_list[i])):
            if(new_list[i][j] == ''):
                new_list[i][j] = None
 
        