import itertools

import ioparse as iop
import strlist as strl
import pinax as px

from tcheck import imprimerTemplate
from mathops import spline

# conversion functions

# Work in progress...

class eos(spline):

    def __init__(self, state, energy):

        super(eos, self).__init__(self, space="    ",
                                        endline="\n",
                                        failPrint=True,
                                        x_vec=None,
                                        y_vec=None,
                                        new_x_vec=None)

        self.__set_funcNameHeader__("eos", **kwargs)
        self.state = state
        self.energy = energy




    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        kwargs = {}
        kwargs = self.__update_funcNameHeader__("state", **kwargs)
        if(self.__not_numarr_print__(value, **kwargs)):
            return None
        else:
            self._state = value
            self.x_vec = self._state

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        kwargs = {}
        kwargs = self.__update_funcNameHeader__("energy", **kwargs)
        if(self.__not_numarr_print__(value, **kwargs)):
            return None
        else:
            self._energy = value
            self.y_vec = self._energy

    def convert_kf(self, gam=2.0):
        self.state = np.array(list(map(lambda x: self.kf2den(x, gam), self.state)))
        return self.state

    def convert_den(self, gam=2.0):
        self.state = np.array(list(map(lambda x: self.den2kf(x, gam), self.state)))
        return self.state

    def kf2den(self, kf, gam):
        return gam*(kf*kf*kf)/(3.0*pi2)

    def den2kf(self, den, gam):
        return pow((3.0*pi2*den/gam),1.0/3.0)


def read_eos(file_name, header=False, entete=False, transpose=True, genre=float, **pkwargs):

    table = flat_file_intable(file_name, header, entete, transpose, genre, funcName=['read_eos'])
    if(table == False):
        return False

    if(len(table) == 2):
        return [eos(table[0],table[1])]
    elif(len(table) == 3):
        return [eos(table[0],table[1]),eos(table[0],table[2])]
    elif(len(table) == 4):
        return [eos(table[0],table[1]),eos(table[2],table[3])]
    else:
        return False



def convert(self, value, style, roundValue=None):
    '''
    
    notes: possible 'style' option
            
        style = 'sym2den'
        style = 'asym2den'
        style = 'den2sym'
        style = 'den2asym'
        style = 'sym2asym'
        style = 'asym2sym'           

    '''

    if(isinstance(roundValue, int)):
        if(roundValue >= 0):
            rnd = True
    if(convert == 'sym2den'):
        if(listopt):
            if(rnd):
                return [round(kf2den(entry,2.0),roundValue) for entry in value]
            else:
                return [kf2den(entry,2.0) for entry in value]        
        else:
            if(rnd):
                return round(kf2den(value,2.0),roundValue)
            else:
                return kf2den(value,2.0)
    elif(convert == 'asym2den'):
        if(listopt):
            if(rnd):
                return [round(kf2den(entry,1.0),roundValue) for entry in value]  
            else:
                return [kf2den(entry,1.0) for entry in value]
        else:
            if(rnd):
                return round(kf2den(value,1.0),roundValue)
            else:
                return kf2den(value,1.0)    
    elif(convert == 'den2sym'):
        if(listopt):
            if(rnd):
                return [round(den2kf(entry,2.0),roundValue) for entry in value]
            else:
                return [den2kf(entry,2.0) for entry in value]
        else:
            if(rnd):
                return round(den2kf(value,2.0),roundValue)
            else:
                return den2kf(value,2.0)
    elif(convert == 'den2asym'):
        if(listopt):
            if(rnd):
                return [round(den2kf(entry,1.0),roundValue) for entry in value]
            else:
                return [den2kf(entry,1.0) for entry in value]
        else:
            if(rnd):
                return round(den2kf(value,1.0),roundValue)
            else:
                return den2kf(value,1.0)  
    elif(convert == 'sym2asym'):
        if(listopt):
            if(rnd):
                return [round(pow(2,1.0/3.0)*entry,roundValue) for entry in value]
            else:
                return [pow(2,1.0/3.0)*entry for entry in value]
        else:
            if(rnd):
                return round(pow(2,1.0/3.0)*value)            
            else:
                return pow(2,1.0/3.0)*value
    elif(convert == 'asym2sym'):
        if(listopt):
            if(rnd):
                return [round(entry/pow(2,1.0/3.0),roundValue) for entry in value]
            else:
                return [entry/pow(2,1.0/3.0) for entry in value]  
        else:
            if(rnd):
                return round(value/pow(2,1.0/3.0),roundValue) 
            else:
                return value/pow(2,1.0/3.0) 
    else:
        return False  


def fileConvert(fileName, style, header = False, newFile = None):
    '''

    notes: 

        fileName : the name of a eos file in the same directory as the script
        style    : see 'convert' function for possible options 
        header   : Set to True if there is a header, else keep as False 
        newFile  : if None, the original file will be overwritten with the EoS
                   if a string, a new file with a name equal to the string will be created and filled with the EoS
                   if True, a list of the strings corrosponding to the EoS will be returned. 
   '''

    lines = iop.flat_file_intable(fileName, header = header, entete=True)
    
    if(header): 
        modLines = convertFunc(lines[0][1:], convert = style, round_Value = 4)
        modLines.insert(0,lines[0][0])
    else:
        modLines = convertFunc(lines[0], convert = style, round_Value = 4) 
    
    lines[0] = modLines     
    newLines = px.table_trans(lines)      

    outLines = map(lambda x: strl.array_to_str(x,spc ='    ',endline=True), newLines)

    if(newFile == None):
        iop.flat_file_write(fileName,outLines)
    elif(isinstance(newFile,str)):
        iop.flat_file_write(newFile,outLines)
    else:
        return outLines
    return True


# Constants

pi = 3.141592653589793 # pi - 16 digits 
hc = 197.327           # hc - Standard Nuclear Conversion Constant
pi2 = pi*pi            # pi squared
                       
mnuc = 938.918         # Nucleon Mass-Energy 
mneu = 939.5656328     # Neutron Mass-Energy   
mprt = 938.2720881629  # Proton Mass-Energy  
melc = 0.51099895      # Electron Mass-Energy 
mmun = 105.658375523   # Muon Mass-Energy    
                       
vmhc = pi*hc*mnuc/2.0  # (pi/2) hc [MeV^-2] -> fm Conversion Constant      

kf_vals_20 = [i*0.1 for i in xrange(1,21)]  
qf_vals_20 = [hc*float(i) for i in kf_vals_20]
pf_vals_20 = [int(i) for i in qf_vals_20]

sm_vals_20 = [2.0*i*i*i/(3.0*pi2) for i in kf_vals_20]    
nm_vals_20 = [i*i*i/(3.0*pi2) for i in kf_vals_20]   