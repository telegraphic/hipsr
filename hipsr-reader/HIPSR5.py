# encoding: utf-8
"""
HIPSR5.py
=============

Created by Danny Price on 2011-10-05.
Copyright (c) 2011 The HIPSR collaboration. All rights reserved.\n

Functions for creating HIPSR5 data files. The HIPSR5 data format is the
main storage format for data taken with HIPSR. It is based on HDF5, which
is superior to FITS in pretty much every way:\n
http://www.hdfgroup.org/HDF5/
""" 

__version__ = "0.2"
__author__  = "Danny Price"

import time,sys,os
from datetime import datetime

# Data and math handling
import numpy as np, tables as tb

class Spectrum(tb.IsDescription):
  """ PyTables table descriptor: storage of spectral data """
  id        = tb.Int32Col(pos=0)            # Unique ID
  timestamp = tb.Time64Col(pos=1)           # Timestamp (at BRAM read)
  xx        = tb.UInt32Col(shape=8192,pos=2) # XX Autocorrelation data
  yy        = tb.UInt32Col(shape=8192,pos=3) # YY Autocorrelation data
  re_xy     = tb.Int32Col(shape=8192,pos=4) # XY Cross correlation - real
  im_xy     = tb.Int32Col(shape=8192,pos=5) # XY Cross correlation - imag
  fft_of    = tb.BoolCol(pos=6)             # FFT overflow flag
  adc_clip  = tb.BoolCol(pos=7)             # ADC clipping flag
    
class FirmwareConfig(tb.IsDescription):
  """PyTables table descriptor: storage of basic setup parameters"""
  firmware          = tb.StringCol(64, pos=0) # Firmware name - e.g. hipsr_16.bof
  quant_xx_gain	    = tb.Int32Col(pos=1)      # Gain used in quantization - XX
  quant_yy_gain	    = tb.Int32Col(pos=1)      # Gain used in quantization - XX
  quant_xy_gain	    = tb.Int32Col(pos=1)      # Gain used in quantization - XX
  mux_sel	        = tb.Int32Col(pos=1)      # Digital noise source or the ADC?
  fft_shift	        = tb.Int32Col(pos=2)      # FFT shift
  acc_len	        = tb.Int32Col(pos=3)      # Number of accumulations per dump
  iadc_controller	= tb.Int32Col(pos=4)      # Not really sure what this is, but adc info
  
class Observation(tb.IsDescription):
  """PyTables table descriptor: observation details"""
  telescope     = tb.StringCol(32, pos=0)    # Telescope name (always Parkes for us)
  receiver      = tb.StringCol(32, pos=1)    # Receiver name (MULTI for us)
  date          = tb.Time64Col(pos=2)        # Date - only 32bits reqd for date but using 64
  project_id    = tb.StringCol(32, pos=3)    # Project ID number, PXXX for Parkes
  project_name  = tb.StringCol(255, pos=4)   # Project name
  observer      = tb.StringCol(255, pos=5)   # Observer's name
  num_beams     = tb.Int8Col(pos=6)          # Number of beams being used  
  ref_beam      = tb.Int8Col(pos=7)          # Reference beam
  feed_rotation = tb.StringCol(64, pos=8)    # Feed rotation (e.g. STEPPED)
  #feed_angle    = tb.Float32Col(pos=9)      # Feed angle
  acc_len       = tb.Float32Col(pos=9)       # Accumulation length, in seconds
  bandwidth     = tb.Int32Col(pos=10)        # Bandwidth (MHz) (-ve means inverted)
  dwell_time    = tb.Float32Col(pos=11)      # Dwell time (sec)
  frequency     = tb.Float32Col(pos=12)      # Central frequency (check this)
  
class Weather(tb.IsDescription):
  """PyTables table descriptor: weather details"""
  timestamp      = tb.Time64Col(pos=0)       # Timestamp at telescope pointing
  temperature    = tb.Float32Col(pos=1)      # Ambient temperature (K)
  pressure       = tb.Float32Col(pos=2)      # Pressure (kPa)
  humidity       = tb.Float32Col(pos=3)      # Humidity (%)
  wind_speed     = tb.Float32Col(pos=4)      # Wind Speed (m/s)
  wind_direction = tb.Float32Col(pos=5)      # Wind Direction (deg)  
  
class Pointing(tb.IsDescription):
  """PyTables table descriptor: telescope pointing details"""
  timestamp   = tb.Time64Col(pos=0)      # Timestamp at telescope pointing
  source      = tb.StringCol(255,pos=1)  # Name of source
  ra          = tb.Float32Col(pos=2)     # Right Ascension (radians)
  dec         = tb.Float32Col(pos=3)     # Declination (radians)
  feed_angle  = tb.Float32Col(pos=4)     # Feed angle
  freq_switch = tb.BoolCol(pos=5)        # Frequency switching flag
  
    
def createSingleBeam(filename, path='./'):
    """ Create a new HDF5 file and populate with table structure for single beam
    
    returns pyTables h5 object
    
    Parameters
    ----------
    filename: string
      filename of the file to be created
    path:
      path to the file, defaults to current directory.
    """
    
    print('Creating new HDF5 file %s in %s'%(filename, path))
    h5 = tb.openFile(os.path.join(path, filename), mode = 'w')
    
    print('Creating data tables...')
    beam_01 = h5.createGroup('/', 'beam_01', 'Multibeam reciver 01')
    a_data  = h5.createTable(beam_01, 'data')
    
    config  = h5.createTable('/', 'roach_config', FirmwareConfig)
    obs     = h5.createTable('/', 'observation', Observation)
    obs.attr.units = {
        'feed_angle' : 'deg', 
        'acc_len' : 's', 
        'bandwidth':'MHz',
        'dwell_time' : 's'
        }

    pointing = h5.createTable('/', 'pointing', Pointing, 'Telescope pointing details')
    pointing.attrs.units = { 
        'ra' : 'deg', 
        'dec' : 'deg',
        'feed_angle' : 'deg'
        }

    weather = h5.createTable('/', 'weather', Weather, 'Weather Details')
    weather.attrs.units = { 
        'temperature'     : 'K',
        'pressure'        : 'kPa',
        'humidity'        : '%',
        'wind_speed'      : 'm/s',
        'wind_direction'  : 'deg'
        }
    
    
    h5.flush()
    
    return h5

def createMultiBeam(filename, path='./', num_beams=13):
    """ Create a new HDF5 file and populate with table structure for multibeam receiver
    
    returns pyTables h5 object
    
    Parameters
    ----------
    filename: string
      filename of the file to be created
    path: string
      path to the file, defaults to current directory.
    num_beams: int
      number of beams, should be 1, 7 or 13. Defaults to 13
    """
    
    print('Creating new HDF5 file %s in %s'%(filename, path))
    h5 = tb.openFile(os.path.join(path, filename), mode = 'w')
    
    print('Creating data tables...')
    raw_data = h5.createGroup('/', 'raw_data', 'raw data (from FPGA)')
    for id in range(1,num_beams+1):
      print('Creating multibeam receiver table %s of %s...'%(id,num_beams))

      h5.createTable(raw_data, 'beam_%02i'%id, Spectrum, 'Multibeam receiver beam %02s'%id)
    
    config = h5.createTable('/', 'firmware_config', FirmwareConfig, 'Firmware Configuration')
    
    obs = h5.createTable('/', 'observation', Observation, 'Observation Details')
    obs.attrs.units = {
        'feed_angle' : 'deg', 
        'acc_len' : 's', 
        'bandwidth':'MHz',
        'dwell_time' : 's'
        }

    pointing = h5.createTable('/', 'pointing', Pointing, 'Telescope pointing details')
    pointing.attrs.units = { 
        'ra' : 'deg', 
        'dec' : 'deg',
        'feed_angle' : 'deg'
        }


    weather = h5.createTable('/', 'weather', Weather, 'Weather Details')
    weather.attrs.units = { 
        'temperature'     : 'K',
        'pressure'        : 'kPa',
        'humidity'        : '%',
        'wind_speed'      : 'm/s',
        'wind_direction'  : 'deg'
        }
    
    h5.flush()
    
    return h5

def hdfWriter(h5, data):
  """ Writes data to a HDF file """
  print "HIPSR5 Writer: Starting I/O FIFO"
  
  # Set up file handlers
  tbPointing       = h5.root.pointing
  tbData           = h5.root.raw_data
  tbObservation    = h5.root.observation
  tbData           = h5.root.raw_data
  tbFirmwareConfig = h5.root.firmware_config 

  def writePointing():
    #tbPointing.row["id"]        = data["pointing"]["id"]
    tbPointing.row["timestamp"] = data["pointing"]["timestamp"]
    tbPointing.row["ra"]        = data["pointing"]["ra"]
    tbPointing.row["dec"]       = data["pointing"]["dec"]
    tbPointing.row["feed_angle"]= data["pointing"]["feed_angle"]
    tbPointing.row.append()
    tbPointing.flush()

  def writeObservation():
    tbObservation.row["telescope"]      = data["observation"]["telescope"]
    tbObservation.row["receiver"]       = data["observation"]["receiver"]
    tbObservation.row["frequency"]      = data["observation"]["frequency"]
    tbObservation.row["date"]           = data["observation"]["date"]
    tbObservation.row["project_id"]     = data["observation"]["project_id"]
    #tbObservation.row["project_name"]  = data["observation"]["project_name"]
    #tbObservation.row["observer"]      = data["observation"]["observer"]
    tbObservation.row["acc_len"]        = data["observation"]["acc_len"]
    tbObservation.row["bandwidth"]      = data["observation"]["bandwidth"]
    tbObservation.row["num_beams"]      = data["observation"]["num_beams"]
    tbObservation.row["ref_beam"]       = data["observation"]["ref_beam"]
    tbObservation.row["feed_rotation"]  = data["observation"]["feed_rotation"]
    tbObservation.row["dwell_time"]     = data["observation"]["dwell_time"]
    #tbObservation.row["conf_name"]     = data["observation"]["project_id"]
    
    tbObservation.row.append()
    tbObservation.flush()
  
  def writeData():
    for key in data["raw_data"].keys():
      beam = h5.getNode('/raw_data',key)
      beam.row["id"]         = data["raw_data"][key]["id"]
      beam.row["timestamp"]  = data["raw_data"][key]["timestamp"]
      beam.row["xx"]         = data["raw_data"][key]["xx"]
      beam.row["yy"]         = data["raw_data"][key]["yy"]
      beam.row["re_xy"]      = data["raw_data"][key]["re_xy"]
      beam.row["im_xy"]      = data["raw_data"][key]["im_xy"]
      beam.row["fft_of"]     = data["raw_data"][key]["fft_of"]
      beam.row["adc_clip"]   = data["raw_data"][key]["adc_clip"]
      beam.row.append()
      beam.flush()
      
  def writeWeather():
    tbWeather.row["timestamp"]       = data["weather"]["timestamp"]
    tbWeather.row["temperature"]     = data["weather"]["temperature"]
    tbWeather.row["pressure"]        = data["weather"]["pressure"]
    tbWeather.row["humidity"]        = data["weather"]["humidity"]
    tbWeather.row["wind_speed"]      = data["weather"]["wind_speed"]
    tbWeather.row["wind_direction"]  = data["weather"]["wind_direction"]
    tbWeather.row.append()
    tbWeather.flush()
      
  def writeFirmwareConfig():                
    tbFirmwareConfig.row["firmware"]        = data["firmware_config"]["firmware"]
    tbFirmwareConfig.row["quant_xx_gain"]   = data["firmware_config"]["quant_xx_gain"]
    tbFirmwareConfig.row["quant_yy_gain"]	= data["firmware_config"]["quant_yy_gain"]
    tbFirmwareConfig.row["quant_xy_gain"]	= data["firmware_config"]["quant_xy_gain"]
    tbFirmwareConfig.row["mux_sel"]	        = data["firmware_config"]["mux_sel"]
    tbFirmwareConfig.row["fft_shift"]	    = data["firmware_config"]["fft_shift"]
    tbFirmwareConfig.row["acc_len"]	        = data["firmware_config"]["acc_len"]
    tbFirmwareConfig.row["iadc_controller"] = data["firmware_config"]["iadc_controller"]

  def keyNotFound():
      print "Warning: key not found."
          
  def validKeys(key):    
   return  {
      'pointing'    : writePointing,
      'raw_data'    : writeData,
      'observation' : writeObservation,
      'weather'     : writeWeather,
      'firmware'    : writeFirmwareConfig
    }.get(key, keyNotFound)()
    
  for key in data.keys():
    validKeys(key)

if __name__ == "__main__":
    x = createMultiBeam('test.h5', num_beams=13)
    print x
    x.close()