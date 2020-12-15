
from scipy.interpolate import interp1d as __spln__
from scipy.interpolate import splrep as __bspln__
from scipy.interpolate import splev as __deriv__
from scipy.interpolate import splint as __integ__

from scipy.integrate import quad as __definteg__

import tcheck as check
from tcheck import imprimerTemplate
import strlist as strl

'''
Functions useful for mathmatical operations and plotting, emphasis on parsing floating point variables
'''

#################################################################
# Error Printing Helper functions-------------------------------#
#################################################################

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

def __not_type_print__(var, sort, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.typeCheck(var, sort, **pkwargs)

def __not_numarr_print__(var, numStyle=None, arrStyle=None, firstError=False, varID=None, descriptiveMode=False, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    if(descriptiveMode):
        return printer.numarrCheck(var, numStyle, arrStyle, firstError, descriptiveMode, **pkwargs)
    else:
        return not printer.numarrCheck(var, numStyle, arrStyle, firstError, **pkwargs)

def __update_funcName__(newFuncName, **pkwargs):
    pkwargs = printer.update_funcName(newFuncName, **pkwargs)
    return pkwargs


#################################################################
# Rounding functions -------------------------------------------#
#################################################################


def round_decimal(value, decimal, string=True, **pkwargs):
    '''
    round_decimal(30.112, 1, True)

        value: input file string
        decimal: non-zero integer
        string: (bool)[True] if True, returns String. Else, returns Float
    '''

    pkwargs = __update_funcName__("round_decimal", **pkwargs)

    try:
        value = float(value)
    except:
        __err_print__("must be castable to a float value", varID='value', heading="ValueError", **pkwargs)
        return False

    if(__not_num_print__(decimal, style='int', **pkwargs)):
        return False

    if(decimal < 0):
        __err_print__("should be an integer greater than zero", varID="decimal", **pkwargs)
        return False

    value = float(value)                
    fm = '%.' + str(int(decimal)) + 'f'
    rnum = fm % value

    if(string):
        if(decimal > 0):
            output = str(rnum)
            return output
        else:
            output = str(int(rnum))+'.'
            return output          
    else:
        if(decimal > 0):
            output = float(rnum)
            return output
        else:
            output = int(rnum)
            return output                  


def round_scientific(value, digits, pyver = '2.7', string=True, **pkwargs):
    '''
    Description:

        Takes as inputs a numeric value and the number of significant digits
        to which the the value is rounded when the value is converted to 
        scientific notation

    round_scientific(30.112, 1)

        value: input file string

        decimal: non-zero integer

        digits: a non-negative integer signifying the number of significant digits

        string: (bool)[True] if True, returns String. Else, returns Float
    '''

    # round_scientific(30.112, 1, True)
    # value: input file string

    pkwargs = __update_funcName__("round_scientific", **pkwargs)

    if(__not_num_print__(value, varID='number', heading="warning", **pkwargs)):
        try:
            value = float(value)
        except:
            return False

    if(__not_num_print__(digits, varID='digits', style='int', **pkwargs)):
        return False
    else:
        if(digits <= 0):
            __err_print__("should be an integer greater than zero", varID="digits", **pkwargs)

    if(pyver == '2.7' or pyver == 2.7):
        fm = "{:." + str(int(digits)-1) + "e}"
        rnum = fm.format(value)
    elif(pyver == '2.6' or pyver == 2.6):
        fm = "{0:." + str(int(digits)-1) + "e}"
        rnum = fm.format(value)
    else:
        __err_print__("supported vaules are either '2.7' or '2.6'; '"+str(pyver)+"' not recognized", varID="pyver", **pkwargs)
        return False

    if(string):
        return str(rnum)
    else:
        return float(rnum)


def round_uniform(value, pyver = '2.7', failReturn=True, **pkwargs):

    pkwargs = __update_funcName__("round_uniform", **pkwargs)

    if(isinstance(value, str)):
        try:
            value = float(value)
        except:
            if(failReturn):
                return __err_print__("could not be coerced to a number", varID="value", **pkwargs)
            else:
                return value
    elif(__not_num_print__(value, varID=str(value), heading="error", **pkwargs)):
        if(failReturn):
            return False
        else:
            return value
    else:
        pass

    pos_bool = (value > 0.0)
    neg_bool = (value < 0.0)
    nul_bool = (value == 0.0)

    if(pos_bool):
        if(value < 10000000):
            output = round_decimal(value, 6, **pkwargs)
            for i in range(6):
                if(value > 10.0**(i+1)):
                    output = round_decimal(value, 6-(i+1), **pkwargs)
                    if(i == 6):
                        output = output+'.'
            if(value < 0.000001):
                output = round_scientific(value, 3, pyver, **pkwargs)
        else:
            output = round_scientific(value, 3, pyver, **pkwargs)
    elif(neg_bool):
        if(value > -1000000):
            output = round_decimal(value, 5, **pkwargs)
            for i in range(5):
                if(value < -10.0**(i+1)):
                    output = round_decimal(value, 5-(i+1), **pkwargs)   
                    if(i == 5):
                        output = output+'.'
            if(value > -0.000001):
                output = round_scientific(value, 2, pyver, **pkwargs)
        else:
            output = round_scientific(value, 2, pyver, **pkwargs)
    else:
        output = '0.000000'
    return output


def round_uniform_array(arr, pyver='2.7', failReturn=False, **pkwargs):
    return [round_uniform(entry, pyver, failReturn, **pkwargs) for entry in arr]


def round_format(num, dec, **pkwargs):     
    ''' 

    '''

    pkwargs = __update_funcName__("round_format", **pkwargs)

    if(not isinstance(dec,int)):
        return False 
    else:
        if(dec < 0):
            return False 
        else:
            pass

    if(check.numeric_test(num)):
        pass
    else:
        try:
            if(isinstance(num,str)):
                try:
                    if('.' in num):                    
                        num = float(num)
                    else:
                        num = int(num)
                except:
                    __err_print__("could not be coerced into a numeric type", varID="num", **pkwargs)
                    return False
        except:
            __err_print__("must be castable as a numeric type", varID="num", **pkwargs)
            return False

    f = "{0:."+str(dec)+"f}"

    out_String = f.format(num) 
    return out_String    


def space_format(num, spc, adjust = 'left', **pkwargs):

    def __extra_spaces__(string, extra_Spaces, adjust):
        out_Str = ''
        adjust = adjust.lower()
        if(adjust == 'left'):
            out_Str = extra_Spaces*' '+string
            return out_Str
        if(adjust == 'right'):
            out_Str = string+extra_Spaces*' '
            return out_Str
        if(adjust == 'split'):
            extra_Spaces_Right = extra_Spaces/2
            extra_Spaces_Left = extra_Spaces - extra_Spaces_Right
            out_Str = extra_Spaces_Left*' '+string+extra_Spaces_Right*' '
            return out_Str
        return False

    pkwargs = __update_funcName__("space_format", **pkwargs)

    sci_notation = False
    decimal = False
    negative = False

    output_String = ''
    required_String = ''

    if(not isinstance(num, str)):
        try:
            num = str(num)
        except:
            __err_print__("should be a string, or castable to a string", varID="num")
            return False

    num = num.lower()

    n = len(num)

    if('e' in num or 'd' in num):
        sci_notation = True
    if('.' in num):
        decimal = True
    if('-' in num):
        negative = True

    if(spc > n):
        output_String = __extra_spaces__(num, (spc-len(num)), adjust)
        return output_String
    elif(n > spc):
        numlist = [j for i,j in enumerate(num) if i < spc]
        output_String = strl.array_to_str(numlist, spc='')

        if(sci_notation and ('e' not in output_String or 'd' not in output_String)):
            __err_print__("lost scientific notation markers when parsed thorugh spacer", varID="num", **pkwargs)
            return False
        if(decimal and '.' not in output_String):
            __err_print__("lost decimal place when parsed thorugh spacer", varID="num", **pkwargs)
            return False
        if(negative and '-' not in output_String):
            __err_print__("lost negative sign when parsed thorugh spacer", varID="num", **pkwargs)
            return False

        return output_String
    else:
        return num


def sci_space_format(num, digi, spacing=3, adjust='left', pyver='2.7', **pkwargs):

    def to_float(num, **pkwargs):
        if(not isinstance(num, float)):
            try:
                num = float(num)
                return num
            except:
                __err_print__("could not be coerced to numeric", varID="num", **pkwargs)
                return None
        else:
            return num

    pkwargs = __update_funcName__("sci_space_format", **pkwargs)

    space='    '
    if(__not_num_print__(digi, style='int', **pkwargs)):
        return False
    else:
        if(digi < 1):
            __err_print__("must equal to or greater than 1, setting 'digi' to 1", varID='digi', **pkwargs)
            digi = 1

    value_array = []

    if(isinstance(num,(list,tuple))):
        for i,entry in enumerate(num):
            value = to_float(entry, **pkwargs)
            if(value == None):
                __err_print__("entry index, "+str(i)+", could be converted to a numeric", varID='num', **pkwargs)
                continue
            else:
                value_array.append(value)
    elif(isinstance(num,str)):
        value = to_float(num)
        if(value == None):
            __err_print__("could be converted to a numeric", varID='num', **pkwargs)
            return False
        else:
            value_array.append(value)
    elif(isinstance(num,(float,int,long))):
        value_array.append(num)
    else:
        __err_print__("type, "+str(type(num))+", is not a recognized type", varID='num', **pkwargs)

    if(len(value_array) == 0):
        __err_print__("no values found after parsing 'num' into an array", **pkwargs)
        return False

    for i,entry in enumerate(value_array):
#        try:
        if(abs(value_array[i]) < 10e100):
            spacing_value = digi+5+spacing
        else:
            spacing_value = digi+6+spacing
        value_array[i] = round_scientific(entry, digi, pyver=pyver)
        if(value_array[i] == False):
            __err_print__("could not parse  '"+str(value_array[i])+"' into scientific notation")
            continue
        value_array[i] = space_format(value_array[i], spacing_value, adjust=adjust)    
    return value_array


def span_vec(xvec, nspan, **pkwargs):
    '''
    Description: generates a list which spans the range of numerical
                 array 'xvec' with 'nspan' number of equally spaced floats

    Inputs:

        'xvec' : A python array containing numeric values
        'nspan': The length of the generated spanning array

    Output:

        'span_list' : A list of equally spaced floats spanning the range of 'xvec'
        False       : if an error is detected
    '''

    pkwargs = __update_funcName__("sci_space_format", **pkwargs)

    if(__not_arr_print__(xvec, varID='xvec', **pkwargs)):
        return False
    else:
        if(not all([check.isNumeric(i) for i in xvec])):
            __err_print__("should be an array of numerics", varID='xvec', **pkwargs)
            return False

    if(__not_num_print__(nspan, style='int', **pkwargs)):
        return False
    else:
        if(nspan < 3):
            __err_print__("should be at least equal to 3", varID='nspan', **pkwargs)
            return False

    xl = min(xvec)
    xu = max(xvec)

    if(xl < 0):
        xl = xl-0.0000000001
    elif(xl > 0):
        xl = xl+0.0000000001
    else:
        pass

    if(xu < 0):
        xu = xu+0.0000000001
    elif(xl > 0):
        xu = xu-0.0000000001
    else:
        pass

    if(xl == xu): 
        __err_print__("should be contain at least two different numbers", varID='xvec')
        return False

    inc = (xu-xl)/float((nspan-1))
    span_list = [float(xl)]
    for i in range(nspan-1):
        val = xl+float(i+1)*(inc)
        span_list.append(val) 
    return span_list



class spline(imprimerTemplate):
    '''
    class spline:

        spline(x_array, y_array, x_array = x_points_array)

        A class for performing 1-D spline and calculus operations on 
        discreet arrays of points. 

        A note on usage: this class is only meant to be used as a quick
                         means to estimate splined values or the derivatives
                         and integrals of two sets of data with the relationship,
                         f(X) = Y. This module is not meant to be used when 
                         accuracy is important, nor is it meant to be scalable and 
                         used for a large number of operations. 

        Warning: Interpolation using fuctions called upon splines generated with 
                 scipy must be within the range of the function, scipy functions 
                 in general do not interpolate beyond the range of the input data
    '''

    def __init__(self, space="    ",
                       endline="\n",
                       failPrint=True,
                       x_vec=None,
                       y_vec=None,
                       new_x_vec=None):

        super(spline, self).__init__(space, endline, failPrint)

        self.x_vec = x_vec
        self.y_vec = y_vec

        #Values to be passed
        self.new_x_vec = new_x_vec
        self.spline_inst = None
        self.bspline_inst = None

        #Values to get
        self.spln_array = None
        self.der_array = None
        self.int = None

        #Values for variables
        self.alim = None
        self.blim = None
        self.der = None

    @property
    def x_vec(self):
        return self._x_vec

    @x_vec.setter
    def x_vec(self, vector):
        pkwargs = {}
        pkwargs = self.__update_funcNameHeader__("x_vec", **pkwargs)

        arrcheck, numcheck = self.__not_numarr_print__(vector, varID='x_vec', descriptiveMode=True, **pkwargs)
        if(arrcheck and numcheck):
            self._x_vec = vector
        elif(arrcheck and not numcheck):
            self.__err_print__("will be cast as a numerical array", varID='x_vec', heading='warning', **pkwargs)
            try:
                self._x_vec = map(lambda x: float(x), vector)
            except:
                self.__err_print__("failed to be cast into a numerical array", varID='x_vec', **pkwargs)
                self._x_vec = None
        else:
            self.__err_print__("must be a numerical array", varID='x_vec', **pkwargs)
            self._x_vec = None

    @property
    def y_vec(self):
        return self._y_vec

    @y_vec.setter
    def y_vec(self, vector):
        pkwargs = {}
        pkwargs = self.__update_funcNameHeader__("y_vec", **pkwargs)
        arrcheck, numcheck = __not_numarr_print__(vector, varID='y_vec', descriptiveMode=True, **pkwargs)
        if(arrcheck and numcheck):
            self._y_vec = vector
        elif(arrcheck and not numcheck):
            self.__err_print__("will be cast as a numerical array", varID='y_vec', heading='warning', **pkwargs)
            try:
                self._y_vec = map(lambda x: float(x), vector)
            except:
                __err_print__("failed to be cast into a numerical array", varID='y_vec', **pkwargs)
                self._y_vec = None
        else:
            __err_print__("must be a numerical array", varID='y_vec', **pkwargs)
            self._y_vec = None

    @property
    def new_x_vec(self):
        return self._new_x_vec

    @new_x_vec.setter
    def new_x_vec(self, vector):
        pkwargs = {}
        pkwargs = self.__update_funcNameHeader__("new_x_vec", **pkwargs)
        arrcheck, numcheck = self.__not_numarr_print__(vector, varID='new_x_vec', descriptiveMode=True, **pkwargs)
        if(arrcheck and numcheck):
            self._new_x_vec = vector
        elif(arrcheck and not numcheck):
            self.__err_print__("will be cast as a numerical array", varID='new_x_vec', heading='warning', **pkwargs)
            try:
                self._new_x_vec = map(lambda x: float(x), vector)
            except:
                self.__err_print__("failed to be cast into a numerical array", varID='new_x_vec', **pkwargs)
                self._new_x_vec = None
        else:
            self.__err_print__("must be a numerical array", varID='new_x_vec', **pkwargs)
            self._new_x_vec = None

    @property
    def der(self):
        return self._der

    @der.setter
    def der(self, val):
        pkwargs = {}
        pkwargs = self.__update_funcNameHeader__("der", **pkwargs)
        if(__not_num_print__(val, style='int', varID='der', heading='warning', **pkwargs)):
            try:
                val=int(val)
            except:
                self.__err_print__("could not be evaluated as an integer", varID='der', **pkwargs)
                val = None
        else:
            if(val < 0 or val > 5):
                self.__err_print__("should be an integer between 1 and 5", varID='der', **pkwargs)
                val = None
        self._der = val

    @property
    def alim(self):
        return self._alim

    @alim.setter
    def alim(self, val):
        pkwargs = {}
        pkwargs = self.__update_funcNameHeader__("alim", **pkwargs)
        if(__not_num_print__(val, varID='alim', heading='warning', **pkwargs)):
            try:
                val=float(val)
            except:
                __err_print__("could not be evaluated as an integer", varID='alim', **pkwargs)
                val = None
        self._alim = val

    @property
    def blim(self):
        return self._blim

    @blim.setter
    def blim(self, val):
        pkwargs = {}
        pkwargs = self.__update_funcNameHeader__("blim", **pkwargs)
        if(__not_num_print__(val, varID='blim', heading='warning', **pkwargs)):
            try:
                val=float(val)
            except:
                __err_print__("could not be evaluated as an integer", varID='blim', **pkwargs)
                val = None
        self._blim = val


    def spline(self, x_arr=None, y_arr=None, style='spline', sort='cubic', **pkwargs):

        pkwargs = self.__update_funcNameHeader__("spline", **pkwargs)
        spline_list = ['spline', 'bspline']

        if(x_arr != None and y_arr != None):
            self.x_arr = x_arr
            self.y_arr = y_arr
            if(self.x_arr == None or self.y_arr == None):
                return self.__err_print__("should be numeric arrays", varID="x_arr/y_arr", **pkwargs)
        elif(self.x_arr != None and self.y_arr != None):
            pass
        else:
            self.__err_print__("should be numeric arrays", varID="x_arr/y_arr", **pkwargs)
            return False

        if(style not in spline_list):
            self.__err_print__("is not recognized, defaulting to 'spline'", varID='style', heading='warning', **pkwargs)
            style='spline'

        if(style == 'spline'):
            try:
                self.spline_inst = __spln__(x_arr, y_arr, kind=sort)
                return self.spline_inst
            except:
                return self.__err_print__("failure to generate spline object", **pkwargs)
        elif(style == 'bspline'):
            try:
                self.bspline_inst = __bspln__(x_arr, y_arr)
                return self.bspline_inst
            except:
                return self.__err_print__("failure to generate spline object", **pkwargs)
        else:
            return self.__err_print__("is not recognized: '"+str(style)+"'", varID='style', **pkwargs)


    def interpolate(self, new_x_vec, spline_inst=None, errCheck=True, **pkwargs):

        pkwargs = self.__update_funcNameHeader__("interpolate", **pkwargs)

        if(errCheck):
            if(spline_inst != None):
                if(self.__not_type_print__(spline_inst, __spln__, varID='spline_inst', **pkwargs)):
                    return False
            else:
                if(self.__not_type_print__(self.spline_inst, __spln__, varID='spline_inst', **pkwargs)):
                    return False
                else:
                    spline_inst = self.spline_inst

            if(self.__not_numarr_print__(new_x_vec, varID='new_x_vec', **pkwargs)):
                return False

        try:
            return spline_inst(new_x_vec)
        except:
            return self.__err_print__("failure to parse interpolated value from input", **pkwargs)


    def derivate(self, new_x_vec, bspline_inst=None, der=1, errCheck=True, **pkwargs):

        pkwargs = self.__update_funcNameHeader__("derivate", **pkwargs)

        if(errCheck):
            if(bspline_inst != None):
                if(self.__not_type_print__(bspline_inst, __spln__, varID='bspline_inst', **pkwargs)):
                    return False
            else:
                if(self.__not_type_print__(self.bspline_inst, __spln__, varID='bspline_inst', **pkwargs)):
                    return False
                else:
                    bspline_inst = self.bspline_inst
		    
            if(self.__not_numarr_print__(new_x_vec, varID='new_x_vec', **pkwargs)):
                return False
		    
            if(self.__not_num_print__(der, style='int', varID='der', **pkwargs)):
                return False
            else:
                if(der < 1 or der > 5):
                    return self.__err_print__("must be an integer in the range: 0 < der < 6", varID='der', **pkwargs)

        try:
            return __deriv__(new_x_vec, bspline_inst, der)
        except:
            return self.__err_print__("failure to evaluate the derivative from input", **pkwargs)


    def integrate(self, alim=None, blim=None, bspline_inst=None, errCheck=True, **pkwargs):

        pkwargs = self.__update_funcNameHeader__("integrate", **pkwargs)

        if(errCheck):
            if(bspline_inst != None):
                if(self.__not_type_print__(bspline_inst, __spln__, varID='bspline_inst', **pkwargs)):
                    return False
            else:
                if(self.__not_type_print__(self.bspline_inst, __spln__, varID='bspline_inst', **pkwargs)):
                    return False
                else:
                    bspline_inst = self.bspline_inst

            if(alim == None):
                if(self.__not_num_print__(self.alim, varID='alim', **pkwargs)):
                    return False
                else:
                    alim = self.alim
            else:
                if(self.__not_num_print__(alim, varID='alim', **pkwargs)):
                    return False

            if(blim == None):
                if(self.__not_num_print__(self.blim, varID='blim', **pkwargs)):
                    return False
                else:
                    blim = self.blim
            else:
                if(self.__not_num_print__(blim, varID='blim', **pkwargs)):
                    return False

            if(alim >= blim):
                return self.__err_print__("'alim' must be less than 'blim': (alim,blim) = ("+str(alim)+","+str(blim)+")", **pkwargs)

        try:
            return __integ__(alim, blim, bspline_inst)
        except:
            return self.__err_print__("failure to parse the derivative from input", **pkwargs)


    # SCOS (does not use class variables)

    def scos_interpolate(self, new_x_arr, x_arr, y_arr, der=0, sort='cubic', **pkwargs):

        pkwargs = self.__update_funcNameHeader__("scos_interpolate", **pkwargs)

        if(not isinstance(der,int)):
            try:
                der = int(der)
            except:
                return self.__err_print__("should be a non-negative integer", varID='der', **pkwargs)
        else:
            if(der < 0):
                return self.__err_print__("should be a non-negative integer", varID='der', **pkwargs)

        if(der == 0):
            spline = self.spline(x_arr, y_arr, 'spline', sort, **pkwargs)
            if(spline == False):
                return self.__err_print__("could not be evaluated, check input for errors", varID="spline", **pkwargs)
            return self.interpolate(new_x_arr, spline, **pkwargs)
        else:
            spline = self.spline(x_arr, y_arr, 'bspline', sort, **pkwargs)
            if(spline == False):
                return self.__err_print__("could not be evaluated, check input for errors", varID="spline", **pkwargs)
            return self.derivate(new_x_arr, spline, der, **pkwargs)


    def scos_integrate(self, x_arr, y_arr, alim, blim, **pkwargs):

        pkwargs = self.__update_funcNameHeader__("scos_integrate", **pkwargs)

        spline = self.spline(x_arr, y_arr, 'bspline', sort, **pkwargs)
        if(spline == False):
            return __err_print__("could not be evaluated, check input for errors", varID="spline", **pkwargs)
        integral = self.integrate(alim, blim, spline, **pkwargs)
        return(integral)
