
# Component Installer for deploying PySSA
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://GitHub.com/urban233/ComponentInstaller/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/urban233/ComponentInstaller)](https://GitHub.com/urban233/ComponentInstaller/issues/)
[![GitHub contributors](https://img.shields.io/github/contributors/urban233/ComponentInstaller.svg)](https://GitHub.com/urban233/ComponentInstaller/graphs/contributors/)
[![GitHub release](https://img.shields.io/github/v/release/urban233/ComponentInstaller)](https://github.com/urban233/ComponentInstaller/releases/)

## Contents of this document
* [Description](#Description)
* [Contents of this repository](#Contents-of-this-repository)
    * [Sources](#Sources)
    * [Documentation](#Documentation)
    * [Assets](#Assets)
* [Build](#Build)
    * [Windows](#Windows)
    * [Source code](#Source-code)
* [Dependencies](#Dependencies)
* [Citation](#Citation)
* [References and useful links](#References-and-useful-links)
* [Acknowledgements](#Acknowledgements)

## Description
The Component Installer is a software tool designed for use as a component-based installer. 
It is capable of addressing a range of deployment contexts that typically necessitate more 
intricate configuration than is typically required in other scenarios. 
The PySSA Installer serves as a case study demonstrating 
the potential utility of the component-based installation methodology.


## Contents of this repository
### Sources
The repository comprises four distinct source code units.

- _src/main/java_
    - The package contains the communicator class, which is utilized for communication with WindowsTasks.exe.
- _src/main/kotlin_
    - The package contains the main source code, including gui and model.
- _WindowsWrapper/WindowsCmdElevator_
    - The package contains the class to elevate a normal cmd shell with admin privileges.
- _WindowsWrapper/WindowsTasks_
    - The package contains the communicator, which facilitates communication with the Kotlin application, as well as a number of useful classes for the management of the MS Windows operating system.

### Documentation
The <a href="https://github.com/urban233/ComponentInstaller/tree/main/deployment">"deployment"</a> folder 
contains a user guide as PDF file.
This [PDF file](https://github.com/urban233/ComponentInstaller/blob/v1.0.1/deployment/inno_setup/PySSA-Component-Installer-User-Guide.pdf) is also available through the help menu item within the PySSA Component Installer. 
The user guide explains the installation and uninstallation of every component 
as well as the update procedure for ColabFold and PySSA. Furthermore,
it contains a troubleshooting section for WSL2 and ColabFold.

### Assets
The <a href="https://github.com/urban233/ComponentInstaller/tree/main/src/main/resources/assets">"assets"</a> folder contains 
all logos including the WSL2, ColabFold and PySSA logo, as well as the PySSA Component Installer logo.
If you are using PySSA Component Installer for your own projects, you are welcome to give credit to PySSA Component Installer by using the logo in your presentations, etc.

## Build
The Component Installer consists of a Kotlin/Java project and a C# solution with two projects.

### Windows
To deploy the installer on a Microsoft Windows OS (10 or 11), use the provided 
inno setup script as a starting point. 
Be aware that the inno setup compiler needs to be pre-installed!

### Source code
The Kotlin/Java project is a Gradle project. 
In order to use the source code for your own software or do your own Component Installer build, 
download or clone the repository and open it in a Gradle-supporting IDE (e.g. IntelliJ) 
as a Gradle project and execute the build.gradle file. 
Gradle will then take care of installing all dependencies. 
A Java Development Kit (JDK) of version 17 must also be pre-installed and 
set as project JDK / project compiler.

The C# solution contains the C# project WindowsCmdElevator and WindowsTasks. Both can be compiled to 
an .exe file using the provided FolderProfile.pubxml files.

## Dependencies
**Needs to be pre-installed:**
* Java Development Kit (JDK) version 17
  * [Adoptium Open JDK](https://adoptium.net/temurin/archive/?version=17) (as one possible source of the JDK)
* .NET 8.0
  * [Microsoft .NET 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

**Managed by Gradle:**
* Java Native Access (JNA) version 5.8.0
  * [Java Native Access GitHub repository](https://github.com/java-native-access)
  * [LGPL, version 2.1 or later, or (from version 4.0 onward) the Apache License, version 2.0](https://github.com/java-native-access/jna?tab=License-1-ov-file)
* JeroMQ version 0.6.0
  * [JeroMQ GitHub repository](https://github.com/zeromq/jeromq)
  * Mozilla Public License Version 2.0

**Managed by NuGet:**
* NLog version 5.3.2
  * [NLog GitHub repository](https://github.com/NLog/NLog)
  * BSD-3-Clause license
* NetMQ version 4.0.1.13
  * [NetMQ GitHub repository](https://github.com/zeromq/netmq/)
  * GNU Lesser General Public License 3

## Citation
You can cite this software or this repository as it is defined in the CITATION.cff file.

## References and useful links
**Windows Subsystem for Linux**
* [What is the Windows Subsystem for Linux? (Article)](https://learn.microsoft.com/en-us/windows/wsl/about)
* [How to install Linux on Windows with WSL (Article)](https://learn.microsoft.com/en-us/windows/wsl/install)

**ZeroMQ**
* [ZeroMQ Homepage](https://zeromq.org/)
  * [Java implementation (JeroMQ)](https://github.com/zeromq/jeromq)
  * [C# implementation (NetMQ)](https://github.com/zeromq/netmq/)

## Acknowledgements
**Developers:**
* Martin Urban
* Hannah Kullik

**End-user testers:**
* Jonas Schaub
* Achim Zielesny

**Logo:**
* Martin Urban
* Hannah Kullik

**Initialization, conceptualization, and supervision:**
* Achim Zielesny and Angelika Loidl-Stahlhofen

**The ComponentInstaller project team would like to thank
the communities behind the open software libraries for their amazing work.**

<!--
**ComponentInstaller was developed at:**
<br>
<br>Zielesny Research Group
<br>Westphalian University of Applied Sciences
<br>August-Schmidt-Ring 10
<br>D-45665 Recklinghausen Germany
--!>
