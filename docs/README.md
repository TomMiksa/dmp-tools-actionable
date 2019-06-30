# RDMO XML to RDA DMP Common Standard Converter

[RDMO](https://rdmorganiser.github.io/) is a very handy
tool to support the planning of data management in research projects.

The [RDA DMP Common Standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)
defines a unified interface for the exchange of DMPs between different systems,
allowing automation of steps required in a DMP.

This tool tries to bring the two together.
It allows to export the DMP created in RDMO in a JSON file,
compliant to the RDA DMP Common Standard Specification.

## Mapping of Questions to maDMP JSON fields, JSON examples

RDMO uses its own datamodel (based on _attributes_) which is aimed at being a
generic representation
of questions arising in a Data Management Plan.
In that way it is very similar to the RDA DMP Common Standard, except that
it does not define an exchange format for interoperability with other tools,
including possible automation systems.

A _questionaire_ (as for example the questionaire for _Horizon 2020_ or _FWF_ which
we have created as an addition to RDMO) is mapping questions to these attributes.

A _view_ (as for example the existing _Horizon 2020_ view which we adjusted,
and the new _FWF_ view which we have created as an addition to RDMO) is then
mapping the attributes to some output fields.

Due to this architecture, this tool is mapping the attributes to output fields in the
RDA DMP Common Standard JSON format.
The mapping of fields is fully described in [field mapping](field_mapping.md).

Some examples of the mapping:

* DMP 1 - [FWF Template](samples/fwf-gerald.pdf) (PDF)
* DMP 1 - [RDMO Export](samples/fwf-gerald.xml) (XML)
* DMP 1 - [RDA DMP Common Standard](samples/fwf-gerald.json) (JSON)
* DMP 2 - [Horizon 2020 Template](samples/h2020-gerald.pdf) (PDF)
* DMP 2 - [RDMO Export](samples/h2020-gerald.xml) (XML)
* DMP 2 - [RDA DMP Common Standard](samples/h2020-gerald.json) (JSON)
* DMP 3 - [FWF Template](samples/fwf-helmuth.pdf) (PDF)
* DMP 3 - [RDMO Export](samples/fwf-helmuth.xml) (XML)
* DMP 3 - [RDA DMP Common Standard](samples/fwf-helmuth.json) (JSON)
* DMP 4 - [Horizon 2020 Template](samples/h2020-helmuth.pdf) (PDF)
* DMP 4 - [RDMO Export](samples/h2020-helmuth.xml) (XML)
* DMP 4 - [RDA DMP Common Standard](samples/h2020-helmuth.json) (JSON)

## Installation

This is a command-line based tool which is written in Python.
It converts an XML export from RDMO into a
[RDA DMP Common Standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)
compliant JSON-encoded machine-actionable DMP.

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
