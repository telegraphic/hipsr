Introduction
============

HIPSR is a new reconfigurable digital backend for the Parkes multibeam receiver. HIPSR is capable of running many different firmware modes, so can be used for both high resolution, wide bandwidth spectral line observations, and high time resolution pulsar observations.

Architecture
------------

HIPSR consists of digitizer cards; FPGA digital processing boards for "low-level" DSP; 
a 10GbE switch for data interconnect; and, a CPU/GPU cluster for "high-level" DSP and data storage. The network architecture is shown in the figure below:

.. figure:: HIPSR_arch.png
    :scale: 100%
    :alt: HIPSR Architecture
    :align: center
    
    *Network architecture for HIPSR.*


