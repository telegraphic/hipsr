.. HIPSR documentation master file, created by

HIPSR User's Guide
==================

This User Guide gives an overview of the HIPSR system. HIPSR is the next-generation 
signal processor for the multibeam receiver. If you're reading this, you probably want
to know how to use it.

If you're in a hurry, skip down to `Observing with HIPSR`_. Otherwise, continue reading
for an introduction to the HIPSR system.

.. note::

    If you're not familiar with the Parkes 64 m telecsope, you should have a read of
    the `telescope user guide`_.
    
    
Introduction
------------

HIPSR is a new reconfigurable digital backend for the Parkes multibeam receiver. HIPSR is capable of running many different firmware modes, so can be used for both high resolution, wide bandwidth spectral line observations, and high time resolution pulsar observations.

As of writing, there are two main modes of operations supported:

1) **HISPEC** 8192 channel, 400 MHz bandwidth spectrometer for HI observations.
2) **BPSR**   high time resolution pulsar modes, used in the HTRU survey.

The documentation here focuses on HISPEC; please head over to [??] for documentation
on the pulsar modes.

Hardware
---------

For an in-depth overview of the HIPSR hardware, head over to the 
the :ref:`hardware-chapter` chapter. To give a quick overview, HIPSR consists of:

* 13x dual-input CASPER iADC digitizer cards, 
* 13x CASPER ROACH FPGA digital processing boards for "low-level" signal processing
* A Cisco 10GbE switch for data interconnect 
* A CPU/GPU cluster for "high-level" DSP and data storage. 

These are located in racks R, S, and T. All of the signal processing nodes in HIPSR
are connected with Ethernet; the network architecture is shown in the figure below:

.. figure:: HIPSR_arch.png
    :width: 600px
    :alt: HIPSR Architecture
    :align: center
    
    *Network architecture for HIPSR.*

.. note::

    The GPU servers are mainly used for pulsar work. All of the signal processing for HISPEC 
    (HI spectrometer) is currently done on the CASPER ROACH boards. Future (lower bandwidth)
    modes of observation will likely use the GPU servers too.

Software
--------

If you *really* want to know
what's going on, the module listing and API can be found here: :ref:`software-chapter`.
A quick run-through is shown below.

hipsr-server.py
~~~~~~~~~~~~~~~

For HISPEC, all of the signal processing is done on the ROACH boards. The ROACH boards are
controlled by a script, *hipsr-server.py*, which collects data from the ROACH boards and 
metadata (e.g. pointing info) from the telescope control system (TCS). The server script then
writes the data to HDF5 files. Note that *hipsr-server.py* does not control telescope pointing,
it only collects and collates data/metadata.

hipsr-gui.py
~~~~~~~~~~~~

Data from HISPEC can be monitored using the *hipsr-gui.py* script. This script gives shows the
bandpass from all 13 beams, and has a beam scope, waterfall plotter and total power monitor.

.. figure:: hipsr-gui.jpg
    :width: 600px
    :alt: HIPSR GUI screenshot
    :align: center
    
    *Screenshot of hipsr-gui running on Mac OSX.*

hipsr-writer.py
~~~~~~~~~~~~~~~

The *hipsr-writer.py* script converts files from HDF5 to SD-FITS. At the end of your observations, you'll want to run this as most data reduction packages don't support HDF5 yet.


.. note::
    All firmware and software for HIPSR is stored on github: https://github.com/telegraphic/hipsr.
    It is of course, already installed wherever it needs to be.

How everything fits together
----------------------------

.. figure:: hipsr-server.png
    :width: 500px
    :alt: HIPSR server software
    :align: center
    
    *What's really going on.*


The hipsr-server collects, collates and writes data to HDF files. To do this, several threads must be run in parallel. Firstly, a connection to each ROACH board is made using KATCP_, a communication 
protocol which runs over TCP/IP. Each connection runs in a separate thread. In addition to this, a 
TCP/IP server is set up to communicate with TCS, which sends ASCII command : value pairs with info
about telescope setup, observation config and pointing detiails.

Having multiple threads all attempting to write the same HDF file isn't good. So, there's a dedicated
HDF thread which has a data input queue, into which the KATCP and TCS threads append data. Finally,
so we can see what's going on, TCS and KATCP threads send a subset of data over a UDP connection to
the `hipsr-gui.py`_ script, which is generally run on a different computer. This UDP connection sends
python dictionaries converted into JSON.


Observing with HIPSR
--------------------

Starting observations
~~~~~~~~~~~~~~~~~~~~~

There are three things that must be started to observe with HIPSR:

    1) The telescope control system, TCS
    2) The hipsr-server script which runs on hipsr-srv0
    3) The hipsr-gui plotter which runs on [?]

To start TCS, get onto one of the Sun machines and type::

    > tcs

Until someone copy and paste's how to use TCS here, you'll have to consult the `telescope user guide`_.

*Before* you press "go" on TCS, you first need to start the hipsr-server script. To do so,
you need to SSH into hipsr-srv0::

    > ssh [user]@hipsr-srv0(.atnf.csiro.au)

Once you've connected, change into directory /data/hipsr/hipsr-server/::

    > cd /data/hipsr/hipsr-server/

Finally, start the server with the command::

    > ./hipsr_server.py

You can optionally pass the argument -p PXXX, where PXXX is your project ID, e.g.::

    > ./hipsr_server.py -p P641
    
This might save you a few seconds.


Stopping observations
~~~~~~~~~~~~~~~~~~~~~

To stop the server, press ctrl + C. The server will close all open files before exiting.

Getting your data
~~~~~~~~~~~~~~~~~

HIPSR data is stored on hipsr-srv0 in /data/hipsr/. 


When things go wrong
--------------------

Here's a few notes on problems you might run into with HIPSR. For anything to do with the
telescope, consult the `telescope user guide`_.

Socket errors
~~~~~~~~~~~~~

TCS seems to give a random socket error 9: bad file name the first time
it connects to the HIPSR server (hipsr-srv0). This doesn't seem to matter.

Sometimes the TCS socket (59012) is held open, and neither TCS or HIPSR will negotiate
a new TCP/IP connection. If this happens, you can check the port status by typing::

    > netstat | grep 59012

You can check whether there's another instance of hipsr_server by typing::

    > ps aux | grep hipsr_server

.. caution::
    If there's a rogue instance of hipsr-sever.py running, you may have to kill it.
    This can be done with the command::
    
        > kill [PID] 
        
    However, take care when doing this that you kill the right thing.

.. _KATCP : https://casper.berkeley.edu/wiki/KATCP
.. _`telescope user guide` : http://www.parkes.atnf.csiro.au/observing/documentation/user_guide/
    