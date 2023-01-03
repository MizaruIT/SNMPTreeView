## 📗 Table of contents
* [📖 About the project](#about-the-project)
	* [Why?](#why)
	* [How?](#how)
* [🛠 Installation](#installation)
	* [Installation in one step](#aio-installation)
	* [Installing SNMPTreeView](#install-tool)
	* [Creation of the database](#creation-db)
	* [Quick start for the Web Interface](#web-app)
* [💻 Getting started](#getting-started)
	* [Usage](#usage)
	* [Structure of the project](#structure-project)
	* [Use example(s)](#use-examples)
* [🔭 Roadmap](#roadmap)
* [👥 Contact](#contact)
* [🤝 Contributing](#contributing)
* [🙏 Acknowledgments](#acknowledgments)

**[ATTENTION]** The script provided is for educational and informational purposes only, I am not responsible of any actions that you could take with it.

## 📖 About the project <a name="about-the-project"/>
**Why?** <a name="why"/>

SNMP (aka Simple Network Management Protocol) is used as a way to monitor devices on a network (routers, switches, printers, etc.). 

During a pentest it can be useful to request the SNMP ports to get information about the host such as Network Interfaces (IPv4, IPv6 addresses), credentials (usernames, passwords, etc.), server/OS version, processes, etc.

But for this, it is required to have MIB (Management Information Base) files which are written in ASN.1 (Abstract Syntax Notation One, that incomprehensible language yep). Each MIB file contains at least one OID (Object Identifier) allowing to get information about the device requested (when parsing its infos).

Thus to ensure to understand the device information when requesting them, a repository containing over +10k MIB files (into JSON and ASN.1 format) is available there: https://github.com/MizaruIT/MIBS

More infos on: https://book.hacktricks.xyz/network-services-pentesting/pentesting-snmp


**How?** <a name="how"/>

For now, different tools exist such as snmpwalk, but the only problem of these tools is that they request the entire OID tree, it can be really long and we can easily miss information. For this reason, SNMPTreeView allows to have a global visualization, you only have to select the (sub)trees to check, and so on.

## 🛠 Installation <a name="installation"/>
### All in one (just copy/paste) <a name="aio-installation"/>
You can copy/paste the following notes (in Linux bash), it will clone the project, auto-configure the project, and you will be ready to work with it.

```sh
## Cloning the project
git clone https://github.com/MizaruIT/SNMPTreeView;
cd SNMPTreeView;

## Installing the dependencies
pip3 install -r requirements.txt

## Create symlink to use it as snmptreeview_cli (optional)
# sudo ln -sf $(pwd)/snmptreeview_cli.py snmptreeview_cli;

# Getting the MIBs
git clone https://github.com/MizaruIT/MIBS;

# Creation of the database
python3 Utilities/database.py -p JSON-FORMAT/

# Configuring FLASK app
export FLASK_APP=snmptreeview_web.py;
export FLASK_ENV=development;
flask run;
```

Once it is done, you can jump to the section: <a href="#getting-started">Getting started</a> to start use SNMPTreeView.

### Installing the tool <a name="install-tool"/>
1. Clone the repository
```sh
git clone https://github.com/MizaruIT/SNMPTreeView;
cd SNMPTreeView;
```

2. Install the required dependencies
```sh
pip3 install -r requirements.txt
```

3. **(Optional)** To use the script from everywhere, just run the following command
```sh
sudo ln -sf $(pwd)/snmptreeview_cli.py snmptreeview_cli;
```

### Creation of the database with MIB infos <a name="creation-db"/>
1) Getting MIB files

You can retrieve MIB files from the repository: https://github.com/MizaruIT/MIBS or any others sources, then you just need to put them into a specific directory (I recommend to call it: MIB-$FORMAT, examples: MIB-JSON for MIB already parsed in a JSON format, or MIB-ASN1 for MIB in a ASN.1 format).
```sh
# From the SNMPTreeView directory
git clone https://github.com/MizaruIT/MIBS
```

For use cases, the MIB must be parsed into a JSON format, it is already done on the Github (over 12k MIB files): https://github.com/MizaruIT/MIBS.

2) **(Optional)** Convert MIB (in ASN.1) to MIB (in JSON)

*The step is optional if you already have MIB files in a JSON format (check **step 1**).*

The tool uses MIB files via the JSON format, for this reason, you must convert your MIB files into a JSON format.

Via a for loop in a python script

- You can use the tool: pysmi-master (from the repo: https://github.com/etingof/pysmi)
```sh
git clone https://github.com/etingof/pysmi;
# You can't execute it on a directory, you will need to do a for loop for each MIB file
python3 pysmi/scripts/mibdump.py --generate-mib-texts --no-python-compile --mib-source <source of your ASN.1 files> --destination-format=json --destination-directory=<destination directory> --ignore-errors <name of the ASN.1 file>
```

- Or you can use asn1tojson.py from the "Utilities" folder **(recommended way)**
```sh
python3 asn1tojson.py -p <directory of your ASN1 files> -d <directory where you want create these files>
# If you want to quit the process (via a Linux terminal): ^Z --> [1]+  Stopped --> kill %1
```

- In Linux, via a for loop in Bash
```sh
input_dir=VAR1; output_dir=VAR2; for filename in $(ls $input_dir); do echo "Parsing: $filename..." && python3 mibdump.py --generate-mib-texts --no-python-compile --mib-source "$input_dir" --destination-format=json --destination-directory="$output_dir" "$input_dir"/"$filename"; done

# Example:
input_dir=asn1-mib; output_dir=json-mib; for filename in $(ls $input_dir); do echo "Parsing: $filename..." && python3 mibdump.py --generate-mib-texts --no-python-compile --mib-source "$input_dir" --destination-format=json --destination-directory="$output_dir" "$input_dir"/"$filename"; done
```

3) Creation of the database sqlite3 (with the MIB infos)
```sh
python3 database.py -p <directory of your JSON files>
# A file 'snmp_mibs.db' will be created with all the information from the MIB into a sqlite database.
```

### (Optional) Quick start for the Web Interface <a name="web-app"/>

*This step is optional if you only want to use the CLI tool.*

The SNMPTreeView tool can be used in two ways: via CLI (command line) or via a web interface.

To create the web application, run the following commands:
```sh 
export FLASK_APP=snmptreeview_web.py;
export FLASK_ENV=development;
flask run
# You can now visit: http://127.0.0.1:5000/
```



## 💻 Getting started <a name="getting-started"/>
The script is interactive, once executed, it will be shown with a menu and you only need to select the actions to realize.

It can be used in two cases: via the command line or via the web interface.
### Usage <a name="usage"/>
**I) Command line (CLI)**
1) Launch the script 
<pre>
python3 snmptreeview_cli.py -a IP [-o OIDS] [-c COMMUNITY] [-v {0,1,3}] [-u USERNAME] [--authKey AUTHKEY] [--privKey PRIVKEY] [--authProtocol {USM_AUTH_NONE, USM_AUTH_SHA, USM_AUTH_MD5}] [--privProtocol {USM_PRIV_NONE,USM_PRIV_CBC56,USM_PRIV_CBC168_3DES,USM_PRIV_CFB128_AES,USM_PRIV_CFB192,USM_PRIV_CFB256_AES}]

# Arguments
-h, --help = Show the help message  
<b>[required]</b>                                -a ADDR, --addr ADDR = Address/IP of the target 
<b>[not required, per default=0]</b>             -o OIDS, --oids OIDS = OIDs to parse, per default it is the value 0 to start at the root 
<b>[not required, per default=public]</b>        -c COMMUNITY, --community COMMUNITY = Authentication with the community as input
<b>[not required, per default=v2c]</b>           -v {0,1,3}, --version {0,1,3} = Version of the SNMP, it can be the version 1 (with an input of 0), the v2c (input=1) and the version 3 (input=3) 
<b>[not required, per default=None]</b>          -u USERNAME, --userName USERNAME = The user name for the version 3 of the SNMP protocol
<b>[not required, per default=None]</b>          --authKey AUTHKEY = The key of the authentication protocol
<b>[not required, per default=None]</b>          --privKey PRIVKEY = The key of the privacy protocol
<b>[not required, per default=USM_AUTH_NONE]</b> --authprotocol {USM_AUTH_NONE,USM_AUTH_SHA,USM_AUTH_MD5} = The type of the authentication protocol
<b>[not required, per default=USM_PRIV_NONE]</b> --privProtocol {USM_PRIV_NONE,USM_PRIV_CBC56_DES,USM_PRIV_CBC168_3DES,USM_PRIV_CFB128_AES,USM_PRIV_CFB192_AES,USM_PRIV_CFB256_AES} = The type of the privacy protocol
</pre>

An example: 
```sh
$ python3 snmptreeview_cli.py -a 127.0.0.1

--------------------------------------
Welcome to the SNMPTreeView Tool
--------------------------------------

LIST OF THE OIDs (aka BRANCHES)
┌────────┬───────────┬────────────────────┬─────────┬───────┬─────────────┬────────────┬─────────┬─────────────┐
│ Choice │ OID       │ File name          │ Name    │ Value │ Description │ maxacccess │ indices │ Type        │
├────────┼───────────┼────────────────────┼─────────┼───────┼─────────────┼────────────┼─────────┼─────────────┤
│ 0      │ 1.3.6.1.2 │ SNMPv2-SMI-v1.json │ mgmt    │ None  │ None        │ None       │ None    │ OctetString │
├────────┼───────────┼────────────────────┼─────────┼───────┼─────────────┼────────────┼─────────┼─────────────┤
│ 1      │ 1.3.6.1.4 │ SNMPv2-SMI-v1.json │ private │ None  │ None        │ None       │ None    │ Integer     │
├────────┼───────────┼────────────────────┼─────────┼───────┼─────────────┼────────────┼─────────┼─────────────┤
│ 2      │ 1.3.6.1.6 │ SNMPv2-SMI-v1.json │ snmpV2  │ None  │ None        │ None       │ None    │ Integer     │
└────────┴───────────┴────────────────────┴─────────┴───────┴─────────────┴────────────┴─────────┴─────────────┘
Which OID (aka branch) do you want to check the sub-OIDs (aka subtrees)?
Choice = 2

LIST OF THE OIDs (aka BRANCHES)
┌────────┬────────────────┬──────────────────────────────┬──────────────────┬───────┬──────────────────────────────────────────┬────────────┬─────────┬─────────────┐
│ Choice │ OID            │ File name                    │ Name             │ Value │ Description                              │ maxacccess │ indices │ Type        │
├────────┼────────────────┼──────────────────────────────┼──────────────────┼───────┼──────────────────────────────────────────┼────────────┼─────────┼─────────────┤
│ 0      │ 1.3.6.1.6.3.1  │ SNMP-STORAGE-MIB.json        │ snmpStorageMIB   │ None  │ This MIB modules provides objects that   │ None       │ None    │ Integer     │
│        │                │                              │                  │       │ allow management applications to commit  │            │         │             │
│        │                │                              │                  │       │ non-volatile conceptual rows to stable   │            │         │             │
│        │                │                              │                  │       │ storage.                                 │            │         │             │
├────────┼────────────────┼──────────────────────────────┼──────────────────┼───────┼──────────────────────────────────────────┼────────────┼─────────┼─────────────┤
│ 1      │ 1.3.6.1.6.3.10 │ SNMP-FRAMEWORK-MIB.json      │ snmpFrameworkMIB │ None  │ The SNMP Management Architecture MIB     │ None       │ None    │ OctetString │
│        │                │                              │                  │       │ Copyright (C) The Internet Society       │            │         │             │
│        │                │                              │                  │       │ (2002). This version of this MIB module  │            │         │             │
│        │                │                              │                  │       │ is part of RFC 3411; see the RFC itself  │            │         │             │
│        │                │                              │                  │       │ for full legal notices.                  │            │         │             │
├────────┼────────────────┼──────────────────────────────┼──────────────────┼───────┼──────────────────────────────────────────┼────────────┼─────────┼─────────────┤
│ 2      │ 1.3.6.1.6.3.11 │ SNMP-MPD-MIB.json            │ snmpMPDMIB       │ None  │ None                                     │ None       │ None    │ Counter32   │
├────────┼────────────────┼──────────────────────────────┼──────────────────┼───────┼──────────────────────────────────────────┼────────────┼─────────┼─────────────┤
│ 3      │ 1.3.6.1.6.3.12 │ SNMP-TARGET-MIB.json         │ snmpTargetMIB    │ None  │ This MIB module defines MIB objects      │ None       │ None    │ Integer     │
│        │                │                              │                  │       │ which provide mechanisms to remotely     │            │         │             │
│        │                │                              │                  │       │ configure the parameters used by an SNMP │            │         │             │
│        │                │                              │                  │       │ entity for the generation of SNMP        │            │         │             │
│        │                │                              │                  │       │ messages.                                │            │         │             │
├────────┼────────────────┼──────────────────────────────┼──────────────────┼───────┼──────────────────────────────────────────┼────────────┼─────────┼─────────────┤
│ 4      │ 1.3.6.1.6.3.15 │ SNMP-USER-BASED-SM-MIB.json  │ snmpUsmMIB       │ None  │ The management information definitions   │ None       │ None    │ Counter32   │
│        │                │                              │                  │       │ for the SNMP User-based Security Model.  │            │         │             │
├────────┼────────────────┼──────────────────────────────┼──────────────────┼───────┼──────────────────────────────────────────┼────────────┼─────────┼─────────────┤
│ 5      │ 1.3.6.1.6.3.16 │ SNMP-VIEW-BASED-ACM-MIB.json │ snmpVacmMIB      │ None  │ The management information definitions   │ None       │ None    │ OctetString │
│        │                │                              │                  │       │ for the View-based Access Control Model  │            │         │             │
│        │                │                              │                  │       │ for SNMP.                                │            │         │             │
└────────┴────────────────┴──────────────────────────────┴──────────────────┴───────┴──────────────────────────────────────────┴────────────┴─────────┴─────────────┘
Which OID (aka branch) do you want to check the sub-OIDs (aka subtrees)?
Choice = 
```
In brief, with the CLI script, you just need to choose the option among the different **"Choice" (column 1)**.


**II) Web Interface**

It is the same usage than the CLI script, it is just via a web interface accessible on 127.0.0.1:5000.

Just launch the application
```sh
python3 snmptreeview_web.py
# Go to: 127.0.0.1:5000
```

Once on the web interface, you just need to enter the parameters of your choice.

The only thing to know is: when an OID has a maxaccess with "write" permission, the row will be highlighted in a color.



### Some features

1) Feature SET VALUE
Depending on the device, multiple types of permissions are set. A device can be "read-only", "write-only", "read-write". In the last two cases, it means that you can modify the value of the OID attributes. 

The feature **"SET VALUE"** is implemented for these cases.

2) Others (TO DO)

### Structure of the project <a name="structure-project"/>
The project has the following structure:

    ├── requirements.txt      # The python dependencies required to make it works.
    ├── snmpclientclass.py    # The SNMPTreeView class with its functions.
    ├── snmptreeview_cli.py   # The SNMPTreeView tool in CLI (command line).
    ├── snmptreeview_web.py   # The SNMPTreeView tool via web interface (Flask app).
    ├── static/               # The libraries used for the web interface (for CSS, JS, etc.). It can be simplified, I used BootStrap.
    ├── templates/            # The template used for the web interface page.
    └── Utilities/            # The script utilities for parsing, creating the database, etc.
    │   ├── asn1tojson.py     # The script used to convert multipe ASN.1 MIB files from a directory into JSON format (via mibdump.py)
    │   ├── database.py       # The script used to collect the data from the JSON MIB files into a sqlite database
    │   └── mibdump.py        # The script used for parsing ASN.1 MIB file into another format


### Use example(s) <a name="use-examples"/>
The recommended way to use the script is the following:

**1) Launch it**
```sh
# Usage for SNMP version 1
$ python3 snmp_cmd_terminal.py -a 127.0.0.1 -o 1.3.6.1.2.1 -v 1 (To do the same previous request but with the version 1 instead of version v2c)
$ python3 snmp_cmd_terminal.py -a 127.0.0.1 -o 1.3.6.1.2.1 -v 1 -c private (To do the same previous request but with the community private instead of public)

# Usage for SNMP version 2c
$ python3 snmp_cmd_terminal.py -a 127.0.0.1 (To request our local IP with the community=public, version=v2c, and the first OID of your address)
$ python3 snmp_cmd_terminal.py -a 127.0.0.1 -o 1.3.6.1.2.1 (To request our local IP=127.0.0.1 with the community public, version=v2c, and to check the OIDs at 1.3.6.1.2.x with x starting from 0)

# Usage for SNMP version 3
- python3 snmp_cmd_terminal.py -a 127.0.0.1 -v3 -u user1 (To request our local IP with the community=public, version=3, the first OID of your address and the userName=user1)
- python3 snmp_cmd_terminal.py -a 127.0.0.1 -v3 -u user1 --authKey hi --authProtocol USM_AUTH_SHA (To request our local IP with the community=public, version=3, the first OID of your address, the userName=user1, the key of the authentication protocol=hi, and the authentication protocol=SHA)
- python3 snmp_cmd_terminal.py -a 127.0.0.1 -v3 -u user1 --privKey hihi --privProtocol USM_PRIV_CFB256_AES (To request our local IP with the community=public, version=3, the first OID of your address, the userName=user1, the key of the privacy protocol=hihi, and the privacy protocol=USM_PRIV_CFB256_AES)
- python3 snmp_cmd_terminal.py -a 127.0.0.1 -v3 -u user1 --privKey hihi --privProtocol USM_PRIV_CFB256_AES --authKey hi --authProtocol USM_AUTH_SHA (To request our local IP with the community=public, version=3, the first OID of your address, the userName=user1, the key of the authentication protocol=hi, and the authentication protocol=SHA, the key of the privacy protocol=hihi, the privacy protocol=CFB256 AES)
```


  ## 🔭 ROADMAP <a name="roadmap"/>
- [x] Add a CLI feature
- [x] Add an interface feature 
	- [ ] Improve the interface? I did it when I was bad at html, i improved a bit since, it currently sucks
	- [ ] Add the usage of the SNMPv3 on the web interface (it is implemented, but not checked)
- [x] Add the utilisation with the different versions (SNMPv1, SNMPv2, SNMPv3)
  - [x] SNMPv1
  - [x] SNMPv2
  - [ ] SNMPv3: to improve (not checked)
- [ ] Add a grepping features (especially for attributes: description, name, maxaccess, indices)
- [ ] Add a grepping features for OID(s) with maxaccess having write rights, retrieve all the list from an IP. 
- [ ] Add a setting values combine with a revert (when has rights to modify value) features


## 👥 Contact <a name="contact"/>
- Twitter: @MizaruIT (https://twitter.com/MizaruIT)
- GitHub: @MizaruIT (https://github.com/MizaruIT)
- Project Link: https://github.com/MizaruIT/SNMPTreeView

## 🤝 Contributing <a name="contributing"/>
Contributions, issues, and feature requests are welcome!

Feel free to send me messages to add new features (such as new vulnerabilities, new scan, etc.)

## 🙏 Acknowledgments <a name="acknowledgments"/>
Thanks to the repos filled with thousand of MIBs files.