.. HIPSR documentation master file, created by

HIPSR User's Guide
==================

Starting HIPSR
--------------

::

    > ssh [user]@hipsr-srv0(atnf.csiro.au)
    > cd /home/pri229/hipsr/dev/
    > python hipsr_server.py

Stopping HIPSR
--------------
Press ctrl + C


Socket error
------------
TCS seems to give a random socket error 9: bad file name the first time
it connects to the HIPSR server (hipsr-srv0). This doesn't seem to matter.

Sometimes the TCS socket is held open, and neither TCS or HIPSR will negotiate
a new TCP/IP connection. You may need to wait 30 seconds until the socket clears.


    