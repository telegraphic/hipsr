.. HIPSR documentation master file, created by

Gateware
========

Overview
--------

The MSSGE toolflow (short for Matlab/Simulink/System Generator/EDK) is the platform
for FPGA-based CASPER development, which stitches together several design and implementation 
environments.

It is better known as the bee_xps toolflow, which was developed at the Berkeley Wireless 
Research Center (BWRC) as a high-level design tool for the BEE and BEE2 platforms. We have 
extended it to work with all other CASPER boards as well. It provides a graphical 
Matlab/Simulink design environment using the Xilinx System Generator Toolbox, 
and abstracts the Xilinx implementation details behind a one-click compile interface.

For installation instructions, see the MSSGE Toolflow page:

* https://casper.berkeley.edu/wiki/MSSGE_Toolflow

HISPEC-8192 Wideband Spectrometer
---------------------------------

**Current gateware: hispec_8192_v2_2013_Apr_18_1730.bof**

This is a 400 MHz bandwidth, 8192-channel polyphase filterbank. The filterbank
is 4-taps, with hamming-windowed coefficients. It is discussed in more detail
in the memo below:

:download:`HISPEC 8192 firmware memo <spectrometers_report.pdf>`.

The current version also includes noise diode control for noise adding radiometer-based
calibration.

============================================  ========================  ======
Logic distribution and feature utilization
============================================  ========================  ======
  Number of occupied Slices:                    14,330 out of  14,720     97%
  Number of BlockRAM/FIFO:                         244 out of     244    100%
  Number of DSP48Es:                               318 out of     640     49%
============================================  ========================  ======

HISPEC-zoom GPU Spectrometer
----------------------------

TODO.

Pulsar modes
------------

The CASPSR firmware is based on the Packetized Astronomy Signal Processor
firmware designed by Terry Filiba. The BPSR firmware is based on the Parspec
firmware designed by Peter Macmahon and ported to ROACH by Danny Price.

ADC to Ten Gigabit Ethernet
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current gateware: adc_to_10gbe_2011_Oct_18_1156.bof**

CASPSR uses a stripped out PASP. It has a more accurate reset, and just turns the ADC input 
into 10GE packets. 

* https://casper.berkeley.edu/wiki/Packetized_Astronomy_Signal_Processor

**Resource utilization summary**

This design fitted onto an iBOB, so unsuprisingly isn't pushing the ROACH in any
way.

============================================  ========================  ======
Logic distribution and feature utilization
============================================  ========================  ======
  Number of occupied Slices:                     6,258 out of  14,720     42%
  Number of BlockRAM/FIFO:                          21 out of     244      8%
    Total Memory used (KB):                        720 out of   8,784      8%
============================================  ========================  ======


Parkes Spectrometer (Parspec)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current gateware: parspec_01_2011_Oct_12_1520.bof**

Parspec is a 400MHz bandwidth, 1024 channel, 2-tap polyphase filterbank based 
spectrometer. 

* https://casper.berkeley.edu/wiki/Parspec

**Resource utilization summary**

Parspec was designed and spec'd to fit onto an iBOB; now it's been ported to
ROACH it feels positively roomy. 

============================================  ========================  ======
Logic distribution and feature utilization
============================================  ========================  ======
  Number of occupied Slices:                     6,171 out of  14,720     41%
  Number of BlockRAM/FIFO:                          85 out of     244     34%
  Number of DSP48Es:                               164 out of     640     25%
============================================  ========================  ======  

  