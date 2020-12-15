#!/usr/bin/env python
'''

Contains : 'minimize'

'minimize' is a class which allows python to communicate with an executable.
The executable must accept an 'n' number of floats passed from a list,
with options for communication values at the beginning and end
of the list of floats. Default values seperate the output float values by an
endline character. The input is also expected to be a float. Options are
available to center the minimization value on zero, or on a given value

'''


import scipy.optimize as sciopt     #import SciPy module with optimization routines
import subprocess as subp           #module for calling subprocesses
import time                         #module with timing functions


class minimize:

    def __init__(self, server = None):

        self.exe_Style = './'
        self.server_Set = False
        self.run_Count = 0

        # Server Parameters
        self.new_Line = True
        self.eval_Print = True
        self.init_Com = 0
        self.term_Com = None
        self.set_Min = '-inf'

        # Minimization parameters

        if(server != None and isinstance(server,str)):
            self.Server = subp.Popen(self.exe_Style+server, stdin = subp.PIPE, stdout = subp.PIPE, stderr = subp.STDOUT)
        else:
            self.Server = None

        if(isinstance(self.Server, subp.Popen)):
            self.server_Set = True
        elif(self.Server == None):
            pass
        else:
            print("[optimize] Error: 'server' input not a valid pipe type and has not been set")

    # Properties

    @property
    def exe_Style(self):
        return self.exe_Style

    @exe_Style.setter
    def exe_Style(self, style, space = False):
        if(isinstance(sytle,str)):
            self.exe_Style = style
            if(space):
                self.exe_Style = self.exe_Style+str(" ")
        else:
            self.exe_Style = './'

    @property
    def Server(self):
        return self.Server

    @Server.setter
    def Server(self, exec_Cmd):
        self.Server = subp.Popen(self.exe_Style+exec_Cmd, stdin = subp.PIPE, stdout = subp.PIPE, stderr = subp.STDOUT)

    @property
    def new_Line(self):
        return self.new_Line

    @new_Line.setter
    def new_Line(self, boolean):
        if(boolean):
            self.new_Line = boolean
        else:
            self.new_Line = bool(boolean)

    @property
    def init_Com(self):
        return self.init_Com

    @init_Com.setter
    def init_Com(self, string):
        self.init_Com = str(string)

    @property
    def term_Com(self):
        return self.term_Com

    @term_Com.setter
    def term_Com(self, string):
        self.term_Com = str(string)

    @property
    def set_Min(self):
        return self.set_Min

    @set_Min.setter
    def set_Min(self, val):
        try:
            self.set_Min = float(val)
        except:
            print("[set_Min] Error: failed to declare 'self.set_Min, reverting to default")

    # MAIN Functions

    def server_Func(self, opti_Vars):
        '''
        Description:

            A minimization function for use with the Minimize function.
            Options for the 'set_Min' variable according to different
            operations; allows for minimization, maximiation and
            convergence to a specific value.
        '''

        nl = "\n"

        if(isinstance(opti_Vars,(list,tuple))):
            print("[server_Func] Error: input 'opti_Vars' must be an array")
            return False

        if(isinstance(self.init_Com,(str,int,float))):
            out_Line = str(self.init_Com)
            if(self.new_Line):
                out_Line += nl
            else:
                out_Line += ' '
        else:
            out_Line = ''

        for i in opti_Vars:
            out_Line += str(i)
            if(self.new_Line):
                out_Line += nl
            else:
                out_Line += ' '

        if(isinstance(self.term_Com,(str,int,float))):
            out_Line += str(self.term_Com)
            if(self.new_Line):
                out_Line += nl
            else:
                out_Line += ' '

        self.Server.stdin.writelines([out_Line])
        eval_Line = float(self.Server.stdout.readline().rstrip())
        if(self.set_Min == 0.0):
            eval_Line = abs(eval_Line)
        elif(self.set_Min == 'inf'):
            eval_Line == 1.0/eval_Line
        elif('-inf' < self.set_Min < 'inf'):
            eval_Line = abs(eval_Line-self.set_Min)
        else:
            pass
        self.run_Count+=1

        if(self.eval_Print):
            if(self.run_Count%10==0):
                print(opti_Vars,eval_Line,self.run_Count)

        return eval_Line


    def Minimize(self, init_Vars, mini_Func, tolerence = 1e-6, method = 'Nelder-Mead', eval_Print = True):

        '''

        Description:

            Minimization function, inputs allow for initial condition
            as well as the function to be minimized.

        inputs:

            init_Vars : array of initial value(s), must be float(s)

            mini_Func : must be a python function, server_Func is useful for this role

        '''

        self.eval_Print = eval_Print

        start_Time = time.time()

        val = sciopt.minimize(
            fun = mini_Func,
            x0 = init_Vars,
            method = method,
            tol = tolerence
            )

        end_Time = time.time()

        interval = round(start_Time - end_Time)

        opti_Val = val.x
        if(eval_Print):
            print(val)
            print("# Runs = "+str(self.run_Count))
            print("procedure took "+str(interval)+" secs")

        self.run_Count = 0

        return opti_Val
