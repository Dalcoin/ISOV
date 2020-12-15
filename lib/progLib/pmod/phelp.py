from matplotlib import pyplot as __plt__

import tcheck as __check__
import mathops as __mops__

# Graphing functions


def __ecc_plot__(x, y, label = None, lims = None, fontsize = 20, save = False, save_name = 'plot.jpg'):
    '''
    __ecc_plot__ : Error correction code plot 

    return tuple: (xarray, yarray ,labre, limre, fontsize, save, save_name)
    '''
    # ECC

    # Dummy Check for 'x' and 'y'
    if(not __check__.array_test(x)):
        print("[__ecc_plot__] Error: 'x' must be an array")  
        return False    
    if(not __check__.array_test(y)):
        print("[__ecc_plot__] Error: 'y' must be an array") 
        return False      
            
    # Checking 'x' for proper formating
    xnumeric = True 
    xarray = True
    for i in x:
        if(__check__.numeric_test(i)):
            xarray = False 
        elif(__check__.array_test(i)):
            xnumeric = False 
            for j in i:
                if(not __check__.numeric_test(j)):
                    xarray = False
        else:
            xnumeric, xarray = False, False 
    if(xarray == False and xnumeric == False):
        print("[__ecc_plot__] Error: input 'x' must either be a numeric array or an array of numeric arrays") 
        return False

    # Checking 'y' for proper formating              
    ynumeric = True 
    yarray = True
    for i in y:
        if(__check__.numeric_test(i)):
            yarray = False 
        elif(__check__.array_test(i)):
            ynumeric = False 
            for j in i:
                if(not __check__.numeric_test(j)):
                    yarray = False
        else:
            ynumeric, yarray = False, False 
    if(yarray == False and ynumeric == False):
        print("[__ecc_plot__] Error: input 'y' must either be a numeric array or an array of numeric arrays") 
        return False
    
    # Special check for a set of y arrays   

    if(yarray and not xarray):
        for i in xrange(len(y)):
            if(len(x) != len(y[i])): 
                print("[__ecc_plot__] Error: 'x' should corrospond 1-to-1 for each array in 'y'")
                return False
         
    if(xarray and not yarray):
        print("[__ecc_plot__] Error: if 'x' is an array of arrays, then 'y' must be as well")
        return False    
           
    if(xarray):
        if(len(x) != len(y)):
            print("[__ecc_plot__] Error: if 'x' is an array of arrays, then it must have the same length as 'y'")
            return False
        else:
            for i in xrange(len(x)):
                if(len(x[i]) != len(y[i])): 
                    errmsg = "[__ecc_plot__] Warning: each respective entry of 'x' "
                    errmsg = errmsg + "should corrospond 1-to-1 to the 'y' entry"
                    print(errmsg)    
                    return False
     
    # Label checks            
    labre = False
    if(not __check__.array_test(label)):
        if(label != None):
            print("[__ecc_plot__] Warning: input 'label' is not an array and has been deprecated") 
        labre = True  
    else:
        if(len(label) < 2):
            print("[__ecc_plot__] Warning: input 'label' has a length less than 2 and has been deprecated") 
            labre = True
        else:
            xlabel, ylabel = label[0], label[1]
            if(not isinstance(xlabel,str)):
                print("[__ecc_plot__] Warning: input 'xlabel' is not string so 'label and has been deprecated")      
                labre = True        
            if(not isinstance(ylabel,str)):
                print("[__ecc_plot__] Warning: input 'ylabel' is not string so 'label and has been deprecated") 
                labre = True                         
              
    # Limit checks
             
    limre = False
    if(not __check__.array_test(lims)):
        if(lims != None):
            print("[__ecc_plot__] Warning: input 'lims' is not an array and has been deprecated") 
        limre = True  
    else:
        if(len(lims) < 2):
            print("[__ecc_plot__] Warning: input 'lims' has a length less than 2 and has been deprecated") 
            limre = True
        else:
            xlims, ylims = lims[0], lims[1]
            if(__check__.array_test(xlims)):
                if(not __check__.numeric_test(xlims[0]) or not __check__.numeric_test(xlims[1])):
                    print("[__ecc_plot__] Warning: input 'xlims' is not string so 'lims and has been deprecated")    
                    limre = True 
            else:
                limre = True 
            if(__check__.array_test(ylims)):
                if(not __check__.numeric_test(ylims[0]) or not __check__.numeric_test(ylims[1])):
                    print("[__ecc_plot__] Warning: input 'ylims' is not string so 'lims and has been deprecated")  
                    limre = True      
            else:
                limre = True          
                                   
    # Checking the rest of the input variables
    if(__check__.numeric_test(fontsize)):
        fontsize = int(fontsize)
    else:
        fontsize = 30 
             
    if(not isinstance(save,bool)):
        save = False          

    if(not isinstance(save_name, str)):
        save_name = 'plot.jpg'    
             
    output = (xarray, yarray ,labre, limre, fontsize, save, save_name)
    return output
              

def new_plot(x, y, label = None, lims = None, fontsize = 30, save = False, save_name = 'plot.jpg'):

    test = __ecc_plot__(x, y, label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: input test failed, see preceding error msg for details")
        return False  
    else:
        xarray, yarray ,labre, limre, fontsize, save, save_name = test
        
    xysep, ysep, sep = False, False, False
    if(xarray and yarray): 
        xysep = True 
    elif(yarray):
        ysep = True 
    else:
        sep = True 

    if(labre):
        label = (None, None)
    if(limre):
        lims = (None, None)

    xlab, ylab = label[0], label[1]
    xlim, ylim = lims[0], lims[1]

                   
    __plt__.figure()
    __plt__.rc('xtick',labelsize=16)
    __plt__.rc('ytick',labelsize=16)
     
    if(sep):
        __plt__.plot(x, y, linewidth = 2.5)
    elif(ysep):
        for i in y:
            __plt__.plot(x, i, linewidth = 2.5)
    elif(xysep):
        for i in xrange(len(x)):
            __plt__.plot(x[i], y[i], linewidth = 2.5)
         
    if(xlab != None):
        __plt__.ylabel(ylab, fontsize = fontsize, labelpad = 20)
    if(ylab != None):
        __plt__.xlabel(xlab, fontsize = fontsize, labelpad = 20)
    if(xlim != None):
        __plt__.xlim(xlim[0],xlim[1])
    if(ylim != None):
        __plt__.ylim(ylim[0],ylim[1])
             
    __plt__.show()
    if(save):
        __plt__.savefig(save_name)    
    return True  


def new_smooth_plot(x, y, label = None, lims = None, smoothness = 300,
                    fontsize = 30, save = False, save_name = 'plot.jpg'):    

    test = __ecc_plot__(x, y, label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: input test failed, see preceding error msg for details")
        return False  
    else:
        xarray, yarray ,labre, limre, fontsize, save, save_name = test
        
    xysep, ysep, sep = False, False, False


    if(xarray and yarray): 
        xysep = True 
    elif(yarray):
        ysep = True 
    else:
        sep = True 

    if(labre):
        label = (None, None)
    if(limre):
        lims = (None, None)

    xlab, ylab = label[0], label[1]
    xlim, ylim = lims[0], lims[1]

    spln_inst = __mops__.spline()
                   
    __plt__.figure()
    __plt__.rc('xtick',labelsize=16)
    __plt__.rc('ytick',labelsize=16)

    if(sep):
        xsmooth = __mops__.span_vec(x, smoothness)  
        spln_inst.pass_vecs(x, y, xsmooth)
              
        spln_inst.pass_spline()
        ysmooth = spln_inst.get_spline()   

        __plt__.plot(xsmooth, ysmooth, linewidth = 2.5)

    elif(ysep):
        for i in y:
            xsmooth = __mops__.span_vec(x, smoothness)  
            spln_inst.pass_vecs(x, i, xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   

            __plt__.plot(xsmooth, ysmooth, linewidth = 2.5)

    elif(xysep):
        for i in xrange(len(x)):
            xsmooth = __mops__.span_vec(x[i], smoothness)  
            spln_inst.pass_vecs(x[i], y[i], xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   

            __plt__.plot(xsmooth, ysmooth, linewidth = 2.5)

    if(xlab != None):
        __plt__.ylabel(xlab, fontsize = fontsize, labelpad = 20)
    if(ylab != None):
        __plt__.xlabel(ylab, fontsize = fontsize, labelpad = 20)
    if(xlim != None):
        __plt__.xlim(xlim[0],xlim[1])
    if(ylim != None):
        __plt__.ylim(ylim[0],ylim[1])
             
    __plt__.show()
    if(save):
        __plt__.savefig(save_name)    
    return True  




def new_four_plot(tl_data, tr_data, bl_data, br_data, 
                  fontsize = 20, lwd = 2.5, 
                  label = None, lims = None, namelab = None, 
                  smooth = False, smoothness = 300, 
                  save = False, save_name=None):

    fig, axs = __plt__.subplots(2, 2, sharex=False, sharey=False)

    tl_xysep, tl_ysep, tl_sep = False, False, False
    tr_xysep, tr_ysep, tr_sep = False, False, False
    bl_xysep, bl_ysep, bl_sep = False, False, False
    br_xysep, br_ysep, br_sep = False, False, False

    if(smooth):
        spln_inst = __mops__.spline()
    
    if(not __check__.array_test(label)):
        tl_label, tr_label, bl_label, br_label = [[' ',' '],[' ',' '],[' ',' '],[' ',' ']]        
    else:
        if(len(label) != 4): 
            tl_label, tr_label, bl_label, br_label = [[' ',' '],[' ',' '],[' ',' '],[' ',' ']]
        else:
            tl_label = label[0]
            tr_label = label[1]
            bl_label = label[2]
            br_label = label[3]
           
    try:
        x,y = tl_data
    except:
        print("Error: input data 'tl_data' must be a python array of length two")
    test = __ecc_plot__(x, y, tl_label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: 'tl_data' (top-left) data test failed, see preceding error msg for details")
        return False  
    else:
        tl_xarray, tl_yarray , tl_labre, tl_limre, tl_fontsize, save, save_name = test

        if(tl_xarray and tl_yarray): 
            tl_xysep = True 
        elif(tl_yarray):
            tl_ysep = True 
        else:
            tl_sep = True 
	    
        if(tl_labre):
            tl_label = (None, None)
        if(tl_limre):
            tl_lims = (None, None)


    try:
        x,y = tr_data
    except:
        print("Error: input data 'tr_data' must be a python array of length two")
    test = __ecc_plot__(x, y, tr_label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: 'tr_data' (top-right) data test failed, see preceding error msg for details")
        return False  
    else:
        tr_xarray, tr_yarray , tr_labre, tr_limre, tr_fontsize, save, save_name = test

        if(tr_xarray and tr_yarray): 
            tr_xysep = True 
        elif(tr_yarray):
            tr_ysep = True 
        else:
            tr_sep = True 
	    
        if(tr_labre):
            tr_label = (None, None)
        if(tr_limre):
            tr_lims = (None, None)
               
             
    try:
        x,y = bl_data
    except:
        print("Error: input data 'bl_data' must be a python array of length two")
    test = __ecc_plot__(x, y, bl_label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: 'bl_data' (bottom-left) data test failed, see preceding error msg for details")
        return False  
    else:
        bl_xarray, bl_yarray , bl_labre, bl_limre, bl_fontsize, save, save_name = test

        if(bl_xarray and bl_yarray): 
            bl_xysep = True 
        elif(bl_yarray):
            bl_ysep = True 
        else:
            bl_sep = True 
	    
        if(bl_labre):
            bl_label = (None, None)
        if(bl_limre):
            bl_lims = (None, None)
               
    try:
        x,y = br_data
    except:
        print("Error: input data 'br_data' must be a python array of length two")
    test = __ecc_plot__(x, y, br_label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: 'br_data' (bottom-right) data test failed, see preceding error msg for details")
        return False  
    else:
        br_xarray, br_yarray , br_labre, br_limre, br_fontsize, save, save_name = test

        if(br_xarray and br_yarray): 
            br_xysep = True 
        elif(br_yarray):
            br_ysep = True 
        else:
            br_sep = True 
	    
        if(br_labre):
            br_label = (None, None)
        if(br_limre):
            br_lims = (None, None)
            

    # Top-Left plot     

    x,y = tl_data 

    if(tl_sep):

        if(smooth):
            xsmooth = __mops__.span_vec(x, smoothness)  
            spln_inst.pass_vecs(x, y, xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   
            tempx = xsmooth
            tempy = ysmooth
        else:
            tempx = x
            tempy = y
            
        axs[0,0].plot(tempx, tempy, linewidth = lwd)

    elif(tl_ysep):
        for i in y:
            if(smooth): 
                xsmooth = __mops__.span_vec(x, smoothness)  
                spln_inst.pass_vecs(x, i, xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth
            else:
                tempx = x
                tempy = i
                 
            axs[0,0].plot(tempx, tempy, linewidth = lwd)

    elif(tl_xysep):
        for i in xrange(len(x)):
            if(smooth): 
                xsmooth = __mops__.span_vec(x[i], smoothness)  
                spln_inst.pass_vecs(x[i], y[i], xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth               
            else:
                tempx = x[i]
                tempy = y[i]

            axs[0,0].plot(tempx, tempy, linewidth = lwd)

    if(namelab != None):
        try:
            axs[0,0].set_title(str(namelab[0]))
        except:
            pass          

    if(tl_label != (None,None)):
        axs[0,0].set(xlabel=tl_label[0], ylabel=tl_label[1])

    # Top-Right plot     

    x,y = tr_data 

    if(tr_sep):

        if(smooth):
            xsmooth = __mops__.span_vec(x, smoothness)  
            spln_inst.pass_vecs(x, y, xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   
            tempx = xsmooth
            tempy = ysmooth
        else:
            tempx = x
            tempy = y
            
        axs[0,1].plot(tempx, tempy, linewidth = lwd)

    elif(tr_ysep):
        for i in y:
            if(smooth): 
                xsmooth = __mops__.span_vec(x, smoothness)  
                spln_inst.pass_vecs(x, i, xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth
            else:
                tempx = x
                tempy = i
                 
            axs[0,1].plot(tempx, tempy, linewidth = lwd)

    elif(tr_xysep):
        for i in xrange(len(x)):
            if(smooth): 
                xsmooth = __mops__.span_vec(x[i], smoothness)  
                spln_inst.pass_vecs(x[i], y[i], xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth               
            else:
                tempx = x[i]
                tempy = y[i]

            axs[0,1].plot(tempx, tempy, linewidth = lwd)

    if(namelab != None):
        try:
            axs[0,1].set_title(str(namelab[1]))
        except:
            pass    

    if(tr_label != (None,None)):
        axs[0,1].set(xlabel=tr_label[0], ylabel=tr_label[1])
    
    # Bottom-Left plot     

    x,y = bl_data 

    if(bl_sep):

        if(smooth):
            xsmooth = __mops__.span_vec(x, smoothness)  
            spln_inst.pass_vecs(x, y, xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   
            tempx = xsmooth
            tempy = ysmooth
        else:
            tempx = x
            tempy = y
            
        axs[1,0].plot(tempx, tempy, linewidth = lwd)

    elif(bl_ysep):
        for i in y:
            if(smooth): 
                xsmooth = __mops__.span_vec(x, smoothness)  
                spln_inst.pass_vecs(x, i, xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth
            else:
                tempx = x
                tempy = i
                 
            axs[1,0].plot(tempx, tempy, linewidth = lwd)

    elif(bl_xysep):
        for i in xrange(len(x)):
            if(smooth): 
                xsmooth = __mops__.span_vec(x[i], smoothness)  
                spln_inst.pass_vecs(x[i], y[i], xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth               
            else:
                tempx = x[i]
                tempy = y[i]

            axs[1,0].plot(tempx, tempy, linewidth = lwd)

    if(namelab != None):
        try:
            axs[1,0].set_title(str(namelab[2]))
        except:
            pass 

    if(bl_label != (None,None)):
        axs[1,0].set(xlabel=bl_label[0], ylabel=bl_label[1])   
    
    
    # Bottom-Right plot     

    x,y = br_data 

    if(br_sep):

        if(smooth):
            xsmooth = __mops__.span_vec(x, smoothness)  
            spln_inst.pass_vecs(x, y, xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   
            tempx = xsmooth
            tempy = ysmooth
        else:
            tempx = x
            tempy = y
            
        axs[1,1].plot(tempx, tempy, linewidth = lwd)

    elif(br_ysep):
        for i in y:
            if(smooth): 
                xsmooth = __mops__.span_vec(x, smoothness)  
                spln_inst.pass_vecs(x, i, xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth
            else:
                tempx = x
                tempy = i
                 
            axs[1,1].plot(tempx, tempy, linewidth = lwd)

    elif(br_xysep):
        for i in xrange(len(x)):
            if(smooth): 
                xsmooth = __mops__.span_vec(x[i], smoothness)  
                spln_inst.pass_vecs(x[i], y[i], xsmooth)
                      
                spln_inst.pass_spline()
                ysmooth = spln_inst.get_spline()   
                tempx = xsmooth
                tempy = ysmooth               
            else:
                tempx = x[i]
                tempy = y[i]

            axs[1,1].plot(tempx, tempy, linewidth = lwd)
    if(namelab != None):
        try:
            axs[1,1].set_title(str(namelab[3]))
        except:
            pass    

    if(br_label != (None,None)):
        axs[1,1].set(xlabel=br_label[0], ylabel=br_label[1])
        
    __plt__.tight_layout()
    __plt__.show()
        
    if(save):
        try:
            fig.savefig(save_name)
        except:
            print("Error: attempted and failed to print graph as "+str(save_name))
       
    return True
