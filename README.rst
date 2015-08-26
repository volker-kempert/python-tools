======
README
======

Set of command line tools bundles in a python package

License
-------

2015 (c) Volker Kempert, all rights reserved
Licensed under MIT type of open source license.

Deployment
----------

install via pip

Quickstart for development
--------------------------

Install the source as follow and build the documentation.

.. code-block:: bash


   $ virtualenv tool
   $ cd tool
   $ source bin/activate
   $ git clone <the remote repo> python-tools
   $ cd python-tools
   $ pip install -r requirement.txt
   $ pip install -r dev_requirements.txt
   $ python setup.py develop
   $ python setup.py pytest

