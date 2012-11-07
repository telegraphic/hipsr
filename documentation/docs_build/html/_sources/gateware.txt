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

Spectral line modes
-------------------

HIPSR Wideband Spectrometer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current gateware: hipsr_16_2011_Oct_01_0824.bof**

This is a 400MHz bandwidth, 8192 channel polyphase filterbank. The filterbank
is 4-taps, with hamming window coefficients. 

.. figure:: PFB_response.png
    :width: 650px
    :alt: PFB response vs FFT response
    :align: center
    
    *Filterbank response for different numbers of taps. We are using 4-taps in
    this 8192 channel design.*



The registers that can be used to control the board logic are listed below.

===============  ============================================================
Register          Description
===============  ============================================================
quant_gain        Gain used in quantization, accepts an eight bit
                  number which sets the shift before quantisation.
                  Values under 00001111 shift the data to the left;
                  values over  00001111 shift the data to the right.
mux_sel           Digital noise source or the ADC? A value of 1 selects
                  the digital noise source, and 0 selects the ADC input.
fft_shift         FFT shift, selects which stages of the FFT the bits are
                  shifter to the left. Accepts 12 bits, one bit for each
                  stage in the FFT. For example, 111111111111 shifts every
                  stage, and 010101010101 shifts every second stage.
acc_len	          Number of accumulations, in clock cycles. As the FPGA
                  is clocked at 200MHz, and there are 8192 channels, a
                  value of 24414 corresponds to 1 second. The maximum
                  value is 2^18 accumulations, which gives about 10s,
                  although care must be taken to ensure there is no overflow.
===============  ============================================================


**Resource utilization summary**

The design uses a fair proportion of slices and BRAMs, but there is a fair
amount of DSP48E logic left.

============================================  ========================  ======
Logic distribution and feature utilization
============================================  ========================  ======
  Number of occupied Slices:                    10,305 out of  14,720     70%
  Number of LUT Flip Flop pairs used:           36,261                    
    Number with an unused Flip Flop:             2,830 out of  36,261      7%
    Number with an unused LUT:                   9,846 out of  36,261     27%
    Number of fully used LUT-FF pairs:          23,585 out of  36,261     65%
    Number of unique control sets:                 167                    
    Number of slice register sites lost                                   
      to control set restrictions:                 229 out of  58,880      1%
  Number of BlockRAM/FIFO:                         191 out of     244     78%
    Number using BlockRAM only:                    191                    
    Total primitives used:                                                
      Number of 36k BlockRAM used:                 185                    
      Number of 18k BlockRAM used:                  12                    
    Total Memory used (KB):                      6,876 out of   8,784     78%
  Number of DSP48Es:                               222 out of     640     34%
============================================  ========================  ======


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

===============  ============================================================
Register          Description
===============  ============================================================
todo              todo.

===============  ============================================================

**Resource utilization summary**

This design fitted onto an iBOB, so unsuprisingly isn't pushing the ROACH in any
way.

============================================  ========================  ======
Logic distribution and feature utilization
============================================  ========================  ======
  Number of occupied Slices:                     6,258 out of  14,720     42%
  Number of LUT Flip Flop pairs used:           16,637                    
    Number with an unused Flip Flop:             6,747 out of  16,637     40%
    Number with an unused LUT:                   3,378 out of  16,637     20%
    Number of fully used LUT-FF pairs:           6,512 out of  16,637     39%
    Number of unique control sets:                 459                    
    Number of slice register sites lost                                   
      to control set restrictions:               1,041 out of  58,880      1%
  Number of BlockRAM/FIFO:                          21 out of     244      8%
    Number using BlockRAM only:                     21                    
    Total primitives used:                                                
      Number of 36k BlockRAM used:                  12                    
      Number of 18k BlockRAM used:                  16                    
    Total Memory used (KB):                        720 out of   8,784      8%
============================================  ========================  ======


Parkes Spectrometer (Parspec)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current gateware: parspec_01_2011_Oct_12_1520.bof**

Parspec is a 400MHz bandwidth, 1024 channel, 2-tap polyphase filterbank based 
spectrometer. 

* https://casper.berkeley.edu/wiki/Parspec

===============  ============================================================
Register          Description
===============  ============================================================
todo              todo.

===============  ============================================================

**Resource utilization summary**

Parspec was designed and spec'd to fit onto an iBOB; now it's been ported to
ROACH it feels positively roomy. 

============================================  ========================  ======
Logic distribution and feature utilization
============================================  ========================  ======
  Number of occupied Slices:                     6,171 out of  14,720     41%
  Number of LUT Flip Flop pairs used:           20,028                   
    Number with an unused Flip Flop:             3,139 out of  20,028     15%
    Number with an unused LUT:                   5,881 out of  20,028     29%
    Number of fully used LUT-FF pairs:          11,008 out of  20,028     54%
    Number of unique control sets:                 349                   
    Number of slice register sites lost                                  
      to control set restrictions:                 728 out of  58,880      1%
  Number of BlockRAM/FIFO:                          85 out of     244     34%
    Number using BlockRAM only:                     85                   
    Total primitives used:                                               
      Number of 36k BlockRAM used:                  10                   
      Number of 18k BlockRAM used:                 119                   
    Total Memory used (KB):                      2,502 out of   8,784     28%
  Number of DSP48Es:                               164 out of     640     25%
============================================  ========================  ======  

  