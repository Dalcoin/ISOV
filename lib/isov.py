import sys
import os
import subprocess
import re
import time

from progLib.programStructure import progStruct

from progLib.pmod import ioparse as iop
from progLib.pmod import strlist as strl
from progLib.pmod import mathops as mops
from progLib.pmod import pinax   as px


class isov(progStruct):

    def __init__(self,
                 eos_fold_name='eos',
                 run_bin_name='run',
                 osFormat='linux',
                 newPath=None,
                 rename=True,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    ',
                 endline='\n',
                 moduleNameOverride="ISOV",
                 **kwargs):

        super(isov, self).__init__('isov',
                                   'src',
                                   'bin',
                                   'dat',
                                   'par.don',
                                   'log.don',
                                   True,
                                   osFormat,
                                   newPath,
                                   rename,
                                   debug,
                                   shellPrint,
                                   colourPrint,
                                   space,
                                   endline,
                                   moduleNameOverride=moduleNameOverride,
                                   **kwargs)

        #########################
        # File and folder names #
        #########################

        # EoS
        self.EOSFOLD = eos_fold_name
        self.EOSPATH = ''

        # Files in BIN #

        # Bin Files
        self.RUNNAME = run_bin_name
        self.RUNPATH = ''

        # Input Files

        self.XPEFILE = 'execpar.don'
        self.XPEPATH = ''

        self.RDPFILE = 'readpar.don'
        self.RDPPATH = ''

        self.PHPFILE = 'phenpar.don'
        self.PHPPATH = ''


        # EOS-BIN FILE
        self.EXFILE = 'ex_nxlo.don'
        self.E0FILE = 'e0_nxlo.don'
        self.E1FILE = 'e1_nxlo.don'

        self.DENFILE = 'den.don'
        self.DENPATH = ''

        # Output Files

        self.EOSFILE = 'eosvals.don'
        self.EOSPATH = ''

        self.ISOFILE = 'isovals.don'
        self.ISOPATH = ''

        self.PRBFILE = 'prbvals.don'
        self.PRBPATH = ''

        self.PHNFILE = 'pheneos.don'
        self.PHNPATH = ''

        # DAT Files


        ###############
        # REGEX codes #
        ###############

        # General Regex codes
        self.DIGITS   = r"(\d+)"
        self.DIGITSPC = r"(\d+)\s+"

        self.FLOAT    = r'([+-]*\d+\.*\d*)'
        self.FLOATSPC = r'([+-]*\d+\.*\d*)\s+'

        self.RE_INT      = re.compile(r'([+-]*\d+)')
        self.RE_DIGITS   = re.compile(r"(\d+)")
        self.RE_DIGITSPC = re.compile(r"(\d+)\s+")

        self.RE_FLOAT        = re.compile(r'([+-]*\d+\.*\d*)')
        self.RE_FLOATSPC     = re.compile(r'([+-]*\d+\.*\d*)\s+')
        self.RE_SCIFLOAT     = re.compile(r'(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')
        self.RE_CHARFLOAT    = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+')
        self.RE_CHARSCIFLOAT = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')

        self.RE_BOOL = re.compile(r'(?:TRUE|True|true|FALSE|False|false)')
        self.RE_BOOL_FR = re.compile(r'(?:VRAI|Vrai|vrai|FAUX|Faux|faux)')

        self.EXECREG = re.compile(self.DIGITSPC+self.DIGITS)
        self.READREG = re.compile(5*self.DIGITSPC+self.DIGITS)
        self.PHENREG = re.compile(3*self.DIGITSPC+2*self.FLOATSPC+self.FLOAT)

        # Load regex codes
        self.LOADPAR = re.compile(r"\s*LOADPAR\s*:\s*(TRUE|True|true|FALSE|False|false)")

        # EoS errors 
        self.EOS_SPLIT_FILE_ERROR = False
        self.EOS_FILE_FORMAT_ERROR = False 
        self.EOS_SPLIT_PARSE_ERROR = False
        self.EOS_PASS_ERROR = False
        self.INITIAL_PARS_ERROR = False

        # BENV Parameters---------------|

        # initial data 
        self.initial_exepar = []
        self.current_exepar = []
        self.default_exepar = []

        self.initial_rrdpar = []
        self.current_rrdpar = []
        self.default_rrdpar = []

        self.initial_phnpar = []
        self.current_phnpar = []
        self.default_phnpar = []

        # output data

        self.eos_collect_lines = []
        self.iso_collect_lines = []
        self.prb_collect_lines = []
        self.phn_collect_lines = []
        self.sng_collect_lines = []

        # Set Binary and par Files
        self.isov_bin_list = [self.RUNNAME, self.XPEFILE, self.RDPFILE, self.PHPFILE, self.DENFILE]
        self.ISOV_SET_BINARIES = self.init_binary(self.isov_bin_list)
        self.ISOV_SET_PATHWAYS = self.isov_structure(**kwargs)

        self.ISOV_SET_PARS = self.get_parameters(**kwargs)

        self.EOS_OBJ = None
        eoslist = self.collect_eos(**kwargs)
        if(eoslist == False):
            self.ISOV_SET_EOS = False
        else:
            self.EOS_OBJ = eoslist
            self.ISOV_SET_EOS = True

        self.DEN_OBJ = None
        denlist = self.collect_den(**kwargs)
        if(denlist == False):
            self.ISOV_SET_DEN = False
        else:
            self.DEN_OBJ = denlist
            self.ISOV_SET_DEN = True

    ##########################
    # Initiate BENV STRUCTRE #
    ##########################

    def isov_structure(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("isov_structure", **kwargs)

        success = True

        eosset = self.init_fold_in_main(self.EOSFOLD, **kwargs)
        if(eosset == False):
            return False
        self.EOSPATH = self.FOLDPATH_DICT[self.EOSFOLD]

        if(self.RUNNAME in self.BIN_DICT):
            self.RUNPATH = self.BIN_DICT[self.RUNNAME]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.RUNNAME, **kwargs)

        if(self.XPEFILE in self.BIN_DICT):
            self.XPEPATH = self.BIN_DICT[self.XPEFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.XPEFILE, **kwargs)

        if(self.RDPFILE in self.BIN_DICT):
            self.RDPPATH = self.BIN_DICT[self.RDPFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.RDPFILE, **kwargs)

        if(self.PHPFILE in self.BIN_DICT):
            self.PHPPATH = self.BIN_DICT[self.PHPFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.PHPFILE, **kwargs)

        if(self.DENFILE in self.BIN_DICT):
            self.DENPATH = self.BIN_DICT[self.DENFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.DENFILE, **kwargs)

        return success


    ##############
    # Parameters #
    ##############

    def create_exeparln(self, nrun=1, nprint=1, **kwargs):

        kwargs = self.__update_funcNameHeader__("create_exeparln", **kwargs)

        if(not isinstance(nrun, int)):
            try:
                nrun = int(float(nrun))
            except:
                return self.__err_print__("should be castable to an integer", varID='nrun' **kwargs)

        if(not isinstance(nprint, int)):
            try:
                nprint = int(float(nprint))
            except:
                return self.__err_print__("should be castable to an integer", varID='nprint' **kwargs)

        if(nrun not in [1,2,3]):
            return self.__err_print__("should be equal to either 1, 2, or 3", varID='nrun' **kwargs)

        if(nrun == 1 and nprint not in [1,2,3]):
            return self.__err_print__("is equal to 1, 'nprint' should be equal to either 1, 2, or 3", varID='nrun' **kwargs)

        if(nrun == 2 and (nprint < 2 or nprint > 21)):
            return self.__err_print__("is equal to 2, 'nprint' a value in the range [3,21]", varID='nrun' **kwargs)

        line = str(nrun)+"  "+str(nprint)
        return line

    def create_rrdparln(self, n0, n1, n=0, n_read=0, nkf_read=1, ndn_read=0, **kwargs):

        kwargs = self.__update_funcNameHeader__("create_rrdparln", **kwargs)

        vars = [n0, n1, n, n_read, nkf_read, ndn_read]
        varnames = ['n0', 'n1', 'n', 'n_read', 'nkf_read', 'ndn_read']

        for i in range(len(vars)):
            if(not isinstance(vars[i], int)):
                try:
                    vars[i] = int(float(vars[i]))
                except:
                    return self.__err_print__("should be castable to an integer", varID=varnames[i], **kwargs)

        if(vars[3] not in [0,1]):
            return self.__err_print__("should be equal to either 0 or 1", varID='n_read' **kwargs)

        if(vars[4] not in [0,1]):
            return self.__err_print__("should be equal to either 0 or 1", varID='nkf_read' **kwargs)

        if(vars[5] not in [0,1]):
            return self.__err_print__("should be equal to either 0 or 1", varID='ndn_read' **kwargs)

        line = strl.array_to_str([vars[3], vars[4], vars[5], vars[2], vars[1], vars[0]], spc='  ', **kwargs)
        return line


    def create_phpparln(self, mic, isnm=0, isym_emp=0, gam=2.7, xk0=220.0, rhosat=0.16, **kwargs):

        kwargs = self.__update_funcNameHeader__("create_rrdparln", **kwargs)

        intvars = [mic, isnm, isym_emp]
        intvarnames = ['mic', 'isnm', 'isym_emp']

        floatvars = [gam, xk0, rhosat]
        floatvarnames = ['gam', 'xk0', 'rhosat']

        for i in range(len(intvars)):
            if(not isinstance(intvars[i], int)):
                try:
                    intvars[i] = int(float(intvars[i]))
                except:
                    return self.__err_print__("should be castable to an integer", varID=intvarnames[i] **kwargs)

        for i in range(len(floatvars)):
            if(not isinstance(floatvars[i], float)):
                try:
                    floatvars[i] = float(floatvars[i])
                except:
                    return self.__err_print__("should be castable to an integer", varID=floatvarnames[i] **kwargs)

        if(intvars[0] not in [0,1]):
            return self.__err_print__("should be equal to either 0 or 1", varID='mic' **kwargs)

        if(intvars[1] not in [0,1]):
            return self.__err_print__("should be equal to either 0 or 1", varID='isnm' **kwargs)

        if(intvars[2] not in [0,1]):
            return self.__err_print__("should be equal to either 0 or 1", varID='isym_emp' **kwargs)

        if(floatvars[0] < 0):
            return self.__err_print__("should be greater than 0", varID='gam' **kwargs)

        if(floatvars[1] < 0):
            return self.__err_print__("should be greater than 0", varID='xk0' **kwargs)

        if(floatvars[2] < 0):
            return self.__err_print__("should be greater than 0", varID='rhosat' **kwargs)

        line = strl.array_to_str([intvars[0], intvars[1], intvars[2], floatvars[0], floatvars[1], floatvars[2]], spc='  ', **kwargs)
        return line


    def write_parline(self, parline, type, **kwargs):
        '''
        Passes benv parameters to 'par.don' file located in 'bin'


        '''
        kwargs = self.__update_funcNameHeader__("write_parline", **kwargs)

        if(not isinstance(type, str)):
            return self.__err_print__("should be a string", varID='type', **kwargs)
        else:
            if(type.lower() not in ['exec', 'read', 'phen']):
                return self.__err_print__("should be one of the following: 'exec', 'read', 'phen'", varID='type', **kwargs)

        if(not isinstance(parline, str)):
            return self.__err_print__("should be a string", varID='parline', **kwargs)

        path = ''
        if(type == 'exec'):
            path = self.XPEPATH
        elif(type == 'read'):
            path = self.RDPPATH
        elif(type == 'phen'):
            path = self.PHPPATH
        else:
            return self.__err_print__("should be one of the following: 'exec', 'read', 'phen'", varID='type', **kwargs)

        success = iop.flat_file_write(path, [parline], **kwargs)
        return success


    def parse_readfiles(self, execvals, **kwargs):

        kwargs = self.__update_funcNameHeader__("write_parlnlist", **kwargs)

        nrun, nprint = execvals

        readfiles = []
        if(str(nrun) == '1'):
            if(str(nprint) == '1'):
                readfiles = ["eosvals.don"]
            elif(str(nprint) == '2'):
                readfiles = ["isovals.don"]
            elif(str(nprint) == '3'):
                readfiles = ["eosvals.don", "isovals.don"]
            else:
                pass
        elif(str(nrun) == '2'):
            readfiles = ['prbvals.don']
        elif(str(nrun) == '3'):
            readfiles = ['pheneos.don']
        else:
            pass

        return readfiles


    def parse_parameters(self, par_lines, **kwargs):

        kwargs = self.__update_funcNameHeader__("parse_parameters", **kwargs)

        try:
            execline = par_lines[0].rstrip()
            readline = par_lines[1].rstrip()
            phenline = par_lines[2].rstrip()
        except:
            return self.__err_print__("should be an array containing 3 strings", varID='par_lines', **kwargs)

        try:
            execlist = self.EXECREG.findall(execline)[0]
        except:
            return self.__err_print__("could not parse 'EXEC' line from 'par.don'", **kwargs)

        try:
            readlist = self.READREG.findall(readline)[0]
        except:
            return self.__err_print__("could not parse 'READ' line from 'par.don'", **kwargs)

        try:
            phenlist = self.PHENREG.findall(phenline)[0]
        except:
            return self.__err_print__("could not parse 'PHEN' line from 'par.don'", **kwargs)

        return (execlist, readlist, phenlist)

    def get_parameters(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("get_parameters", **kwargs)

        # Get parameters from 'par.don' file
        par_lines = self.get_options(**kwargs)
        if(par_lines == False):
            return self.__err_print__("could not collect lines from 'par.don' file", **kwargs)

        # Format parameters lines into three data lines
        pars = self.parse_parameters(par_lines, **kwargs)
        if(pars == False):
            return self.__err_print__("failure to format parameter data", **kwargs)

        self.initial_exepar = pars[0]
        self.initial_rrdpar = pars[1]
        self.initial_phnpar = pars[2]

        self.current_exepar = pars[0]
        self.current_rrdpar = pars[1]
        self.current_phnpar = pars[2]

        return True



    ################
    # Output Data  #
    ################

    def format_isov_data(self, isovdata, return_data=False, add_newline=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("format_isov_data", **kwargs)

        if(add_newline):
            nl = '\n'
        else:
            nl = ''

        phen_collect = [["n0",
                         "rho0",
                         "rho1",
                         "rho2",
                         "e0o",
                         "e01",
                         "e02",
                         "e1o",
                         "e11",
                         "e12",
                         "esym0",
                         "esym1",
                         "esym2",
                         "prs0o",
                         "prs01",
                         "prs02",
                         "prs1o",
                         "prs11",
                         "prs12",
                         "bigL",
                         "bigK",
                         "bigKR",
                         "bigK0"]]

        eos_names = sorted(list(isovdata))

        for i,eos in enumerate(eos_names):
            isofiles, phenline = isovdata[eos]
            file_names = sorted(list(isofiles))
            for file in file_names:
                lines = isofiles[file]
                if(file == 'eosvals.don'):
                    self.eos_collect_lines += ["EoS : "+str(eos)+", [phenline] : "+str(phenline)+"\n","\n"]
                    self.eos_collect_lines += lines
                    self.eos_collect_lines += ["\n", "\n"]
                if(file == 'isovals.don'):
                    self.phen_collect_lines += ["EoS : "+str(eos)+", [phenline] : "+str(phenline)+"\n","\n"]
                    phen_collect.append(strl.array_to_str(map(lambda x: x.rstrip(), eos[file]), **kwargs))
                if(file == 'prbvals.don'):
                    self.prb_collect_lines += ("EoS : "+str(eos)+", [phenline] : "+str(phenline)+"\n","\n")
                    self.prb_collect_lines += lines
                    self.prb_collect_lines += ["\n", "\n"]
                if(file == 'pheneos.don'):
                    self.phn_collect_lines += ("EoS : "+str(eos)+", [phenline] : "+str(phenline)+"\n","\n")
                    self.phn_collect_lines += lines
                    self.phn_collect_lines += ["\n", "\n"]

        if(file == 'isovals.don'):
            self.phen_collect_lines += px.matrix_to_str_array(px.table_str_to_numeric(phen_collect, **kwargs), **kwargs)
            self.phen_collect_lines += ["\n", "\n"]

        if(return_data):
            output = True
        else:
            output = True
        return output


    def write_to_dat(self, file, data, **kwargs):

        kwargs = self.__update_funcNameHeader__("write_to_dat", **kwargs)

        datfilepath = self.joinNode(self.DATPATH, file, **kwargs)
        if(datfilepath == False):
            return False

        return iop.flat_file_write(datfilepath, data, **kwargs)


    def write_all_dat_output(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("write_all_dat_output", **kwargs)

        if(len(self.eos_collect_lines) > 0):
            success = self.write_to_dat(self.EOSFILE, self.eos_collect_lines, **kwargs)
            if(success == False):
                self.__err_print__("Failure when writing 'eos_collect_lines'", **kwargs)

        if(len(self.iso_collect_lines) > 0):
            success = self.write_to_dat(self.ISOFILE, self.iso_collect_lines, **kwargs)
            if(success == False):
                self.__err_print__("Failure when writing 'iso_collect_lines'", **kwargs)

        if(len(self.prb_collect_lines) > 0):
            success = self.write_to_dat(self.PRBFILE, self.prb_collect_lines, **kwargs)
            if(success == False):
                self.__err_print__("Failure when writing 'prb_collect_lines'", **kwargs)

        if(len(self.phn_collect_lines) > 0):
            success = self.write_to_dat(self.PHNFILE, self.phn_collect_lines, **kwargs)
            if(success == False):
                self.__err_print__("Failure when writing 'phn_collect_lines'", **kwargs)

        return True

    #######
    # EOS #
    #######

    def collect_den(self, **kwargs):
        kwargs = self.__update_funcNameHeader__("collect_den", **kwargs)
        eos_file_list = self.contentPath(self.EOSPATH, **kwargs)
        if(eos_file_list == None or eos_file_list == False):
            self.EOS_COLLECT_ERROR = True
            return self.__err_print__("folder contents could not be retrieved", varID='eos', **kwargs)

        if('den.txt' in eos_file_list):
            file_path = self.joinNode(self.EOSPATH, 'den.txt', **kwargs)
            den = iop.flat_file_intable(file_path, **kwargs)[0]
            return den
        else:
            return []

    def collect_eos(self, **kwargs):
        '''
        Notes:

            Collects EoS from 'eos' directory 
            This function should only be called once per BENV run
        '''

        kwargs = self.__update_funcNameHeader__("collect_eos", **kwargs)

        eos_file_list = self.contentPath(self.EOSPATH, **kwargs)

        if(eos_file_list == None or eos_file_list == False):
            self.EOS_COLLECT_ERROR = True
            return self.__err_print__("folder contents could not be retrieved", varID='eos', **kwargs)

        exfiles = []
        e1files = []
        e0files = []
        eafail = []
        eoslist = []

        for i in eos_file_list:
            if('ex' in i.lower() and (('e0' not in i.lower()) and ('e1' not in i.lower()))):
                exfiles.append(i)
            elif('e1' in i.lower() and (('e0' not in i.lower()) and ('ex' not in i.lower()))):
                e1files.append(i) 
            elif('e0' in i.lower() and (('ex' not in i.lower()) and ('e1' not in i.lower()))):
                e0files.append(i)
            else:
                eafail.append(i)

        if(len(eafail) > 0):
            msg = ["The following files are not valid 'eos' files:"]+eafail
            self.__err_print__(msg, **kwargs)

        improper_format = []
        for file in exfiles:
            file_path = self.joinNode(self.EOSPATH, file, **kwargs)
            ex = iop.flat_file_intable(file_path, **kwargs)
            if(ex != False):
                if(len(ex) != 3):
                    improper_format.append(ex)
                    continue
                eoslist.append((ex, (file,)))
            else:
                continue
        if(len(improper_format)>0):
            self.__err_print__(["The following 'ex' files were improperly formatted:"]+improper_format, **kwargs)

        for file in e0files:

            e1pack = False
            e1name = ''

            comp_name = self.name_compliment(file, {'e0':'e1', 'E0':'E1'}, **kwargs)
            if(comp_name == False):
                self.__err_print__("could not be converted to a name compliment", varID=file, **kwargs)
            else:
                if(len(comp_name) > 0):
                    if(len(comp_name) > 2):
                        self.__err_print__("has more than one file compliment", varID=file, heading='Warning', **kwargs)
                    e1name = comp_name[0][0]
                    idbaseline = comp_name[0][1]
                else:
                    self.__err_print__("could not be converted to a name compliment", varID=file, **kwargs)

            e1data = False

            e0_file_path = self.joinNode(self.EOSPATH, file, **kwargs)
            e0data = iop.flat_file_intable(e0_file_path, **kwargs)
            if(e1name in e1files):
                e1pack = True
                e1_file_path = self.joinNode(self.EOSPATH, e1name, **kwargs)
                e1data = iop.flat_file_intable(e1_file_path, **kwargs)

            if(e0data == False):
                self.__err_print__("could not parse the file at path '"+str(e0_file_path)+"' into a table", **kwargs)
                continue
            if(e1data == False and e1pack):
                self.__err_print__("could not parse the file at path '"+str(e1_file_path)+"' into a table", **kwargs)
                continue

            if(e1pack):
                e10 = []
                try:
                    e10 = [e0data[0], e0data[1], e1data[0], e1data[1]]
                    eoslist.append((e10,idbaseline))
                except:
                    msg = ["failure to coerce data into four arrays, check pathways:", 
                           "e0 path : "+str(e0_file_path),
                           "e1 path : "+str(e1_file_path)]
                    self.__err_print__(msg, **kwargs)
                    continue
            else:
                self.__err_print__("file does not have an 'E1' compliment", varID='E0', **kwargs)
                continue

        return eoslist


    def parse_eosid(self, eosid, tag, **kwargs):
        if(self.__not_arr_print__(eosid, varID='eosid', **kwargs)):
            return False
        if(self.__not_str_print__(tag, varID='tag', **kwargs)):
            return False
        try:
            n = len(eosid)
            if(n == 1):
                if(tag != 'ex'):
                    return (tag+eosid[0])
                else:
                    return eosid[0]
            elif(n == 2):
                return (eosid[0]+tag+eosid[1])
            else:
                return self.__err_print__("couldn't be parsed - length : "+str(n), varID='eosid', **kwargs)
        except:
            return self.__err_print__("couldn't be parsed", varID='eosid', **kwargs)


    def format_eos_data(self, eos_obj, readvals, den_obj=[], **kwargs):

        kwargs = self.__update_funcNameHeader__("format_eos_data", **kwargs)

        if(self.__not_arr_print__(readvals, varID='readvals', **kwargs)):
            return False
        else:
            if(len(readvals) < 2):
                return self.__err_print__("should be an array of length 2", varID='readvals' **kwargs)

        try:
            eoslist, eosid = eos_obj
        except:
            return self.__err_print__("should be an array of length two", varID='eos_obj',  **kwargs)

        if(self.__not_arr_print__(eoslist, varID='First Entry of eos_obj', **kwargs)):
            return False

        if(isinstance(den_obj, (list,tuple))):
            if(len(den_obj)>0):
                n = len(den_obj)
            else:
                n = 0
        else:
            n = 0

        output = ()
        exgp = []
        e0gp = []
        e1gp = []

        m = len(eoslist)

        if(m == 3):
            n_read = 0
            kf = eoslist[0]
            e0 = eoslist[1]
            e1 = eoslist[2]
            if(len(kf) == len(e0) and len(e0) == len(e1)):
                n0 = len(kf)
                n1 = len(kf)
            else:
                return self.__err_print__("eos arrays should all be the same length", varID='eos_obj', **kwargs)
            exgp = map(lambda x,y,z: strl.array_to_str([x,y,z], spc='  ', endline=True), kf,e0,e1)
            eval = [exgp]
            neid = self.parse_eosid(eosid, 'ex', **kwargs)

        elif(m == 4):
            n_read = 1
            kf0 = eoslist[0]
            e0  = eoslist[1]
            kf1 = eoslist[2]
            e1  = eoslist[3]

            if(len(kf0) == len(e0)):
                n0 = len(kf0)
            else:
                return self.__err_print__("e0 and the corrosponding kfs should be arrays with the same length", **kwargs)

            if(len(kf1) == len(e1)):
                n1 = len(kf1)
            else:
                return self.__err_print__("e1 and the corrosponding kfs should be arrays with the same length", **kwargs)

            e0gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf0,e0)
            e1gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf1,e1)
            eval = [e0gp, e1gp]
            neid = self.parse_eosid(eosid, 'e10', **kwargs)

        else:
            return self.__err_print__("must a numeric array of length 2 or 3 : "+str(len(eoslist)), varID='eoslist', **kwargs)

        readline = self.create_rrdparln(n0, n1, n, n_read, readvals[1], readvals[2])
        if(readline == False):
            return self.__err_print__("failure to create readline", **kwargs)

        output = (n_read, eval, readline, neid)

        return output


    def write_eos(self, elist, type, **kwargs):

        kwargs = self.__update_funcNameHeader__("write_eos", **kwargs)

        ealist = []
        e0list = []
        e1list = []

        try:
            if(type == 0):
                ealist = elist[0]
            elif(type == 1):
                e0list = elist[0]
                e1list = elist[1]
            else:
                return self.__err_print__("should be either 0, 1 or 2", varID='type', **kwargs)
        except:
            msg = "has a component which is not properly formatted"
            return self.__err_print__(msg, varID='elist', **kwargs)

        if(type == 0):
            eos_path = self.joinNode(self.BINPATH, self.EXFILE, **kwargs)
            if(eos_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.EXFILE, **kwargs)
            success = iop.flat_file_write(eos_path, ealist, **kwargs)
            if(success == False):
                return False
        elif(type == 1):
            e0_path = self.joinNode(self.BINPATH, self.E0FILE, **kwargs)
            if(e0_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.E0FILE, **kwargs)
            success = iop.flat_file_write(e0_path, e0list, **kwargs)
            if(success == False):
                return False
            e1_path = self.joinNode(self.BINPATH, self.E1FILE, **kwargs)
            if(e1_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.E1FILE, **kwargs)
            success = iop.flat_file_write(e1_path, e1list, **kwargs)
            if(success == False):
                return False
        else:
            return self.__err_print__("not properly formatted", varID='formatted_eos', **kwargs)

        return True


    #######################################
    # functions dealing with benv looping #------------------------------------------------------------|
    #######################################

    # Running and Looping functions

    def parline_generator(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("parline_generator", **kwargs)

        density = self.num_from_console("Input the density option [2, 3, 4]: ",
                                        value_type='int',
                                        free_and_accepted_values=[2,3,4],
                                        **kwargs)
        if(density not in [2, 3, 4]):
            return True

        micro = self.bool_from_console("Should the EoS be pure microscopic? [True, False]: ", **kwargs)
        if(micro not in [True, False]):
            return True

        if(micro):
            isym = False
            isyme = False
            k0 = 220
            rho0 = 0.16
        else:
            isym = self.num_from_console("Input the symmetric EoS choice option [0, 1]: ",
                                          value_type='int',
                                          free_and_accepted_values=[0,1],
                                          **kwargs)
            if(isym not in [0,1]):
                return True
            else:
                if(isym == 1): 
                    isym = True
                else:
                    isym = False

            isyme = self.bool_from_console("Should symmetry energy be purely emperical? [True, False]: ", **kwargs)
            if(isyme not in [True, False]):
                return True
            else:
                if(isyme == 1): 
                    isyme = True
                else:
                    isyme = False

            k0 = self.num_from_console("Input the curvature value (integer): ",
                                       value_type='int',
                                       **kwargs)

            rho0 = self.num_from_console("Input the saturation density value (float): ",
                                         value_type='float',
                                         **kwargs)

        fff = self.num_from_console("Input the density functional surface constant (integer): ",
                                    value_type='int',
                                    **kwargs)

        new_parline = self.create_parline(0, 9, 9, 9,
                                          density = density,
                                          mic = micro,
                                          e0_rho0 = isym,
                                          phenom_esym = isyme,
                                          k0 = k0,
                                          rho0 = rho0,
                                          fff = fff,
                                          addn=False,
                                          **kwargs)

        print(" ")

        if(not isinstance(new_parline, str)):
            return False
        else:
            self.initial_parline = new_parline
            self.initial_parlist = self.parse_parline(self.initial_parline)

        print(self.space+"new parline = '"+new_parline+"' \n")

        return new_parline


    def single_run(self, result_files,
                         exeline=None,
                         rrdline=None,
                         phnline=None,
                         run_cmd='run.sh',
                         **kwargs):

        kwargs = self.__update_funcNameHeader__("single_run", **kwargs)

        if(isinstance(exeline, str)):
            pass_line = self.write_parline(exeline, type='exec', **kwargs)
            if(pass_line == False):
                msg = ["failure to create and write exec line", "'exeline' : "+str(exeline)]
                return self.__err_print__(msg, **kwargs)
        if(isinstance(rrdline, str)):
            pass_line = self.write_parline(rrdline, type='exec', **kwargs)
            if(pass_line == False):
                msg = ["failure to create and write exec line", "'rrdline' : "+str(rrdline)]
                return self.__err_print__(msg, **kwargs)
        if(isinstance(phnline, str)):
            pass_line = self.write_parline(phnline, type='exec', **kwargs)
            if(pass_line == False):
                msg = ["failure to create and write exec line", "'phnline' : "+str(phnline)]
                return self.__err_print__(msg, **kwargs)

        self.set_osdir(self.BINPATH, **kwargs)
        self.run_commands(run_cmd, **kwargs)
        self.set_osdir(**kwargs)

        values_dict = self.read_files_from_folder('bin', result_files, clean=True, **kwargs)

        self.cycle+=1
        return (values_dict, phnline)


    def eos_loop(self, eoslist, execvals, readvals, phenvals, denlist=[], reset=True, **kwargs):
        '''
        reset : [bool] (True), resets data files to pre-run values
        '''

        kwargs = self.__update_funcNameHeader__("eos_loop", **kwargs)

        isovals = {}

        if(self.__not_arr_print__(eoslist, varID='eoslist', **kwargs)):
            return False
        if(self.__not_arr_print__(execvals, varID='execvals', **kwargs)):
            return False
        if(self.__not_arr_print__(readvals, varID='readvals', **kwargs)):
            return False
        if(self.__not_arr_print__(phenvals, varID='phenvals', **kwargs)):
            return False

        readfiles = self.parse_readfiles(execvals, **kwargs)
        if(readfiles == False):
            return self.__err_print__("failure to parse which list of files to read from bin", **kwargs)

        execline = self.create_exeparln(execvals[0], execvals[1], **kwargs)
        if(execline == False):
            return self.__err_print__("failure to create 'exec' values", **kwargs)

        phenline = self.create_phpparln(phenvals[0],
                                        phenvals[1],
                                        phenvals[2],
                                        phenvals[3],
                                        phenvals[4],
                                        phenvals[5],
                                        **kwargs)
        if(phenline == False):
            return self.__err_print__("failure to create 'phen' values", **kwargs)

        if(len(denlist)>0):
            den_path = self.joinNode(self.BINPATH, self.DENFILE, **kwargs)
            if(den_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.DENFILE, **kwargs)
            success = iop.flat_file_write(den_path, denlist, **kwargs)
            if(success == False):
                return self.__err_print__("failure to pass 'den' list to 'den.don' in the bin folder", **kwargs)

        # cycle through each EoS
        for i,eos in enumerate(eoslist):

            # Convert each EoS object into eos data (eos_inst) and eos id (eosid)
            formatted_eos = self.format_eos_data(eos, readvals, denlist, **kwargs)
            if(formatted_eos == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS could not be formatted, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue
            # Set eos data (eos_instance) and 'par.don' line (parline)
            type, eos_instance, readline, eosid = formatted_eos

            # Pass the eos data to the appropriate file
            success = self.write_eos(eos_instance, type, **kwargs)
            if(success == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS could not be passed to 'bin', cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

            isovals[eosid] = self.single_run(readfiles, execline, readline, phenline, **kwargs)
            if(isovals[eosid] == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" failed the single-run routine, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

        if(reset):
            pass

        return isovals


    def isov_run(self, reset=True, return_data=False, **kwargs):
        '''
        !Function which runs the EoS loop!
        '''

        kwargs = self.__update_funcNameHeader__("isov_run", **kwargs)

        # Read from initial parameters
        if(self.ISOV_SET_PARS):
            exepar = self.current_exepar
            rrdpar = self.current_rrdpar
            phnpar = self.current_phnpar
        else:
            self.__err_print__("parameters not set, run terminated", **kwargs)

        # Get stored EoS object
        if(self.ISOV_SET_EOS):
            eoslist = self.EOS_OBJ
        else:
            return self.__err_print__("no stored EoS object found", **kwargs)

        # Get stored DEN object
        if(self.ISOV_SET_DEN):
            denlist = self.DEN_OBJ
        else:
            denlist = []

        # Put EoS in EoS loop
        eosdata = self.eos_loop(eoslist, exepar, rrdpar, phnpar, denlist, reset, **kwargs)
        if(eosdata == False):
            return self.__err_print__("failure while looping through the EoSs", **kwargs)

        success = self.format_isov_data(eosdata, return_data, **kwargs)
        if(success == False):
            return self.__err_print__("failure when formatting ISOV data", **kwargs)

        return success


    def set_isov_menu(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("set_isov_menu", **kwargs)

        menu_lines = ["Input 'pars' to set initialize input parameters",
                      "Input 'run' isov program",
                      "Input 'menu' to view the menu again",
                      "Input 'cleardat' to clear the 'dat' folder",
                      "Input 'exit' to quit the program"]

        return self.set_option_menu(menu_lines, **kwargs)



    def isov_program_loop(self, input, **kwargs):

        kwargs = self.__update_funcNameHeader__("isov_program_loop", **kwargs)

        action_list = ('pars', 'run', 'eos', 'menu', 'cleardat', 'help', 'exit', 'quit')

        if(input not in action_list):
            print(self.space+"Input not recognized : '"+str(input))+"'"
            print(self.space+"Please select an option from the menu\n")
            return True
        else:
            if(input == 'exit' or input == 'quit'):
                self.write_all_dat_output(**kwargs)
                return True

        if(input == 'pars'):
            self.parline_generator(**kwargs)
        elif(input == 'run'):
            run_attempt = self.isov_run(**kwargs)
            if(run_attempt == False):
                print(self.space+"An error occured during 'benv' execution, see above for details\n")
            else:
                print(self.space+"ISOV 'eos' loop completed...\n")
        elif(input == 'cleardat'):
            self.clear_data_folder(**kwargs)
        else:
            return True
        return True