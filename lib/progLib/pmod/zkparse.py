# zkparse: Zeit-Kalendar (Time and Calender) parsing 
# clock: Calculating through time (both time and date)

import time
import datetime
import math as mt

import tcheck as check
import mathops as mops


# Zeit Functions:


### Helper functions

def __secs_counter__(zeit, nbool=False, dplace = 3):
    if(nbool):
        return [zeit]
    else:
        if(zeit == 1.):
            return str(str(int(zeit))+' sec')
        else:
            zeit = mops.round_decimal(zeit,dplace)
            return str(zeit)+' secs'              
    
def __mins_counter__(zeit, nbool=False):        
    mins = mt.floor(zeit/60.) 
    secs = zeit - mins*60.
    secs = __secs_counter__(secs,nbool)
    if(nbool):
        return [mins,secs[0]]        
    else:    
        if(mins == 1):
            return str(str(int(mins))+' min'+' & '+str(secs))
        else:
            return str(str(int(mins))+' mins'+' & '+str(secs))

def __hrs_counter__(zeit, nbool=False):           
    hrs = mt.floor(zeit/(3600.))
    secs_left = zeit - hrs*3600.
    mins = __mins_counter__(secs_left,nbool)
    if(nbool):
        return [hrs,mins[0],mins[1]]
    else: 
        if(hrs == 1):
            return str(str(int(hrs))+' hr, ' + str(mins))
        else:
            return str(str(int(hrs))+' hrs, ' + str(mins))
             
def __days_counter__(zeit, nbool=False):
    days = mt.floor(zeit/86400.)
    secs_left = zeit - days*86400.
    hrs = __hrs_counter__(secs_left,nbool)
    if(nbool):
        return [days,hrs[0],hrs[1],hrs[2]] 
    else:
        if(days == 1):
            return str(str(int(days))+' day, ' + str(hrs))
        else:
            return str(str(int(days))+' days, ' + str(hrs)) 

def __yrs_counter__(zeit, nbool=False):
    yrs = mt.floor(zeit/31536000.)
    secs_left = zeit - yrs*31536000.
    days = __days_counter__(secs_left,nbool)
    if(nbool):
        return [yrs,days[0],days[1],days[2],days[3]] 
    else:
        if(yrs == 1):
            return str(str(int(yrs))+' year, ' + str(days))
        else:
            return str(str(int(yrs))+' years, ' + str(days))

def __cent_counter__(zeit, nbool=False):
    cent = mt.floor(zeit/3153600000.)
    secs_left = zeit - cent*3153600000.
    yrs = __yrs_counter__(secs_left,nbool)
    if(nbool):
        return [cent,yrs[0],yrs[1],yrs[2],yrs[3],yrs[4]] 
    else:
        if(cent == 1):
            return str(str(int(cent))+' century, ' + str(yrs))
        else:
            return str(str(int(cent))+' centries, ' + str(yrs))

def __mil_counter__(zeit, nbool=False):
    mil = mt.floor(zeit/31536000000.)
    secs_left = zeit - mil*31536000000.
    cent = __cent_counter__(secs_left,nbool)
    if(nbool):
        return [mil,cent[0],cent[1],cent[2],cent[3],cent[4],cent[5]] 
    else:
        if(mil == 1):
            return str(str(int(mil))+' millennium , ' + str(cent))
        else:
            return str(str(int(mil))+' millennia , ' + str(cent))

def __cosmo_counter__(zeit, nbool=False):
    cosmo = mt.floor(zeit/(31536000000.*230000.))
    secs_left = zeit - cosmo*31536000000.*230000.
    mil = __mil_counter__(secs_left,nbool)
    if(nbool):
        return [cosmo,mil[0],mil[1],mil[2],mil[3],mil[4],mil[5],mil[6]] 
    else:
        if(cosmo == 1):
            return str(str(int(cosmo))+' cosmo, ' + str(mil))
        else:
            return str(str(int(cosmo))+' cosmos, ' + str(mil))

def __aeon_counter__(zeit, nbool=False):
    aeon = mt.floor(zeit/(31536000000.*1000000.))
    secs_left = zeit - aeon*31536000000.*1000000.
    cosmo = __cosmo_counter__(secs_left,nbool)
    if(nbool):
        return [aeon,cosmo[0],cosmo[1],cosmo[2],cosmo[3],cosmo[4],cosmo[5],cosmo[6],cosmo[7]] 
    else:
        if(aeon == 1):
            return str(str(int(aeon))+' aeon, ' + str(cosmo))
        else:
            return str(str(int(aeon))+' aeon, ' + str(cosmo))


### Main Zeit Functions 

def time_convert(zeit, inunit, outunit='sec'):
    '''
    Inputs: 

        zeit       : time input, must be castable to a float 
        inunit     : string input, must be a value in 'unit_list' 

        outunit[*} : = 'sec', string input: see inunit 


    Description : 

        Put a numeric value in 'zeit' and the time unit of 'zeit' in 'inunit'
        If you want the output in something other than seconds, place the 
        string value in 'outunit'. 

        The function converts time from one unit to another. 

    '''

    cosmo = 31536000000.*230000.
    aeon = 31536000000.*1000000.
    unit_list = ['sec','min','day','yr','cent','mil','cosmo','aeon'] 
    factor_list = [1.,60.,86400.,31536000.,3153600000.,31536000000.,cosmo,aeon]

    conv_dict = dict(zip(unit_list,factor_list))

    if(inunit not in unit_list):
        print("[time_convert] Error: "+str(inunit)+" not a recognized abbreviated unit of time")
        return False
    if(outunit not in unit_list):
        print("[time_convert] Error: "+str(outunit)+" not a recognized abbreviated unit of time")
        return False

    zeit = float(zeit)
    secs = zeit*conv_dict[inunit]

    if(outunit == 'sec'):
        return secs
    else:
        heure = secs/conv_dict[outunit]
        return heure


def time_parse_sec(zeit, nbool=False):
    '''
    Inputs: 

        zeit     : time input, must be castable to a float         
        nbool[*} : = False, boolean input: If True a list of numerics is output, else a string 


    Description : 

        Put a numeric value in 'zeit' which is the time units in seconds.
        The function converts time in seconds to time in scaled units.  
    
    '''     
                
    zeit = float(zeit)
    if(zeit < 0):
        zeit=-1.*zeit

    if (zeit < 1.):
        return secs_counter(zeit,nbool)
    elif (zeit< 60.):
        return secs_counter(zeit,nbool)
    elif (zeit < 3600.):
        return mins_counter(zeit,nbool)
    elif (zeit < 86400.):
        return hrs_counter(zeit,nbool)        
    elif (zeit < 31536000.):
        return days_counter(zeit,nbool) 
    elif (zeit < 3153600000.):
        return yrs_counter(zeit,nbool)
    elif (zeit < 31536000000.):
        return cent_counter(zeit,nbool)
    elif (zeit < 31536000000.*230000.):
        return mil_counter(zeit,nbool)
    elif (zeit < 31536000000.*1000000.):
        return cosmo_counter(zeit,nbool)
    else:
        return aeon_counter(zeit,nbool)
    

def time_parse(zeit, inunit, num_bool = False):
    '''
    Inputs: 

        zeit     : time input, must be castable to a float   
        inunit   : string input, must be a value in 'unit_list'
      
        num_bool[*} : = False, boolean input: If True a list of numerics is output, else a string 

    Description : 

        Put a numeric value in 'zeit' which is the time units in units of 'inunit'.
        The function converts time in units of the 'inunit' value to time in scaled units.  
         
    '''

    secs = time_convert(zeit,inunit)
    ptime = time_parse_sec(secs, num_bool = False)
    return ptime


### Clock class




class clock():
    '''
    class: clock
     
    Description:  
     
    '''

    def __init__(self, in_date = None, in_time = None):

        self.init_datetime = datetime.datetime.now()
        self.date = in_date
        self.time = in_time

    ##################                            ##################  
    # date functions ############################## date functions #
    ##################                            ##################        

    def __str_to_date_list__(self,string,delim='-'):
        test = check.type_test_print(string,str,'string','__str_to_date_list__') 
        if(not test):
            return test 
        
        array = string.split(delim)
        date_list = [int(array[2]),int(array[0]),int(array[1])]
        return date_list 

    def __date_list_to_str__(self,array):
        test = check.type_test_print(array,list,'array','__date_list_to_str__') 
        if(not test):
            return test 
         
        string = array[1]+'-'+array[2]+'-'+array[0] 
        return string

    def __date_str_to_str__(self,string):
        test = check.type_test_print(string,list,'string','__date_str_to_str__') 
        if(not test):
            return test 
        
        array = string.split('-') 
        string = array[1]+'-'+array[2]+'-'+array[0] 
        return string    
        
    def __date_list_to_ordate__(self, array):
        test = check.type_test_print(array,list,'array','__date_list_to_ordate__') 
        if(not test):
            return test 
                
        try:
            dateobj = datetime.date(int(array[0]),int(array[1]),int(array[2]))
            ordate = dateobj.toordinal()
            return ordate
        except:
            print("[__date_list_to_ordate__] Error: input array could not be parsed as a date_list")
            return False

    def __str_to_ordate__(self, string):
        date_list = self.__str_to_date_list__(string)
        if(date_list == False):
            return False         
        ordate = self.__date_list_to_ordate__(date_list) 
        if(ordate == False):
            return False
        else:
            return ordate      
          

    ##################                            ################## 
    # time functions ############################## time functions #
    ##################                            ##################

        # Set-up:
        # 
        # seconds through a day:
        #
        # 1 min = 60 s
        # 1 hr  = 60 min = 60*60 (= 3600) s 
        # 1 day = 24 hr  = 24*3600 (= 86400 s)
        #
        # 86400/4 = 21600 s     quarter day
        #
        # 86400/6 = 14400 s     sextile day = 120*120
        #
        # For a sextile hour system, the new day starts about sunset at 18:00:00 in 24 hr time 
        #
        # 00:00:00 :     0 s   ->    2:00:00:00 - second watch  
        # 06:00:00 : 21600 s   ->    3:00:00:00 - third watch 
        # 12:00:00 : 43200 s   ->    4:00:00:00 - fourth watch
        # 18:00:00 : 64800 s   ->    1:00:00:00 - first watch
        #
        # format: six hr (there are four 'watches')
        #
        # watch : hour : minute : second 


    def __str_to_time_list__(self,string,output=list):
        test = check.type_test_print(string,str,'string','__str_to_time_list__') 
        if(not test):
            return test
        string_split = string.split(':')
        hour = string_split[0]
        minute = string_split[1]
        second = string_split[2] 
        if(output == list):            
            array = [int(float(hour)),int(float(minute)),int(float(second))]
            return array
        elif(output == tuple):
            array = (int(float(hour)),int(float(minute)),int(float(second)))
            return array 
        else: 
            print("[__str_to_time_list__] Error: 'output' value, "+str(output)+" not recognized")
            return False
       
    def __convert_clock_18hr__(hour,minute,second):
        time_sec = int(second)+60*int(minute)+60*60*int(hour)
        hour = time_sec/4800
        sec_rem = time_sec-hour*4800
        minute = sec_rem/120
        sec_rem = sec_rem-minute*120
        second = sec_rem
        if(second < 10):
            second = '00'+str(second)
        elif(second < 100):
            second = "0"+str(second)
        else:
            second = str(second)
        if(minute < 10):
            minute = '0'+str(minute)
        else:
            minute = str(minute)
        if(hour < 10):
            hour = '0'+str(hour)
        else:
            hour = str(hour)
       
        time_str = str(hour)+':'+str(minute)+':'+str(second)
        return time_str


    def __convert_clock_16hr_hs__(hour,minute,second):
        time_sec = int(second)+60*int(minute)+60*60*int(hour)
        time_sec = time_sec/2
        hour = time_sec/2700
        sec_rem = time_sec-hour*2700
        minute = sec_rem/90
        sec_rem = sec_rem-minute*90
        second = sec_rem
        if(second < 10):
            second = '00'+str(second)
        elif(second < 100):
            second = "0"+str(second)
        else:
            second = str(second)
        if(minute < 10):
            minute = '0'+str(minute)
        else:
            minute = str(minute)
        if(hour < 10):
            hour = '0'+str(hour)
        else:
            hour = str(hour)
       
        time_str = str(hour)+':'+str(minute)+':'+str(second)+' HS'       
        return time_str
        
        
    def __convert_clock_15hr__(hour,minute,second):
        time_sec = int(second)+60*int(minute)+60*60*int(hour)
        hour = time_sec/5760
        sec_rem = time_sec-hour*5760
        minute = sec_rem/120
        sec_rem = sec_rem-minute*120
        second = sec_rem
        if(second < 10):
            second = '00'+str(second)
        elif(second < 100):
            second = "0"+str(second)
        else:
            second = str(second)
        if(minute < 10):
            minute = '0'+str(minute)
        else:
            minute = str(minute)
        if(hour < 10):
            hour = '0'+str(hour)
        else:
            hour = str(hour)
       
        time_str = str(hour)+':'+str(minute)+':'+str(second)

    
    def __convert_clock_12hr__(hour,minute,second):
        
        midday = 43200 

        time_sec = int(second)+60*int(minute)+60*60*int(hour)

        if(time_sec >= midday):                
            watch = 1
            time_sec = time_sec - midday
        else:
            watch = 0
 
        hour = time_sec/3600
        sec_rem = time_sec-hour*3600
        minute = sec_rem/60
        sec_rem = sec_rem-minute*60
        second = sec_rem            
         
        if(second < 10):
            second = '0'+str(second)
        else:
            second = str(second)
        if(minute < 10):
            minute = '0'+str(minute)
        else:
            minute = str(minute)
        hour = str(hour)            
         
        if(watch == 0):        
            time_str = str(hour)+':'+str(minute)+':'+str(second)+' AM'
        else:                
            time_str = str(hour)+':'+str(minute)+':'+str(second)+' PM'
        return time_str
         

    def __convert_clock_6hr__(hour,minute,second):

        sixsec = 21600
        newday = 64800 

        time_sec = int(second)+60*int(minute)+60*60*int(hour)

        if(time_sec >= newday):
            watch = 1
        else:
            watch = (time_sec/sixsec)+2  

        sec_left = time_sec%sixsec 
        hour = sec_left/3600
        sec_rem = sec_left-hour*3600
        minute = sec_rem/60
        sec_rem = sec_rem-minute*60
        second = sec_rem            
         
        if(second < 10):
            second = '0'+str(second)
        else:
            second = str(second)
        if(minute < 10):
            minute = '0'+str(minute)
        else:
            minute = str(minute)
        hour = str(hour)            

        time_str = str(watch)+':'+str(hour)+':'+str(minute)+':'+str(second) 
        return time_str

    ######################                     ######################  
    # datetime functions ####################### datetime functions #
    ######################                     ######################

    def __dtobj_check__(self,testobj,name=None):
        dtobj = datetime.datetime            
        if(isinstance(testobj,dtobj)):
            return True 
        else: 
            if(name == None):
                print("[__dtobj_check__] Error: input is a "+str(type(testobj))+" and not a datetime object")
            else:
                print("[__dtobj_check__] Error: '"+str(name)+"' is a "+str(type(testobj))+" and not a datetime object")
            return False

    def __str_to_datetime__(self,datestr,timestr=None):
        try:
            datelist = self.__str_to_date_list__(datestr)            
            if(timestr == None):
                timelist = [0,0,0]
            else:
                timelist = self.__str_to_time_list__(timestr)
        except:
            print("[__str_to_datetime__] Error: input strings could not be parsed as a datetime object")
            return False

        dl0,dl1,dl2 = datelist
        tl0,tl1,tl2 = timelist
        dt_obj = datetime.datetime(int(dl0),int(dl1),int(dl2),int(tl0),int(tl1),int(tl2))
        return dt_obj

    def __datetime_to_str__(self,datetime,output='datetime'):

        chk = self.__dtobj_check__(dt,'dt')
        if(not chk):
            return False

        datevals = ['DATE','Date','date']
        timevals = ['TIME','Time','time']
        datetimevals = ['DATETIME','Datetime','datetime']

        date_str = str(datetime.date())
        time_str = str(datetime.time())

        date_str = self.__date_str_to_str__(date_str)
         
        if(output in datetimevals):
            return (date_str,time_str)       
        elif(output in datevals):
            return date_str 
        elif(output in time_str):
            return time_str 
        else:
            print("[__datetime_to_str__] Error: 'output' not recognized")
            return False       

    def __datetime_rel__(self,dt1,dt2):

        chk1 = self.__dtobj_check__(dt1,'dt1')
        chk2 = self.__dtobj_check__(dt2,'dt2') 

        if(not chk1 or not chk2):
            return False
           
        if(dt1 > dt2):
            return dt1
        elif(dt2 > dt1):
            return dt2 
        else:
            return cont
        
    def __datetime_dif__(self,dt1,dt2,output=None):

        '''
        'output' options:

        'sec' or None  : returns integer, total number of seconds between datetime instances 
        'days'         : returns integer, floor rounded number of days between datetime instances
        'int' or 'tup' : returns tuple, tuple version of raw difference between datetime instances 
        'raw'          : returns datetime.deltatime instance, 
                         returns raw result of the difference between datetime instances 
        '''

        chk1 = __dtobj_check__(self,dt1,'dt1')
        chk2 = __dtobj_check__(self,dt2,'dt2') 

        if(not chk1 or not chk2):
            return False            

        dt_dif_raw = dt1 - dt2 
        
        if(output == 'sec' or output == '' or output == None):
            out_val = dt_dif_raw.total_seconds()
            return out_val
        elif(output == 'days'):
            out_val= dt_dif_raw.days
        elif(output == 'int' or 'tup'):
            out_val = (dt_dif_raw.days,dt_dif_raw.seconds)    
            return out_val 
        elif(output == 'raw'):
            return dt_dif_raw
        else:
            return False

    def __datetime_addtime__(self,dt,secs,neg=False,days=0):

        chk1 = __dtobj_check__(self,dt,'dt')
        if(not chk1):
            return False 
         
        test = check.type_test_print(secs,int,'secs','__datetime_addtime__') 
        if(not test):
            return test      
        test = check.type_test_print(days,int,'days','__datetime_addtime__') 
        if(not test):
            return test

        if(neg):
           coef=-1
        else:
           coef=1  
        
        try:
            delt_t = datetime.timedelta(days,secs)
            final_dt = dt+coef*delt_t
        except:
            print("[__datetime_addtime__] Error: adding 'secs' to datetime object 'dt' failed")
            return False 
          
        return final_dt
                              

    ##################                             ##################  
    # Main functions ############################### Main functions #
    ##################                             ##################

    ######################
    # Datetime functions # : Returns datetime data
    ######################
            
    def get_datetime(self,value='datetime',form='str',indt=None):
        
        if(indt == None):  
            datetime_now = datetime.datetime.now()
        else:
            test = check.type_test_print(indt,'arr','indt','get_datetime') 
            if(not test):
                return test
            if(len(indt) < 2):
                print("[get_datetime] Error: 'indt' should be an array with a length of 2")
                return False
            for i in indt:
                test = check.type_test_print(i,str,'indt','get_datetime') 
                if(not test):
                    print("[get_datetime] Error: 'indt' should contain two strings; corrosponding to date and time")
                    return test                      
            dstr = indt[0]
            tstr = indt[1]
            datetime_now = self.__str_to_datetime__(dstr,tstr)
        
        date_now = datetime_now.date()  
        time_now = datetime_now.time()   
                                                     
        datevals = ['DATE','Date','date']
        timevals = ['TIME','Time','time']
        datetimevals = ['DATETIME','Datetime','datetime']


        time_str = str(datetime_now).split(' ')[1]         
        time_list = time_str.split(':')
        time_int = [int(time_list[0]),int(time_list[1]),int(round(float(time_list[2]),0))]
        time_num = [int(time_list[0]),int(time_list[1]),float(time_list[2])]
                     
        if(value in timevals):
            if(form == 'raw'):
                return time_now
            elif(form == 'int'):   
                return time_int
            elif(form == 'num'):
                return time_num
            elif(form == 'list'):                
                return time_list
            elif(form == 'str'):
                return time_str
            else:
                print("[get_datetime] Error: 'form' value, "+form+" not recognized")
                return False

        date_str = str(datetime_now).split(' ')[0]
        date_list = date_str.split('-')     
        date_str = self.__date_list_to_str__(date_list)    
        date_list = [date_list[1],date_list[2],date_list[0]]
        date_int = [int(date_list[0]),int(date_list[1]),int(date_list[2])]

        if(value in datevals):
            if(form == 'raw'):
                return date_now
            elif(form == 'int' or form == 'num'):                
                return date_int
            elif(form == 'list'):
                return date_list
            elif(form == 'str'):
                return date_str
            else:
                print("[get_datetime] Error: 'form' value, "+form+" not recognized")
                return False       

        dt_int = (date_int,time_int)
        dt_num = (date_int,time_num)
        dt_list = (date_list,time_list)
        dt_str = (date_str,time_str)
     
        if(value in datetimevals):
            if(form == 'raw'):
                return datetime_now
            elif(form == 'int'):                     
                return dt_int
            elif(form == 'num'):                
                return dt_num
            elif(form == 'list'):                
                return dt_list
            elif(form == 'str'):
                return dt_str
            else:
                print("[get_datetime] Error: 'form' value, "+form+" not recognized")
                return False

        else:
            print("[get_datetime] Error: 'value' "+value+" not recognized; no action taken")
            return False

    ##################
    # Date functions #
    ##################

    # Dates are all entered in Standard American Format mm/dd/yyyy (e.g. 06/30/2055 )
    # If no date is entered the current date is assumed

    def get_days_between_dates(self,early,later):
        tot = self.__str_to_ordate__(early)
        if(tot == False):
            return False 

        tard = self.__str_to_ordate__(later)
        if(tard == False):
            return False                     
              
        day_dif = int(tard) - int(tot) 
        if(day_dif < 0):
            day_dif = (-1)*day_dif
        
        return day_dif


    def get_weekday(self,string):
        test = check.type_test_print(string,str,'string','get_weekday') 
        if(not test):
            return test         

        date_list = self.__str_to_date_list__(string)
        if(date_list == False):
            return False

        year, month, day = date_list
        
        weekday_nums  = [i for i in range(7)]
        weekday_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Sunday'] 
        weekday_dict = dict(zip(weekday_nums,weekday_names))

        weekday_val = datetime.date(year, month, day).weekday()
        return weekday_dict[weekday_val]


    def get_time_til_date(self,date,now=None,format=None):
        '''
        Description: Returns time (seconds) between 'current' date and future 'date' value           
        '''
        if(isinstance(now,None) or isinstance(now,list) or isinstance(now,tuple)):                
            current = self.get_datetime(value='datetime',form='raw',indt=now)
        elif(isinstance(now,str)): 
            current = self.__str_to_date_list__(now)
        else:
            print("[get_time_til_date] Error: 'now' type, "+str(type(now))+" not valid")
        future = self.__str_to_datetime__(date)
         
        difference = self.__datetime_dif__(future,current,output=format)
        return difference            
         
        
    def get_date_after_time(self,zeit,date=None,in_form='sec',out_form='date'):

        datevals = ['DATE','Date','date']
        timevals = ['TIME','Time','time']
        datetimevals = ['DATETIME','Datetime','datetime']
        
        
        if(isinstance(date,None)):
            current = self.get_datetime(value='datetime',form='raw',indt=date) 
        elif(isinstance(date,list) or isinstance(date,tuple)): 
            current = self.get_datetime(value='datetime',form='raw',indt=date) 
        elif(isinstance(date,str)):     
            current = self.__str_to_datetime__(date)
        
        if(in_form != 'sec'):
            zeit = time_convert(zeit,in_form)

        future = self.__datetime_addtime__(current,zeit)
           
        dt_vals = self.__datetime_to_str__(future,out_form) 
        return dt_vals
         
         
    ##################
    # Time functions #
    ##################

    # Time is entered as standard 24hr digital formated strings: hh-mm-ss [all integers]: (e.g. 14-30-59)
       
    def get_time(self, time = None, heure = None):
        
        if(time != None):
            array_bool = check.type_test_print(time,'arr',name='time',func_name='get_time')
            if(isinstance(time,list) or isinstance(time,tuple)):
                hour = int(time[0])
                minute = int(time[1])
                second = int(time[2])
            elif(isinstance(time,str)):
                time_array = time.split(':')
                hour = int(time_array[0])
                minute = int(time_array[1])
                second = int(time_array[2])
            else:
                print("[get_time] Error: 'time' object must be string or list/tuple; not a "+str(type(time))) 
                return False
        else:
            cdt = self.get_datetime('Time','list')
            hour = int(cdt[0])
            minute = int(cdt[1])
            second = int(round(float(cdt[2]),0))        
        
        if(heure == None or heure == '24' or heure == ''):
            if(second < 10):
                second = '0'+str(second)
            else:
                second = str(second)
            if(minute < 10):
                minute = '0'+str(minute)
            else:
                minute = str(minute)
            if(hour < 10):
                hour = '0'+str(hour)
            else:
                hour = str(hour)
            time_str = str(hour)+':'+str(minute)+':'+str(second)           
        elif(heure == '18'):
            time_str = __convert_clock_18hr__(hour,minute,second)
        elif(heure == '16hs'):
            time_str = __convert_clock_16hr_hs__(hour,minute,second)                 
        elif(heure == '15'):
            time_str = __convert_clock_15hr__(hour,minute,second)        
        elif(heure == '12'):
            time_str = __convert_clock_12hr__(hour,minute,second)
        elif(heure == '6'):
            time_str = __convert_clock_6hr__(hour,minute,second)
        else:
            print("[] Error: 'heure' hour parameter, "+str(heure)+" not recognized")      
            return False          
        return time_str


