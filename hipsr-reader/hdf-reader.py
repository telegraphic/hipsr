# encoding: utf-8
"""
hdf-reader.py
=============

Copyright (c) 2012 The HIPSR collaboration. All rights reserved.\n

A few plotting routines to give a feel for the HIPSR5 file format.
""" 

__version__ = "0.1"
__author__  = "Danny Price"

import time,sys,os
from datetime import datetime

import numpy as np, tables as tb
import pylab as plt

def plotStuff(filename):
    """ Open a HDF file and run a few plotting routines """
    
    print "Opening %s"%filename
    print "--------------------"
    h5 = tb.openFile(filename)      
    print h5

    
    print "Observation details"
    print "-------------------"
    observation = h5.root.observation
    col_names   = observation.coldescrs.keys()
    row_val     = observation[0]
    for i in range(len(col_names)):
        print "%s: \t %s"%(col_names[i], observation.col(col_names[i])[0])
        
    
    # Plot a spectrogram of frequency vs time of beam_01
    print "\nPlotting spectrum vs. time"
    print "--------------------------"
    beam_01    = h5.root.raw_data.beam_01
    timestamps = beam_01.cols.timestamp 
    xx         = beam_01.cols.xx[:]         # For very large datasets this is a bad idea
    
    print xx.shape
    square_aspect = float(xx.shape[1])/float(xx.shape[0])    
    plt.imshow(10*np.log10(xx), aspect=square_aspect)
    plt.colorbar()
    plt.xlabel("Channel (-)")
    plt.ylabel("Integration number (-)")
    plt.show()
    
    
    print "\nPlotting beam power"
    print "-------------------"
    # Plot the power as a function of time for each beam
    multibeam = h5.root.raw_data
    for beam in multibeam:
      print "processing %s"%beam.name
      timestamps = beam.cols.timestamp
      xx         = beam.cols.xx
      
      if len(xx) < 500:
          pow =  np.average(xx, axis=1)
          pow = 10*np.log10(pow / np.min(pow))
          ts   = [datetime.utcfromtimestamp(t) for t in timestamps]
      else:
          skip = len(xx) / 100
          pow = np.average(xx[::skip])
          pow = 10*np.log10(pow / np.min(pow))
          ts   = [datetime.utcfromtimestamp(t) for t in timestamps[::skip]]
      
      plt.plot(ts, pow, label=beam.name)
    
    plt.xticks(rotation=30)
    plt.ylabel("Power (dB)")
    plt.xlabel("Time (UTC)")
    plt.legend()
    plt.show()
    h5.close()
    

if __name__ == "__main__":

    # Option parsing
    from optparse import OptionParser
    p = OptionParser()
    p.set_usage('hdf-reader.py [filename]')
    p.set_description(__doc__)
    (options, args) = p.parse_args(sys.argv[0:])
    
    try:
        filename = args[1]
    except:
        print "Error: could not open file. Have you specified one? \nUsage: \n>> python hdf-reader.py [filename]"
        exit()
    try:
        plotStuff(filename)
    except:
        print "Error: something's up with the plotting routine."
        raise
    
    
    