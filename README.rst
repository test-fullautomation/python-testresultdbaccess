TestResultDBAccess
==================

Table of Contents
-----------------

-  `Getting Started <#getting-started>`__

   -  `How to install <#how-to-install>`__
-  `Contribution <#contribution>`__
-  `Package Documentation <#package-documentation>`__
-  `Feedback <#feedback>`__
-  `About <#about>`__

   -  `Maintainers <#maintainers>`__
   -  `Contributors <#contributors>`__
   -  `License <#license>`__

Getting Started
---------------

The **TestResultDBAccess** package offers a flexible and efficient way to 
interact with the database of a test result web application. 

Users can choose between **Direct Access** and **REST API Access**, depending on 
their specific needs and preferences.

How to install
~~~~~~~~~~~~~~

**TestResultDBAccess** can be installed in two different ways.

1. Installation via PyPi (recommended for users)

   .. code::

      pip install python-testresultdbaccess

   `TestResultDBAccess in PyPi <https://pypi.org/project/python-testresultdbaccess/>`_

2. Installation via GitHub (recommended for developers)

   * Clone the **python-testresultdbaccess** repository to your machine.

     .. code::

        git clone https://github.com/test-fullautomation/python-testresultdbaccess.git

     `TestResultDBAccess in GitHub <https://github.com/test-fullautomation/python-testresultdbaccess>`_

   * Install dependencies

     **Notes:** Regarding the Linux environment (such as **Ubuntu**), there are Linux dependency 
     packages that need to be installed before installing Python dependency libraries. 
     Use the following commands to install them:

     .. code::

         chmod +x ./requirements_linux.sh
         ./requirements_linux.sh

     **TestResultDBAccess** requires some additional Python libraries. Before you install the cloned repository sources
     you have to install the dependencies manually. The names of all related packages you can find in the file ``requirements.txt``
     in the repository root folder. Use pip to install them:

     .. code::

        pip install -r ./requirements.txt

     Additionally install **LaTeX** (recommended: TeX Live). This is used to render the documentation.

   * Configure dependencies

     The installation of **TestResultDBAccess** includes to generate the documentation in PDF format. This is done by
     an application called **GenPackageDoc**, that is part of the installation dependencies (see ``requirements.txt``).

     **GenPackageDoc** uses **LaTeX** to generate the documentation in PDF format. Therefore **GenPackageDoc** needs to know where to find
     **LaTeX**. This is defined in the **GenPackageDoc** configuration file

     .. code::

        packagedoc\packagedoc_config.json

     Before you start the installation you have to introduce the following environment variable, that is used in ``packagedoc_config.json``:

     - ``GENDOC_LATEXPATH`` : path to ``pdflatex`` executable

   * Use the following command to install **TestResultDBAccess**:

     .. code::

        python setup.py install

Contribution
------------
We are always searching support and you are cordially invited to help to improve
**TestResultDBAccess** package.

Package Documentation
------------------------
A detailed documentation of the **TestResultDBAccess** can be found here:
`TestResultDBAccess tool’s Documentation`_.

Feedback
--------
Please feel free to give any feedback to us via

Email to: `Thomas Pollerspöck`_

Issue tracking: `TestResultDBAccess Issues`_

About
-----

Maintainers
~~~~~~~~~~~
`Thomas Pollerspöck`_

`Tran Duy Ngoan`_

Contributors
~~~~~~~~~~~~

`Thomas Pollerspöck`_

`Tran Duy Ngoan`_

License
~~~~~~~

Copyright 2020-2023 Robert Bosch GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    |License: Apache v2|

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


.. |License: Apache v2| image:: https://img.shields.io/pypi/l/robotframework.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html
.. _TestResultDBAccess: https://github.com/test-fullautomation/python-testresultdbaccess
.. _TestResultWebApp: https://github.com/test-fullautomation/TestResultWebApp
.. _Thomas Pollerspöck: mailto:Thomas.Pollerspoeck@de.bosch.com
.. _Tran Duy Ngoan: mailto:Ngoan.TranDuy@vn.bosch.com
.. _TestResultDBAccess tool’s Documentation: https://github.com/test-fullautomation/python-testresultdbaccess/blob/develop/TestResultDBAccess/TestResultDBAccess.pdf
.. _TestResultDBAccess Issues: https://github.com/test-fullautomation/python-testresultdbaccess/issues
