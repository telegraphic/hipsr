.. HIPSR documentation master file, created by

Hardware
========
This page details the hardware in use in the HIPSR system. HIPSR consists of digitizer
cards; FPGA digital processing boards for "low-level" DSP; a 10GbE switch for data
interconnect; and, a CPU/GPU cluster for "high-level" DSP and data storage.

CASPER ROACH boards
-------------------

ROACH (Reconfigurable Open Architecture Computing Hardware) is a standalone 
FPGA processing board, developed by the Collaboration for Astronomy Signal Processing
and Electronics Research.

The centrepiece of ROACH is a Xilinx Virtex 5 FPGA (SX95T). 
A separate PowerPC runs Linux and is used to control the board (program the FPGA 
and allow interfacing between the FPGA "software registers/BRAMs/FIFOs" and external
devices using Ethernet).

Two quad data rate (QDR) SRAMs provide high-speed, medium-capacity memory 
(specifically for doing corner-turns), and one DDR2 DIMM provides slower-speed, 
high-capacity buffer memory for the FPGA. The PowerPC has an independent DDR2 DIMM
in order to boot Linux/BORPH.

The two Z-DOK connectors allow ADC, DAC and other interface cards to be attached to the 
FPGA, in the same manner as the IBOB allowed (with backwards compatibility for the ADC 
boards used with the IBOB).

Four CX4 connectors provide a total of 40Gbits/sec bandwidth for connecting ROACH boards
together, or connecting them to other XAUI/10GbE-capable devices (such as 
computers with 10GbE NICs and 10GbE switches).

For more detailed descriptions, see:

* https://casper.berkeley.edu/wiki/Main_Page
* https://casper.berkeley.edu/wiki/ROACH
* https://casper.berkeley.edu/wiki/ROACH_Architecture

iADC digitizer cards
--------------------
Each HIPSR ROACH board is populated with an iADC digitizer card. These cards are
based on the Atmel/e2V AT84AD001B 8-bit Dual 1Gsps ADC:

* http://www.e2v.com/assets/media/files/documents/broadband-data-converters/doc0817I.pdf

More information about the card is available at:

* https://casper.berkeley.edu/wiki/ADC2x1000-8

Cisco switch
------------

We will be loaning a CISCO C4900M switch from CASS, with the following specs:

=================   =======================================================
Item                  Description
=================   =======================================================
WS-C4900M             CISCO Base system with 8 X2 ports and 2 half slots
S49MIPBK9-15002SG     CISCO Cisco CAT4900M IOS IP BASE SSH 
PWR-C49M-1000AC       CISCO 4900M AC power supply, 1000 watts 
PWR-C49M-1000AC/2     CISCO Redundant AC PS for 4900M 
CAB-AS3112-C15-AU     CISCO AS-3112 to IEC-C15 8ft Aus 
MEM-C4K-FLD128M       CISCO Catalyst 4900M Compact Flash, 128MB Option 
4900M-X2-CVR          CISCO X2 cover on 4900M

WS-X4908-10GE=        CISCO 8 port 2:1 10GbE (X2) line card for 4900M series
                      (this is the expansion module - there are two slots
                      in each chassis)
=================   =======================================================

HIPSR Servers
-------------

Todo

Sync Pulse Distribution
-----------------------

Todo

Clock Distribution System
-------------------------

Todo