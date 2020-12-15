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
                                   'isopar.don',
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
        self.RE_INT      = re.compile(r'([+-]*\d+)')
        self.RE_DIGITS   = re.compile(r"(\d+)")
        self.RE_DIGITSPC = re.compile(r"(\d+)\s+")

        self.RE_FLOAT        = re.compile(r'([+-]*\d+\.*\d*)')
        self.RE_SCIFLOAT     = re.compile(r'(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')
        self.RE_CHARFLOAT    = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+')
        self.RE_CHARSCIFLOAT = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')

        self.RE_BOOL = re.compile(r'(?:TRUE|True|true|FALSE|False|false)')
        self.RE_BOOL_FR = re.compile(r'(?:VRAI|Vrai|vrai|FAUX|Faux|faux)')

        # SKVAL regex codes
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

        # Set Binary and par Files
        self.isov_bin_list = [self.RUNNAME, self.XPEFILE, self.RDPFILE, self.PHPFILE, self.DENFILE]
        self.ISOV_SET_BINARIES = self.init_binary(self.isov_bin_list)
        self.ISOV_SET_PATHWAYS = self.isov_structure(**kwargs)


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

        if(self.RUNFILE in self.BIN_DICT):
            self.RUNPATH = self.BIN_DICT[self.RUNFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.RUNFILE, **kwargs)

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
        elif(type = 'read'):
            path = self.RDPPATH
        elif(type = 'phen'):
            path = self.PHPPATH
        else:
            return self.__err_print__("should be one of the following: 'exec', 'read', 'phen'", varID='type', **kwargs)

        success = iop.flat_file_write(path, [parline], **kwargs)
        return success


    def write_parlnlist(self, parlnlist, **kwargs):

        kwargs = self.__update_funcNameHeader__("write_parlnlist", **kwargs)

        if(self.__not_arr_print__(parlnlist, varID='parlnlist', **kwargs)):
            return False

        if(len(parlnlist) != 3):
            return self.__err_print__("should be a length of 3", varID='parlnlist', **kwargs)

        execvals, readvals, phenvals = parlnlist

        nrun, nprint = execvals
        execln = self.create_exeparln(nrun, nprint, **kwargs)
        if(execln == False):
            return self.__err_print__("failure to create a 'exec' parameter string", **kwargs)
        success = self.write_parline(execln, 'exec', **kwargs)
        if(success == False):
            return self.__err_print__("failure to pass 'exec' parameter string", **kwargs)

        n0, n1, n, n_read, nkf_read, ndn_read = readvals
        readln = self.create_rrdparln(n0, n1, n, n_read, nkf_read, ndn_read, **kwargs)
        if(readln == False):
            return self.__err_print__("failure to create a 'read' parameter string", **kwargs)
        success = self.write_parline(readln, 'read', **kwargs)
        if(success == False):
            return self.__err_print__("failure to pass 'read' parameter string", **kwargs)

        mic, isnm, isym_emp, gam, xk0, rhosat = phenvals
        phenln = self.create_phpparln(mic, isnm, isym_emp, gam, xk0, rhosat, **kwargs)
        if(phenln == False):
            return self.__err_print__("failure to create a 'phen' parameter string", **kwargs)
        success = self.write_parline(phenln, 'phen', **kwargs)
        if(success == False):
            return self.__err_print__("failure to pass 'phen' parameter string", **kwargs)

        if(str(nrun) == '1'):
            if(str(nprint) == '0'):
                readfiles = []
            elif(str(nprint == '1'):
                readfiles = []


    ################
    # Output Data  #
    ################

    def format_isov_data(self, benvdata,
                               eospars=True,
                               eosgrup=True,
                               add_newline=True,
                               add_descript=True,
                               add_key=True,
                               **kwargs):

        if(add_newline):
            nl = '\n'
        else:
            nl = ''

        kwargs = self.__update_funcNameHeader__("format_isov_data", **kwargs)

        par_Strings = []
        val_Strings = []
        den_Strings = []

        rhops = []
        rhons = []
        rhots = []
        rholab= []
        rhoidx= []

        ingroup_pars = {}
        ingroup_vals = {}

        if(add_descript):
            if(eosgrup):
                val_Strings.append("    NR        PR        NS        CHR       BE        SEC       RD      A   Z    (EOS)"+nl)
            else:
                val_Strings.append("    NR        PR        NS        CHR       BE        SEC       RD      EOS    (A  Z)"+nl)
            val_Strings.append(nl)

        eos_names = sorted(list(benvdata))

        for i,eos in enumerate(eos_names):
            if(eosgrup):
                if(eospars):
                    par_Strings.append(str(eos)+nl)
                    val_Strings.append(str(eos)+nl)
                else:
                    val_Strings.append(str(eos)+nl)

            skval = benvdata[eos]
            az_names = sorted(list(skval))
            for az in az_names:
                pars, vals, dentable = skval[az]
                if(eosgrup):
                    nucleus = "  "+strl.array_to_str(az ,spc = '  ')+nl
                    if(eospars):
                        par_Strings.append(pars+nucleus)
                        val_Strings.append(vals+nucleus)
                    else:
                        val_Strings.append(vals+nucleus)
                else:
                    if(eospars):
                        if(ingroup_pars.get(az) == None):
                            ingroup_pars[az] = []
                        if(ingroup_vals.get(az) == None):
                            ingroup_vals[az] = []
                        ingroup_pars[az].append(pars+"  "+eos+nl)
                        ingroup_vals[az].append(vals+"  "+eos+nl)
                    else:
                        if(ingroup_vals.get(az) == None):
                            ingroup_vals[az] = []
                        ingroup_vals[az].append(vals+"  "+eos+nl)
                if(self.skval_dict['Density']):
                    if(isinstance(dentable,(tuple,list))):
                        if(len(dentable) > 0):
                            if(len(rhops) == 0):
                                rhops = [dentable[0]]+[dentable[1]]
                                rhons = [dentable[0]]+[dentable[2]]
                                rhots = [dentable[0]]+[dentable[3]]
                                rholab= ["dens    ", "r0_"+str(az[0])+"_"+str(az[1])]
                                rhoidx= ["dens: Density (fm^{-3})\n", "r0"+"_"+str(az[0])+"_"+str(az[1])+": "+str(eos)+"\n"]
                            else:
                                rhops.append(dentable[1])
                                rhons.append(dentable[2])
                                rhots.append(dentable[3])
                                rholab.append("r"+str(i)+"_"+str(az[0])+"_"+str(az[1]))
                                rhoidx.append("r"+str(i)+"_"+str(az[0])+"_"+str(az[1])+": "+str(eos)+"\n")
                    else:
                        self.__err_print__("does not point to an array : "+str(type(dentable)), varID='dentable', **kwargs)
        if(eosgrup):
            if(eospars):
                par_Strings.append(nl)
                val_Strings.append(nl)
            else:
                val_Strings.append(nl)
        else:
            if(len(ingroup_vals)>0):
                az_names = sorted(list(ingroup_vals))
                if(eospars):
                    for az in az_names:
                        nucleus = ["  "+strl.array_to_str(az ,spc = '  ')+nl]
                        par_Strings += nucleus+ingroup_pars[az]
                        val_Strings += nucleus+ingroup_vals[az]
                else:
                    for az in az_names:
                        nucleus = ["  "+strl.array_to_str(az ,spc = '  ')+nl]
                        val_Strings += nucleus+ingroup_vals[az]

        if(add_key):
            val_Strings.append(nl)
            val_Strings.append(nl)
            val_Strings.append("*Key"+nl)
            val_Strings.append(nl)
            val_Strings.append("NR  :  Neutron Radius"+nl)
            val_Strings.append("PR  :  Proton  Radius"+nl)
            val_Strings.append("NS  :  Neutron Skin"+nl)
            val_Strings.append("CHR :  Charge  Radius"+nl)
            val_Strings.append("BE  :  Binding Energy"+nl)
            val_Strings.append("SEC :  Sym. Eng. Coef"+nl)
            val_Strings.append("RD  :  Ref. Density  "+nl)
            val_Strings.append("A   :  Mass    number"+nl)
            val_Strings.append("Z   :  Atomic  number"+nl)

        if(self.skval_dict['Density']):
            if(all([len(rholab)>0,len(rhots)>0,len(rhons)>0,len(rhops)>0,len(rhoidx)>0])):
                den_Strings.append(str(strl.array_to_str(rholab, spc='  ', **kwargs))+"\n")
                den_Strings.append("\n")
                den_Strings.append("Total Density\n")
                for string in px.matrix_to_str_array(px.table_trans(rhots), spc='  ', roundUniform=True, pyver='2.6', **kwargs):
                    den_Strings.append(str(string)+"\n")
                den_Strings.append("\n")
                den_Strings.append("Neutron Density\n")
                for string in px.matrix_to_str_array(px.table_trans(rhons), spc='  ', roundUniform=True, pyver='2.6', **kwargs):
                    den_Strings.append(str(string)+"\n")
                den_Strings.append("\n")
                den_Strings.append("Proton Density\n")
                for string in px.matrix_to_str_array(px.table_trans(rhops), spc='  ', roundUniform=True, pyver='2.6', **kwargs):
                    den_Strings.append(str(string)+"\n")
                den_Strings.append("\n")
                den_Strings.append("\n")
                den_Strings.append("Index\n")
                for line in rhoidx:
                    den_Strings.append(line)
                den_Strings.append("\n")
                den_Strings.append("\n")

        if(eospars):
            output = (par_Strings, val_Strings, den_Strings)
        else:
            output = val_Strings, den_Strings
        return output


    def write_to_dat(self, file, data, **kwargs):

        kwargs = self.__update_funcNameHeader__("write_to_dat", **kwargs)

        datfilepath = self.joinNode(self.DATPATH, file, **kwargs)
        if(datfilepath == False):
            return False

        return iop.flat_file_write(datfilepath, data, **kwargs)

    #######
    # EOS #
    #######

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
                    msg = ["failure to coerce data into four arrays, check pathways:", "e0 path : "+str(e0_file_path), "e1 path : "str(e1_file_path)]
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


    def format_eos_data(self, eos_obj, parline, **kwargs):

        kwargs = self.__update_funcNameHeader__("format_eos_data", **kwargs)

        try:
            eoslist, eosid = eos_obj
        except:
            return self.__err_print__("should be an array of length two", varID='eos_obj',  **kwargs)

        output = ()
        exgp = []
        e0gp = []
        e1gp = []

        m = len(eoslist)

        if(m == 3):
            type = 0
            kf = eoslist[0]
            e0 = eoslist[1]
            e1 = eoslist[2]
            if(len(kf) == len(e0) and len(e0) == len(e1)):
                n = len(kf)
            else:
                return self.__err_print__("eos arrays should all be the same length", varID='eos_obj', **kwargs)
            exgp = map(lambda x,y,z: strl.array_to_str([x,y,z], spc='  ', endline=True), kf,e0,e1)
            eval = [exgp]
            neid = self.parse_eosid(eosid, 'ex', **kwargs)
            parline = self.update_parline([n,0], [0,2], parline, **kwargs)

        elif(m == 4):
            type = 1
            kf0 = eoslist[0]
            e0  = eoslist[1]
            kf1 = eoslist[2]
            e1  = eoslist[3]

            if(len(kf0) == len(e0)):
                n0 = len(kf0)
            else:
                return self.__err_print__("and the corrosponding kfs should be arrays with the same length", varID='e0', **kwargs)

            if(len(kf1) == len(e1)):
                n1 = len(kf1)
            else:
                return self.__err_print__("and the corrosponding kfs should be arrays with the same length", varID='e0', **kwargs)

            e0gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf0,e0)
            e1gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf1,e1)
            eval = [e0gp, e1gp]
            neid = self.parse_eosid(eosid, 'e10', **kwargs)
            parline = self.update_parline([1, n0, n1], [2, 3, 4], parline, **kwargs)

        else:
            return self.__err_print__("must a numeric array of length 2, 3 or 4", varID='eoslist', **kwargs)

        output = (type, eval, parline, neid)

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
                         clean_run=True,
                         **kwargs):

        kwargs = self.__update_funcNameHeader__("single_run", **kwargs)

        if(isinstance(exeline, str)):
            pass_exeline = self.write_parline(parline, type='exec', **kwargs)
            if(pass_line == False):
                msg = ["failure to create and write exec line", "'exeline' : "+str(exeline)]
                return self.__err_print__(msg, **kwargs)
        if(isinstance(rrdline, str)):
            pass_line = self.write_parline(parline, type='exec', **kwargs)
            if(pass_line == False):
                msg = ["failure to create and write exec line", "'rrdline' : "+str(rrdline)]
                return self.__err_print__(msg, **kwargs)
        if(isinstance(phnline, str)):
            pass_line = self.write_parline(parline, type='exec', **kwargs)
            if(pass_line == False):
                msg = ["failure to create and write exec line", "'phnline' : "+str(phnline)]
                return self.__err_print__(msg, **kwargs)

        self.set_osdir(self.BINPATH, **kwargs)
        self.run_commands(run_cmd, **kwargs)
        self.set_osdir(**kwargs)

        values_dict = self.read_files_from_folder('bin', result_files, clean=True, **kwargs)

        self.cycle+=1
        return (values_dict)



    def eos_loop(self, eoslist,
                       execvals,
                       readvals,
                       phenvals,
                       reset=True,
                       **kwargs):
        '''
        reset : [bool] (True), resets data files to pre-run values
        '''

        kwargs = self.__update_funcNameHeader__("eos_loop", **kwargs)

        isovals = {}
        isovals_group = {}

        if(self.__not_arr_print__(eoslist, varID='eoslist', **kwargs)):
            return False
        if(self.__not_arr_print__(execvals, varID='execvals', **kwargs)):
            return False
        if(self.__not_arr_print__(readvals, varID='readvals', **kwargs)):
            return False
        if(self.__not_arr_print__(phenvals, varID='phenvals', **kwargs)):
            return False

        if(not skval_run and not isinstance(osaz, (str,tuple))):
            return self.__err_print__("should be a tuple when not using 'skval_run' option", varID='osaz', **kwargs)
        else:
            if(not skval_run and isinstance(osaz, (str,tuple))):
                if(len(osaz) != 2):
                    return self.__err_print__("should have a length of two : '"+str(len(osaz))+"'", varID='osaz', **kwargs)

        # cycle through each EoS
        for i,eos in enumerate(eoslist):

            # Convert each EoS object into eos data (eos_inst) and eos id (eosid)
            formdat = self.format_eos_data(eos, execvals, readvals, phenvals, **kwargs)
            if(formdat == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS could not be formatted, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue
            # Set eos data (eos_instance) and 'par.don' line (parline)
            type, eos_instance, parlnlist, eosid = formdat

            # Pass the parameters to the appropriate files
            readfiles = self.write_parlnlist(parlnlist, **kwargs)
            if(readfiles == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS parameters not properly passed to 'bin', cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

            # Pass the eos data to the appropriate file
            success = self.write_eos(eos_instance, type, **kwargs)
            if(success == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS could not be passed to 'bin', cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

            isovals[eosid] = self.single_run(readfiles, **kwargs)
            if(isovals[eosid] == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" failed the 'skval_loop' routine, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

        if(reset):
            self.write_parline(self.initial_parline, **kwargs)
            self.write_vallist(self.initial_vallist, **kwargs)

        return benvals_group


    def isov_run(self, skval, reset=True, return_data=False, **kwargs):
        '''
        !Function which runs the SKVAL loop over the EOS!
        '''

        kwargs = self.__update_funcNameHeader__("isov_run", **kwargs)

        if(skval == ()):
            return self.__err_print__("needs to be set", varID='skval', **kwargs)

        # Get EoS from 'eos' folder
        eoslist = self.collect_eos()
        if(eoslist == False):
            return self.__err_print__("could not collect EoS data from 'eos' folder", **kwargs)

        # Put EoS and skval data in EoS loop
        benval_data = self.eos_loop(eoslist, skval,
                                    parline=self.initial_parline,
                                    initpar=self.skval_dict['Initpar'],
                                    mirrors=self.skval_dict['Mirrors'],
                                    density=self.skval_dict['Density'],
                                    reset  =self.skval_dict['Resetit'],
                                    **kwargs)

        formatted_isov_data = self.format_isov_data(benval_data,
                                                      self.skval_dict['EOSpars'],
                                                      self.skval_dict['EOSgrup'],
                                                      **kwargs)
        if(self.skval_dict['EOSpars']):
            par_Strings, val_Strings, den_Strings = formatted_benval_data
            self.write_to_dat(self.OUTPARS, par_Strings, **kwargs)
            self.write_to_dat(self.OUTVALS, val_Strings, **kwargs)
        else:
            val_Strings, den_Strings = formatted_benval_data
            self.write_to_dat(self.OUTVALS, val_Strings, **kwargs)

        if(self.skval_dict['Density']):
            self.write_to_dat(self.OUTDENS, den_Strings, **kwargs)

        if(return_data):
            return formatted_benval_data
        else:
            return True


    def set_isov_menu(self, **kwargs):

        kwargs = self.__update_funcNameHeader__("set_isov_menu", **kwargs)

        menu_lines = ["Input 'pars' to set initialize input parameters"
                      "Input 'run' isov program"
                      "Input 'eos' to run the 'eos' loop for set parameters",
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
                return True

        if(input == 'pars'):
            self.parline_generator(**kwargs)
        elif(input == 'run'):
            pass
        elif(input == 'eos'):
            run_attempt = self.isov_run(, **kwargs)
            if(run_attempt == False):
                print(self.space+"An error occured during 'benv' execution, see above for details\n")
            else:
                print(self.space+"ISOV 'eos' loop completed...\n")
        elif(input == 'cleardat'):
            self.clear_data_folder(**kwargs)
        else:
            return True
        return True