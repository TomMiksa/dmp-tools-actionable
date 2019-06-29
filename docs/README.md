## Installation

This is a command-line based tool which is written in Python.

A Jupyter Notebook is provided for improved usability.

To install the tool, the following steps are required:

* Download the repository
* Install required python libraries
* _(Optionally)_ Request an API token on RDMO
* _(Optionally)_ Register the API token in the tool

To be able to request an API token one has to be administrator of the RDMO instance. Since this is not an option for regular users of hosted instances, we are also providing a way of using this tool via the XML export from RDMO.

### Download the Repository

The tool is provided on the repository `https://github.com/helmuthb/dmp-tools-actionable`.
To download it use the link on the top right side of GitHub.

### Install Required Libraries

By executing the command `pip install -r requirements.txt` one can install all required dependencies.

## Usage

### Starting the Notebook Server

For having access to the comfortable Jupyter Notebook server, one has to run the command `jupyter notebook` while being in the folder of the tool.

### Using the API

For using the API one has to have administrator privileges on the RDMO instance.
If the instance is hosted on `https://rdmo.example.com/`, one has to visit the page `https://rdmo.example.com/admin/authtoken/token/` in order to create a new or view existing tokens.

After one has requested or copied a token, it is necessary to provide the token in the file `config.py`.

### Using the XML export

For regular users we recommend using the XML export.
Each project created in RDMO allows exporting the project as an XML file, by using the links on the right side.

