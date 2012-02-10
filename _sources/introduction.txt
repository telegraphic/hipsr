.. HIPSR documentation master file, created by

Introduction
============

HIPSR documentation.

.. sourcecode:: python

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  Select KATCP port. Default is 7147
      -i HOSTIP, --hostip=HOSTIP
                            change host IP address to run server. Default is
                            localhost (127.0.0.1)
      -P HOSTPORT, --hostport=HOSTPORT
                            change host port for server. Default is 8080
.. sourcecode:: ipython

    In [69]: lines = plot([1,2,3])

    In [70]: setp(lines)
      alpha: float
      animated: [True | False]
      antialiased or aa: [True | False]
      ...snip

.. math::

  W^{3\beta}_{\delta_1 \rho_1 \sigma_2} \approx U^{3\beta}_{\delta_1 \rho_1}
  
  
.. plot::

   import matplotlib.pyplot as plt
   import numpy as np
   x = np.random.randn(1000)
   plt.hist( x, 20)
   plt.grid()
   plt.title(r'Normal: $\mu=%.2f, \sigma=%.2f$'%(x.mean(), x.std()))
   plt.show()
