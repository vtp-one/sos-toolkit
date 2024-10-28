# sos-toolkit

Develop, package, and distribute local Digital Intelligence.

SOS stands for System of Systems, and the goal of SOS-Toolkit is to provide the tools needed to create and use Digital Intelligence Systems.

 - Simple Description: Better makefiles with Python
 - Functional Description: Wrapper for git, docker, or any other Python module to manage backend services and runtime configuration
 - Ambitious Description: Dynamically modifiable glue code for polymorphic digital intelligence


# Current Release Target
```
v0.0.1
```


# The Local Problem
The next generation of digital intelligence systems requires multiple layers of independent machine learning based components. 
Each of these requires it's own specialized dependency enviornment and runtime configuration in order to work correctly with each other. 
No currently available tools exist that are able to develop, package, and distribute these kinds of systems in a way that is easily accessible.

SOS-Toolkit solves these problems by allowing developers to package processes that generate the required enviornment and configuration by using a YAML-based interface to Python modules and local services.


# Project Status
SOS-Toolkit is currently a proof-of-concept. Usage is only intended for development and testing.
 - It is incomplete, insecure, and has the capability to delete your entire system if used incorrectly
 - The CLI text output is excessively verbose and includes as much internal information as possible for debugging
 - Useful output information such as runtime system state is mixed with development information

If these directions are not detailed enough for you, the project is too early for you to get much use from. 
Even if you can’t use it yet, we welcome any comments you have about what we are doing.
Take a look at the higher level project information, and let us know what we need to add to make something that works for you.

 - [Project Overview](docs/01_project/01_overview.md)
 - [Project Goals](docs/01_project/02_goals.md)
 - [Related Projects](docs/01_project/03_related_projects.md)


# Requirements
### 1. Hardware
Currently only the NVIDIA Jetson AGX Orin 64GB Development Kit is supported. 
The end-goal is to be as hardware neutral as possible, but the current focus is core functionality.
Development is being done using this hardware and the default target will be the Jetson platform for early versions.

[FAQ: Why Jetson?](docs/01_project/06_FAQ.md)

### 2. Operating System
Running on the Jetson AGX Orin: the target OS is L4T 36.3 - Jetpack 6.0. 

Refer to the relevant documentation for flashing and setting up your system: [NVIDIA Documentation](https://developer.nvidia.com/embedded/learn/getting-started-jetson#documentation)

This includes the following packages, some of which you may need to install:
 - Python 3.10 / python-venv
 - Docker / NVIDIA Docker / Docker Compose / Docker Buildx
 - git

Refer to relevant documentation to make sure they are installed correctly.

Simple tests:
```
$ python --version
Python 3.10.XX

$ python -m venv --help
usage: venv [-h] ...

$ docker --version
Docker version XX.X.X

$ docker compose version
Docker Compose version vX.XX.X

$ docker buildx version
github.com/docker/buildx vX.XX.X

$ git --version
git version X.XX.X

```

### 3. User Interface
Current usage is a command line interface only. 
You will need access to a terminal via either a local monitor, SSH, or any other method you prefer.

Running SOS-Toolkit inside of a docker container is not currently supported due to requiring access to the docker binary executables.


# Installation
There are no packages available and it is designed to be run from an isolated python virtual environment as an editable package from the git repository.

### 1. Setup a Root Directory.

Installing systems with models can require a large amount of storage (10-100GB+), you will want to make sure you are using a sufficient sized partition outside of the Orin system partition. 

This will require installing additional storage space and partitioning to utilize it: [NVIDIA Documentation](https://developer.nvidia.com/embedded/learn/getting-started-jetson#documentation)

Once you have a working partition, you can create a directory in it which will act as the root directory for both SOS-Toolkit and installed systems. 
For the purpose of documentation, this will be referenced as: `/sos` - but your specific directory can be different. 
```
$ mkdir sos
$ cd sos
```

A useful method is to setup a bind mount to a directory on the storage partition: be sure to read the documentation for bind mounts and `/etc/fstab` before using this method.

Example /etc/fstab entry for a bind mount:
```
/path/to/your/partition/folder /sos none bind 0 0
```

After adding the entry, you can then run a command to activate the mount.
```
$ sudo mkdir /sos
$ sudo mount /sos
$ cd /sos
```


### 2. Clone the SOS-Toolkit Repository
This repository will be installed as an editable package in a python virtual environment. 
The purpose of this is to facilitate the usage of git tags/branches to allow for different versions of SOS-Toolkit to be run as needed. 
The SOS-Toolkit main branch will contain the current release distribution, but is intended for development.
Specific version tags will allow for predictable functionality even as breaking changes are introduced. 
A system built to operate with SOS-Toolkit v0.0.1 should always work by changing the tag your local repository is currently referencing.
```
$ git clone https://github.com/vtp-one/sos-toolkit.git
$ cd sos-toolkit
$ git checkout v0.0.1
```
Future versions of SOS-Toolkit will handle different versions automatically and this will include handling potential dependency issues as well.


### 3. Setup A Virtual Environment
This step creates a virtual environment to run SOS-Toolkit from, activates the environment, and installs the SOS-Toolkit repository as an editable python package.

The location of this virtual environment is not required to be in the repository itself, but it makes things simpler.
Setup and installation beyond that is left up to your own preferences. 
Anytime you want to use SOS-Toolkit, you will be activating this virtual environment first. 

Any command prefaced with `(sos)` is expected to be run from inside a working SOS-Toolkit virtual environment. When we create the venv, we provide a prompt: `sos` which is added to the terminal when the environment is activated.

```
$ cd /sos/sos-toolkit
$ python3 -m venv venv --prompt sos
$ source venv/bin/activate
(sos)$ pip install -e .
```
The pip install command will be using the current working directory as the target for the package installation, if you are using different directories, modify the command as needed to target the SOS-Toolkit source directory.


### 4. Test SOS-Toolkit
This command will allow you to see if SOS-Toolkit is installed correctly. 
```
(sos)$ sos-toolkit test
```
It should print something like this:
```
SOS_TOOLKIT CLI TEST - version: v0.0.1
```
Not seeing that message means there was something wrong with your installation.

Any additional output with that message is a bug that should be reported.


### 5. SOS-Toolkit Help
This will list the commands available from SOS-Toolkit. Not all commands are currently functional, but take a look at what's listed and you can get an idea of the functionality SOS-Toolkit aims to provide.
```
(sos)$ sos-toolkit --help
```
Calling any of the available commands along with the `--help` switch will provide information about what it does and the arguments it accepts.


### 6. Exit the Virtual Environment
```
(sos)$ deactivate
```


### 7. Upgrade SOS-Toolkit (Not Fully Implemented)
Patch Updates - 0.0.X
- Update your local git repository
```
$ cd sos/sos-toolkit
$ git checkout main
$ git pull
$ git fetch --tags --force
$ git checkout <new release target>
```

Minor Updates - 0.X.0
 - Non-Breaking: Update your local git repository
 - Breaking: Reinstall SOS-Toolkit 

Major Updates - X.0.0
 - Reinstall SOS-Toolkit


# Basic Example - SOS-Test_System
SOS-Toolkit is intended to be used with SOS Systems.

Check out [SOS-Test_System](https://github.com/vtp-one/sos-test_system) to see it in action.


# SOS-Systems
SOS-Test_System is exactly what it's name describes: a Test System. 
It doesn't do much besides test SOS-Toolkit works.

There are a few other systems implemented that are more functional and allow you to get an idea of what SOS-Toolkit is capable of.


## [sos-test_system](https://github.com/vtp-one/sos-test_system)

An SOS-System for testing SOS-Toolkit.


## [sos-nano_llm](https://github.com/vtp-one/sos-nano_llm)

Optimized local inference for LLMs with HuggingFace-like APIs for quantization, vision/language models, multimodal agents, speech, vector DB, and RAG.

[dusty-nv/NanoLLM](https://github.com/dusty-nv/NanoLLM)


## [sos-ollama_webui](https://github.com/vtp-one/sos-ollama_webui)

Ollama Open WebUI is an extensible, feature-rich, and user-friendly self-hosted WebUI designed to operate entirely offline. 
It supports various LLM runners, including Ollama and OpenAI-compatible APIs. 
For more information, be sure to check out the Open WebUI Documentation.

[open-webui](https://github.com/open-webui/open-webui)


## [sos-invokeai](https://github.com/vtp-one/sos-invokeai)

Invoke is a leading creative engine built to empower professionals and enthusiasts alike. 
Generate and create stunning visual media using the latest AI-driven technologies. Invoke offers an industry leading web-based UI, and serves as the foundation for multiple commercial products.

[InvokeAI](https://github.com/invoke-ai/InvokeAI)


## [sos-comfyui](https://github.com/vtp-one/sos-comfyui)

ComfyUI is the most powerful and modular stable diffusion GUI and backend.

[ComfyUI](https://github.com/comfyanonymous/ComfyUI)


## [vtp-synthesis](https://github.com/vtp-one/vtp-synthesis)

Synthesis is an LLM interface for function calling. 
Use Digital Intelligence to Synthesize Digital Intelligence.


# More Information
 - [Frequently Asked Questions](docs/01_project/06_FAQ.md)
 - [Introduction Documentation](docs/02_introduction)
 - [Intermediate Documentation](docs/03_intermediate)
 - [Advanced Documentation](docs/04_advanced)
 - [Technical Documentation](docs/05_technical)
 - [Reference Documentation](docs/06_reference)
 - [Project Roadmap](docs/01_project/04_roadmap.md)
 - [Open Problems](docs/01_project/05_open_problems.md)
 - [Current Bugs]
 - [Feature Requests]
 - [Your Comments Here]


# License
LICENSE WILL CHANGE

The intent is to use a full Open Source license, not a restrictive SaaS license. 

The reason for the current licensing is due to the bundling of components such as large-language models, diffusion models, and miscellaneous data sources being an uncertain area. 

All bundled component licenses are the responsibility of the end-user and the reason for the current restrictive license.

If you are concerned about licensing, let us know what you think we should be using and why.

CURRENT LICENSE: VTP-LICENSE-v0.0.1

FOR APPROVED USE: POLYFORM - STRICT
