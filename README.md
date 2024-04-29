# TestResultDBAccess

## Table of Contents

-   [Getting Started](#getting-started)
    -   [How to install](#how-to-install)
-   [Contribution](#contribution)
-   [Package Documentation](#package-documentation)
-   [Feedback](#feedback)
-   [About](#about)
    -   [Maintainers](#maintainers)
    -   [Contributors](#contributors)
    -   [License](#license)

## Getting Started

The **TestResultDBAccess** package offers a flexible and efficient way
to interact with the database of a test result web application.

Users can choose between **Direct Access** and **REST API Access**,
depending on their specific needs and preferences.

### How to install

**TestResultDBAccess** can be installed in two different ways.

1.  Installation via PyPi (recommended for users)

    ``` 
    pip install python-testresultdbaccess
    ```

    [TestResultDBAccess in
    PyPi](https://pypi.org/project/python-testresultdbaccess/)

2.  Installation via GitHub (recommended for developers)

    -   Clone the **python-testresultdbaccess** repository to your
        machine.

        ``` 
        git clone https://github.com/test-fullautomation/python-testresultdbaccess.git
        ```

        [TestResultDBAccess in
        GitHub](https://github.com/test-fullautomation/python-testresultdbaccess)

    -   Install dependencies

        **TestResultDBAccess** requires some additional Python
        libraries. Before you install the cloned repository sources you
        have to install the dependencies manually. The names of all
        related packages you can find in the file `requirements.txt` in
        the repository root folder. Use pip to install them:

        ``` 
        pip install -r ./requirements.txt
        ```

        Additionally install **LaTeX** (recommended: TeX Live). This is
        used to render the documentation.

    -   Configure dependencies

        The installation of **TestResultDBAccess** includes to generate
        the documentation in PDF format. This is done by an application
        called **GenPackageDoc**, that is part of the installation
        dependencies (see `requirements.txt`).

        **GenPackageDoc** uses **LaTeX** to generate the documentation
        in PDF format. Therefore **GenPackageDoc** needs to know where
        to find **LaTeX**. This is defined in the **GenPackageDoc**
        configuration file

        ``` 
        packagedoc\packagedoc_config.json
        ```

        Before you start the installation you have to introduce the
        following environment variable, that is used in
        `packagedoc_config.json`:

        -   `GENDOC_LATEXPATH` : path to `pdflatex` executable

    -   Use the following command to install **TestResultDBAccess**:

        ``` 
        python setup.py install
        ```

## Contribution

We are always searching support and you are cordially invited to help to
improve **TestResultDBAccess** package.

## Package Documentation

A detailed documentation of the **TestResultDBAccess** can be found
here: [TestResultDBAccess tool's
Documentation](https://github.com/test-fullautomation/python-testresultdbaccess/blob/develop/TestResultDBAccess/TestResultDBAccess.pdf).

## Feedback

Please feel free to give any feedback to us via

Email to: [Thomas Pollerspöck](mailto:Thomas.Pollerspoeck@de.bosch.com)

Issue tracking: [TestResultDBAccess
Issues](https://github.com/test-fullautomation/python-testresultdbaccess/issues)

## About

### Maintainers

[Thomas Pollerspöck](mailto:Thomas.Pollerspoeck@de.bosch.com)

[Tran Duy Ngoan](mailto:Ngoan.TranDuy@vn.bosch.com)

### Contributors

[Thomas Pollerspöck](mailto:Thomas.Pollerspoeck@de.bosch.com)

[Tran Duy Ngoan](mailto:Ngoan.TranDuy@vn.bosch.com)

### License

Copyright 2020-2023 Robert Bosch GmbH

Licensed under the Apache License, Version 2.0 (the \"License\"); you
may not use this file except in compliance with the License. You may
obtain a copy of the License at

> [![License: Apache
> v2](https://img.shields.io/pypi/l/robotframework.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an \"AS IS\" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
