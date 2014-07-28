# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 19:38:59 2014

@author: Charles LE LOSQ
Carnegie Institution of Washington
"""

#Function for transforming Raw spectrum in transmitance then in absorbance spectrum
import numpy as np
from pylab import *
from StringIO import StringIO

def FTIRout(nameR,nameB,nameout,thick): # FUNCTION TO CALCULATE THE ABSORBANCE SPECTRA
    
    # WARNING: adjust skip_header and skip_footer to your files before running the function    
    
    #Initial FTIR SIGNAL
    #fr = open(nameR,'r')  ##### CHANGE NAME
    #sr = fr.read()
    spectreR = np.genfromtxt(nameR, skip_header= 19, skip_footer = 30)
    
    #Initial BACKGROUND
    #fb = open(nameB,'r') ##### CHANGE NAME
    #sb = fb.read()
    spectreB = np.genfromtxt(nameB, skip_header= 19, skip_footer = 30)
    
    # Building transmittance spectrum
    x = spectreR[:,0]
    w = np.divide(spectreR[:,1],spectreB[:,1])
    
    #  Transmittance - Absorbance conversion and thickness normalisation
    w2 = -np.log10(w)/thick # calculation of normalized absorbance
    
    #
    spectreout = np.zeros((len(x),2))
    spectreout[:,0] = x
    spectreout[:,1] = w2
    # We remove possible nan values
    spectreout = spectreout[~np.isnan(spectreout).any(1)]
    
    # data are out in this directory
    np.savetxt(nameout,spectreout)
    
    return spectreout
    #%%
def FTIRfft(name2): # FUNCTION FOR CORRECTING IR SPECTRA OF INTERFERENCE
    
    ##Initial FTIR SIGNAL
    fr = open(name2,'r')  ##### CHANGE NAME
    sr = fr.read()
    spectre = np.genfromtxt(StringIO(sr))
    
    # Now we will make the fft of the signal
    x = spectre[:,0]
    y = spectre[:,1]
    
    N = len(y)
    a = spectre[1000,0]-spectre[999,0]
    L = a * N
    
    sp = np.fft.fft(y)
    k = 2*np.pi*np.arange(len(sp))/L
    
    bp = sp[:]
    # filtering
    for i in range(len(bp)): # (H-red)  
        if i>=10:
            bp[i]=0  
            
    # signal filtred        
    ibp = np.fft.ifft(bp)    
    
    
    plot(x,y,'r-',x,ibp,'g-')
    
    
    #%%
def FTIRcomp(names, listelg, plotdisplay, nameout): # FUNCTION TO PLOT TOGETHER THREE SPECTRA
    
    # We will have at least 1 file so...
    # >Will use it for having the lenght of files (they must have the same of course)   
    x = np.arange(750,7300,0.5)  # Common X axis
  
    spectre1 = np.genfromtxt(names[0]) #reading data
    spectre1 = spectre1[~np.isnan(spectre1).any(1)] # protection over nan
    sp1 = np.interp(x,spectre1[:,0],spectre1[:,1]) # resampling
    
    lg = len(names) # number of files
    datas = np.zeros((len(x),lg+1)) # output matrix
    datas[:,0] = x # x values
    datas[:,1] = sp1 # first spectrum
    
    # We make some efforts for contructing data matrix with other spectra
    if lg > 1:
        for idx in range(1,lg):
            sp = np.genfromtxt(names[idx]) # reading data
            sp = sp[~np.isnan(sp).any(1)] #protection over nan
            datas[:,idx+1] = np.interp(x,sp[:,0],sp[:,1]) # resampling and recording
    
    if plotdisplay == 1:
        ## Now we do the plots
        for idx in range(lg):            
            plot(x, datas[:,idx+1],color=(0.9-0.2*idx,0,0.1+0.2*idx))
            
        legend(listelg[:])   
        plt.xlabel('Wavenumber, $cm^{-1}$', fontsize = 18)
        plt.ylabel('Absorbance', fontsize = 18)     
    
    # data are out in this directory
    np.savetxt(nameout,datas)
        
    savefig(nameout+".pdf", bbox_inches='tight')
    
    return datas