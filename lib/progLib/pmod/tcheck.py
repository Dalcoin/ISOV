#!/usr/bin/env python
'''
'tcheck' module dependencies:

    re

Description: A selection of functions for aiding with error checking
             by searching for TypeError, each function returns either
             a None type or Bool type or Str type for error message.

function list:

    isNumeric(obj)
    isArray(obj)
    isArrayFlat(obj)
    isType(var,sort)
    isType_print(var, sort, var_name=None, func_name='', print_bool=True)

    internal:

        __fail_print__(success, var_name=None, correct_type="valid type", func_name='', print_bool = True)

class list:

    imprimer:

        update_funcName : adds 'funcName' object to pkwargs
        update_varName : sets 'varName' object to pkwargs
        setstop_funcName : sets a stop to adding the function name onto 'funcName' object, overwritten if 'fullErrorPath' is set to True
        errPrint : prints error message
        arrCheck : check if input object is python array (list or tuple), prints error message if not
        numCheck : check if input object is python numeric object (int, float or long), prints error message if not
        strCheck : check if input object is python string object, prints error message if not

Directions:

    1) at the beginning of each new function:
        run 'update_funcName' (input name of the new function as a string)

    2):
        for each major function, run setstop_funcName

    3) for each error message:
        run 'update_varName' (input name of variable for each error message)
    
'''

import re

### Tester functions: test input against a given object type or object format


# Regex codes:

re_funcName_list_from_string = re.compile('\[(.*?)\]')

# Modules functions
    
def isNumeric(obj):
    '''
    Description: A 'numeric' type is defined as an object which evaluates to a python number

    obj: input, any python object
    '''    
    return isinstance(obj, (int, float, long))


def isString(obj):
    '''
    Description: An string is a python 'str' object

    obj: input, any python object
    '''
    return isinstance(obj, str)


def isArray(obj):
    '''
    Description: An 'array' is defined as a iterable and numerically indexed object: lists and tuples

    obj: input, any python object
    '''
    return isinstance(obj, (list, tuple))


def isNumArr(obj):
    '''
    Description: A 'numeric array' is defined as an 'array' for which every entry is a 'numeric'

    obj: input, any python object
    '''
    if(not isArray(obj)):
        return False
    return all([isNumeric(entry) for entry in obj])


def isStrArr(obj):
    '''
    Description: A 'string array' is defined as an 'array' for which every entry is a 'string'

    obj: input, any python object
    '''
    if(not isArray(obj)):
        return False
    return all([isString(entry) for entry in obj])


def isArrayFlat(obj): 
    '''
    Description: Tests an array for flatness (each object within the array has a dimensionality of zero)

    obj: input, any python object    
    ''' 
    if(isArray(obj)):
        for i in obj:
            try:
                n = len(i)
                if(isinstance(i,str)):
                    continue
                else:
                    return False
            except:
                continue
        return True
    else:
        return False

# Printing Functions: Help with printing

def __fail_print__(success, var_name=None, correct_type="valid type", func_name='', print_bool = True):
    '''
    Dunder printing function for internal error correction and checking
    '''
    if(print_bool):
        if(isinstance(correct_type,str)):
            correct_type = correct_type
        else:
            try:
                correct_type = str(correct_type)
            except:
                print("[__fail_print__] Error: 'correct_type' must be a string or type object")
                return False
        if(not success and var_name != None):
            if(func_name == ''):
                print("TypeError: the variable '"+var_name+"' is not a "+correct_type)
            else:
                print("["+func_name+"]"+" TypeError: the variable '"+var_name+"' is not a "+correct_type)
            return False
        if(not success and var_name == None):
            if(func_name == ''):
                print("TypeError: input variable is not a "+correct_type)
            else:
                print("["+func_name+"]"+" TypeError: input variable is not a "+correct_type)
            return False 
        return True       
    else:
        return None   

### Main functions 

def isType(var, sort):
    '''
    Description: This function returns a boolean, 'var' is tested for equivalence to 
                 'sort', 'sort' may a 'type' object.  

    Inputs:
    
        var  : input object 
        sort : sort is either a type, class object or module object against which 'var' is tested
                
    '''

    if(sort == None):
        type_bool = (var == sort)
    elif(sort == 'num'):
        type_bool = isNumeric(var)
    elif(sort == 'arr'):
        type_bool = isArray(var)
    elif(isinstance(sort, type) or type(sort) == "<type 'classobj'>" or type(sort) == "<type 'module'>"):
        type_bool = isinstance(var, sort)
    else:
        type_bool = False
    return type_bool


def isType_print(var, sort, var_name=None, func_name='', print_bool=True):
    '''
    Description: This function returns a boolean, 'var' is tested for equivalence to
                 'sort', 'sort' may a 'type', 'classobj' or 'module' object. The main
                 difference between this function and 'isType' is that this function
                 is optimized for printing out error functions

    Inputs:

        'var'  : python object, input object
        'sort' : sort is either a type, class object or module object against which 'var' is tested
        'var_name' : string, The name of variable 'var', to be used when printing error messages.
        'func_name' : string,  The name of a function, to be used when printing error messages.
        'print_bool' : boolean, printing option, useful when printing to the console would interfere with threading

    '''
    type_bool = isType(var, sort)
    if(print_bool):
        test = __fail_print__(type_bool, var_name, correct_type=sort, func_name=func_name)
        return test
    else:
        return type_bool


class imprimer(object):

    def __init__(self, space="    ", endline="\n", failPrint=True):
        '''
        space : string added at the beginning of error messages

        endline : string added at the end of error messages

        failPrint : True if messages to be printed to console

        kwarg list:

            failPrint : (bool)[True], determines if the output strings are printed (True) or not (False)

            newSpace : (str)(bool)['    '], determines the string which appears at the beginning of the message,
                                         nothing is added for False

            endline : (bool)[False], determines if the endline character is added to the end of each string (True) or not (False)

            funcName : (str)(None)[None], determines the function id strings to be added to the beginning of each string (str),
                                          if None, or not a string then nothing is added

            funcNameHeader : (str)(None)[None], adds a node to the beginning of each 'funcName' string

            heading : (str)(bool)[" Error"], determines the string to be added which identifies the message (str),
                                            if True, the string " 'Error'" is added, else if False, nothing is added

            varName : (str)(bool)[False], determines the string to be added which identifies a specific variable (str),
                                        if True, the string " 'variable'" is added, else if False, nothing is added

            lnum : (str)(int)(None)[None], determines the strings to be added for identifying the line for which the message
                                           applies (str)(int), if None then nothing is added

            blankLine : (bool)[True], determines if an extra blank line is to added between the heading and following lines
                                       if 'msg' input is an array of strings. The blank line is not added if False

            doubleSpace : (bool)[True], determines if an extra 'space' spacing string is to added to the beginning of each
                                        line if the 'msg' input is an array of strings. The spacing defaults to that which is
                                        determined by 'space' if False.

            parSpace : (bool)[True], adds extra line to space out printing list of strings

            nonewFuncName : (bool)[False], prevents referenced functions from added their name to the 'funcName' list

            fullErrorPath : (bool)[False], overrides any existing blocks which might prevent nested function from adding
                                           their name to 'funcName' list


        '''

        if(isinstance(space, str)):
            self.space = space
            self.doubleSpace = space+space
        else:
            self.space = '    '
            self.doubleSpace = space+space

        if(isinstance(endline, str)):
            self.endline = endline
        else:
            self.endline = "\n"

        if(failPrint):
            self.failPrint = True
        else:
            self.failPrint = False

    def __kwarg2bool__(self, kwarg):
        if(kwarg != None):
            return True
        else:
            return False

    def funcName_list2str(self, funcName):
        if(not isArray(funcName)):
            return False
        outString=''
        for entry in funcName:
            outString = outString+"["+str(entry)+"]"
        outString = outString+" "
        return outString

    def funcName_str2list(self, funcName):
        '''
        Description: Takes a properly formatted 'funcName' string and turns it into a 'funcName' list

        Rules:

            'funcName' string takes the format: '(\[\.*?\])'
        '''
        if(isString(funcName)):
            return re_funcName_list_from_string.findall(funcName)
        else:
            return False

    def update_funcName(self, funcNameNode, **kwargs):
        '''
        Run the 'pkwargs' through this function when parsing through each new function in the chain
        '''
        if(not isString(funcNameNode) and not isArray(funcNameNode)):
            return kwargs
        elif(isString(funcNameNode)):
            if("[" not in funcNameNode and "]" not in funcNameNode):
                funcNameNode = "["+funcNameNode+"]"
            funcNameNode = self.funcName_str2list(funcNameNode)
            if(funcNameNode == False):
                return False
        else:
            pass

        funcName = kwargs.get("funcName")
        if(funcName == None):
            funcName = []

        nonewFuncName = kwargs.get("nonewFuncName")

        if(kwargs.get("fullErrorPath")):
            kwargs["nonewFuncName"] = False

        if(nonewFuncName):
            if(funcName == None):
                kwargs["funcName"] = funcNameNode
        else:
            kwargs["funcName"] = funcName+funcNameNode

        return kwargs

    def update_funcNameHeader(self, funcNameHeader, addFuncNameHeader=False, **kwargs):

        if(addFuncNameHeader):
            if(isString(kwargs.get("funcNameHeader"))):
                old_funcNameHeader = kwargs["funcNameHeader"]
        else:
            old_funcNameHeader = ''

        if(isString(funcNameHeader)):
            if("[" not in funcNameHeader and "]" not in funcNameHeader):
                new_funcNameHeader = "["+funcNameHeader+"]"
            kwargs["funcNameHeader"] = old_funcNameHeader+new_funcNameHeader
            return kwargs
        elif(isStrArr(funcNameHeader)):
            new_funcNameHeader = self.funcName_list2str(funcNameHeader)
            kwargs["funcNameHeader"] = old_funcNameHeader+new_funcNameHeader
            return kwargs
        else:
            return kwargs

    def setstop_funcName(self, inverse=False, **kwargs):
        '''
        Run this function to halt any adding of new functions names to the chain, 'fullErrorPath' will overwrite this
        '''
        if(not inverse):
            if(kwargs.get("nonewFuncName") == None):
                kwargs["nonewFuncName"] = True
        else:
            if(kwargs.get("nonewFuncName") == None):
                kwargs["nonewFuncName"] = False
        return kwargs


    def update_varName(self, varName, **kwargs):
        if(not isinstance(kwargs.get("varName"), str)):
            kwargs["varName"] = varName
        elif(varName == None):
            kwargs["varName"] = None
        else:
            pass
        return kwargs

    def __stringParse__(self, msg, **kwargs):
        '''
        Description: Parses 'msg' input message(s) into string output
        '''

        if(kwargs.get('failPrint') == None):
            failPrint = self.failPrint
        else:
            failPrint = kwargs.get('failPrint')

        newSpace = kwargs.get('newSpace')
        if(isinstance(newSpace, str)):
            outString = newSpace
            doubleSpace = newSpace+newSpace 
        elif(newSpace == False):
            newSpace = ''
            outString = newSpace
            doubleSpace = newSpace+newSpace 
        else:
            newSpace = self.space
            outString = self.space
            doubleSpace = newSpace+newSpace 

        parSpace = kwargs.get('parSpace')
        if(parSpace != False):
            parSpace = True
        else:
            parSpace = False

        endlineVal = ''
        if(isinstance(kwargs.get('endline'), str)):
            endlineAdd = True
            endlineVal = kwargs.get('endline')
        elif(kwargs.get('endline')):
            endlineAdd = True
            endlineVal = self.endline
        else:
            endlineAdd = False

        funcNameStr = self.funcName_list2str(kwargs.get('funcName'))
        funcNameHeader = kwargs.get('funcNameHeader')
        if(isString(funcNameStr)):
            if(isString(funcNameHeader)):
                outString = outString+funcNameHeader
            outString = outString+funcNameStr

        if(self.__kwarg2bool__(kwargs.get('heading'))):
            if(isinstance(kwargs.get('heading'), str)):
                outString = outString+kwargs.get('heading')+":"
            elif(kwargs.get('heading') != False):
                outString = outString+"Error:"
            else:
                pass
        else:
            outString = outString+":"

        if(self.__kwarg2bool__(kwargs.get('varName'))):
            if(isinstance(kwargs.get('varName'),str)):
                outString = outString+" '"+kwargs.get('varName')+"'"
            elif(kwargs.get('varName')):
                outString = outString+" 'variable'"
            else:
                pass

        lnum_kwarg = kwargs.get('lnum')
        if(isinstance(lnum_kwarg, int) or isinstance(lnum_kwarg, str)):
            outString = outString+" on line-num. "+str(kwargs.get('lnum'))+")"

        outStrings = []
        if(isinstance(msg, str)):
            outString = outString+" "+msg
            if(endlineAdd):
                outString = outString+endlineVal
        elif(isArray(msg)):

            if(len(msg) == 0):
                if(endlineAdd):
                    outString = outString+endlineVal
            elif(len(msg) == 1):
                if(endlineAdd):
                    outString = outString+" "+msg[0]+endlineVal
                else:
                    outString = outString+" "+msg[0]
            else:
                first = msg[0]
                rest = msg[1:]

                outString = outString+" "+first
                if(endlineAdd):
                    outString = outString+endlineVal
                outStrings.append(outString)

                if(kwargs.get('blankLine') != False):
                    if(endlineAdd):
                        outStrings.append(" "+endlineVal)
                    else:
                        outStrings.append(" ")

                if(kwargs.get('doubleSpace') != False):
                    startString = doubleSpace
                else:
                    startString = newSpace

                for entry in rest:
                    if(isinstance(entry, str)):
                        entryString = startString+entry
                    else:
                        continue

                    if(endlineAdd):
                        entryString = entryString+endlineVal
                    outStrings.append(entryString)
        else:
            return False

        if(failPrint):
            if(len(outStrings) > 0):
                for string in outStrings:
                    print(string)
                if(parSpace):
                    print(" ")
                return outStrings
            else:
                print(outString)
                if(parSpace):
                    print(" ")
                return outString
        else:
            if(outStrings > 0):
                return outStrings
            else:
                return outString


    def errPrint(self, msg, **kwargs):
        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Error"
        outString = self.__stringParse__(msg, **kwargs)
        return outString

    def warnPrint(self, msg, **kwargs):
        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Warning"
        outString = self.__stringParse__(msg, **kwargs)
        return outString


    def numCheck(self, var, style=None, **kwargs):

        if(style == None):
            isNumeric = isinstance(var,(int,float,long))
            typeText = "numeric [int, float or long]"
        elif(style == 'int'):
            isNumeric = isinstance(var, int)
            typeText = "integer [int]"
        elif(style == 'float'):
            isNumeric = isinstance(var, float)
            typeText = "floating point [float]"
        elif(style == 'long'):
            isNumeric = isinstance(var, long)
            typeText = "long integer [long]"
        else:
            isNumeric = isinstance(var,(int,float,long))
            typeText = "numeric [int, float or long]"

        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Error"

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = True

        if(isNumeric == False):
            printString = "should be a "+typeText+", not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return isNumeric
        else:
            return isNumeric


    def strCheck(self, var, **kwargs):
        isStringTest = isinstance(var, str)

        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Error"

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = True

        if(isStringTest == False):
            printString = "should be a string, not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return isStringTest
        else:
            return isStringTest


    def typeCheck(self, var, sort, **kwargs):

        typeTest = isType(var, sort)

        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Error"

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = True

        if(typeTest == False):
            printString = "should be a "+str(sort)+", not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return typeTest
        else:
            return typeTest


    def arrCheck(self, var, style=None, **kwargs):

        if(style == None):
            isArr = isinstance(var,(list,tuple))
            typeText = "array [tuple or list]"
        elif(style == "list"):
            isArr = isinstance(var, list)
            typeText = "mutable array [list]"
        elif(style == "tuple"):
            isArr = isinstance(var, tuple)
            typeText = "immutable array [tuple]"
        else:
            isArr = isinstance(var,(list,tuple))
            typeText = "array (tuple or list)"

        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Error"

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = 'var'

        if(isArr == False):
            printString = "should be a(n) "+typeText+", not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return isArr
        else:
            return isArr


    def numarrCheck(self, var, numStyle=None, arrStyle=None, firstError=False, descriptiveMode=False, **kwargs):

        switch=False
        if(not self.arrCheck(var, style=arrStyle, **kwargs)):
            if(descriptiveMode):
                return (False, False)
            else:
                return False

        if(isString(kwargs.get('varName'))):
            var_name = kwargs['varName']
        else:
            var_name = 'var'

        fail_list = ["contains errors at the following indices:"]
        for i,entry in enumerate(var):

            if(numStyle == None):
                isNumeric = isinstance(entry,(int,float,long))
                typeText = "numeric [int, float or long]"
            elif(numStyle == 'int'):
                isNumeric = isinstance(entry, int)
                typeText = "integer [int]"
            elif(numStyle == 'float'):
                isNumeric = isinstance(entry, float)
                typeText = "floating point [float]"
            elif(numStyle == 'long'):
                isNumeric = isinstance(entry, long)
                typeText = "long integer [long]"
            else:
                isNumeric = isinstance(entry,(int,float,long))
                typeText = "numeric [int, float or long]"

            if(isNumeric == False):
                fail_line = "'"+str(i)+"' index"
                if(firstError):
                    if(descriptiveMode):
                        return (True, False)
                    else:
                        return False
                switch=True
                fail_list.append(fail_line+" should be a(n) "+typeText+", not: "+str(type(entry)))

        if(switch):
            self.__stringParse__(fail_list, **kwargs)
            if(descriptiveMode):
                return (True, False)
            else:
                return False
        else:
            if(descriptiveMode):
                return (True, True)
            else:
                return True


    def strarrCheck(self, var, arrStyle=None, firstError=False, descriptiveMode=False, **kwargs):

        switch=False
        if(not self.arrCheck(var, style=arrStyle, **kwargs)):
            if(descriptiveMode):
                return (False, False)
            else:
                return False

        if(isString(kwargs.get('varName'))):
            var_name = kwargs['varName']
        else:
            var_name = 'var'

        isStringTest = False
        fail_list = ["contains errors at the following indices:"]
        for i,entry in enumerate(var):
            isStringTest = isinstance(entry, str)

            if(isStringTest == False):
                fail_line = "'"+str(i)+"' index"
                if(firstError):
                    if(descriptiveMode):
                        return (True, False)
                    else:
                        return False
                switch=True
                fail_list.append(" should be a 'str', not: "+str(type(entry)))

        if(switch):
            self.__stringParse__(fail_list, **kwargs)
            if(descriptiveMode):
                return (True, False)
            else:
                return False
        else:
            if(descriptiveMode):
                return (True, True)
            else:
                return True


class imprimerTemplate(imprimer):

    '''
    List of Functions:

        Erroor message functions:

            __err_print__
            __not_str_print__
            __not_arr_print__
            __not_num_print__
            __not_type_print__
            __not_numarr_print__
            __not_strarr_print__

        Setting internal kwargs:

            __update_funcName__
            __set_funcNameHeader__
            __update_funcNameHeader__
    '''

    def __init__(self, space="    ", endline="\n", failPrint=True):
        super(imprimerTemplate, self).__init__(space, endline, failPrint)
        self.headerStr = ''

    def __err_print__(self, errmsg, varID=None, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        self.errPrint(errmsg, **pkwargs)
        return False

    def __not_str_print__(self, var, varID=None, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        return not self.strCheck(var, **pkwargs)

    def __not_arr_print__(self, var, varID=None, style=None, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        return not self.arrCheck(var, style, **pkwargs)

    def __not_num_print__(self, var, varID=None, style=None, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        return not self.numCheck(var, style, **pkwargs)

    def __not_type_print__(self, var, sort, varID=None, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        return not self.typeCheck(var, sort, **pkwargs)

    def __not_numarr_print__(self, var, varID=None, numStyle=None, arrStyle=None, firstError=False, descriptiveMode=False, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        if(descriptiveMode):
            return self.numarrCheck(var, numStyle, arrStyle, firstError, descriptiveMode, **pkwargs)
        else:
            return not self.numarrCheck(var, numStyle, arrStyle, firstError, **pkwargs)

    def __not_strarr_print__(self, var, varID=None, firstError=False, descriptiveMode=False, **pkwargs):
        if(isinstance(varID, str)):
            pkwargs["varName"] = varID
        if(descriptiveMode):
            return self.strarrCheck(var, firstError, descriptiveMode, **pkwargs)
        else:
            return not self.strarrCheck(var, firstError, **pkwargs)

    def __update_funcName__(self, newFuncName, **pkwargs):
        pkwargs = self.update_funcName(newFuncName, **pkwargs)
        return pkwargs

    def __set_funcNameHeader__(self, string, **pkwargs):
        pkwargs = self.__update_funcName__("__set_funcNameHeader__")
        if(self.__not_str_print__(string, varID='funcNameHeader', **pkwargs)):
            return None
        else:
            self.headerStr = string

    def __update_funcNameHeader__(self, newFuncName, **pkwargs):
        if(pkwargs.get("funcNameHeader") != None):
            pass
        else:
            pkwargs = self.update_funcNameHeader(self.headerStr, **pkwargs)
        pkwargs = self.update_funcName(newFuncName, **pkwargs)
        return pkwargs