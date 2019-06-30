## Installation

This is a command-line based tool which is written in Python.
It converts an XML export from RDMO into a
[RDA DMP Common Standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard) compliant JSON-encoded
machine-actionable DMP.

To install the tool, the following steps are required:

* Download the script
* Install Prerequisites

### Download the Script

It is sufficient to download the script `xml2madmp.py`.
No further files are needed.

### Install Prerequisites

The script uses Python 3. It has been tested with version 3.6
and 3.7.

By default, all needed libraries are installed on a regular
Python 3 installation.

## Usage

### Export the XML from RDMO

For each project, [RDMO](https://rdmorganiser.github.io) is
showing an export link which will export the project
as an XML file.

Export the project as XML using this link and save it to the file system.

### Convert into maDMP

To convert the exported XML file, enter the following command on
the command line:
```
python3 xml2madmp.py <rdmo-export.xml> <output-madmp.json>
```
