.. _user-guide-chapter:

HIPSR User's Guide
==================

This User Guide gives an overview of the HIPSR system. HIPSR is the next-generation 
signal processor for the multibeam receiver. If you're reading this, you probably want
to know how to use it.

.. note::

    If you're not familiar with the Parkes 64 m telecsope, you should have a read of
    the `telescope user guide`_.
    
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

Checking your setup
~~~~~~~~~~~~~~~~~~~

TODO:
	
	* Cable equalization
	* PKMC
	* OPERFCC
	* Cal control

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
