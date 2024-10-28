## SOS-System
An SOS System is a git repository that contains an `sos-system.yaml` file. 
This file defines what the system is and what the system does. 
It acts as a manifest file that defines the system's meta information and the way it functions with the SOS-Toolkit. 
It is structured as a YAML file and contains root objects that are parsed by SOS-Toolkit when it generates an `SOSContext` object using the setup command. 

These root objects are:

### Meta
Various meta information for the system. 
Currently the sub-objects are:
 - `sos_version`: The SOS-Toolkit version the system is built to utilize
 - `system_name`: The name to identify the system
 - `system_version`: The version identifier for the system
 - `system_description`: The description of the system
 - `system_internal`: The sub-directory the system will use for an internal root directory

### Namespace
Dynamic namespace the system uses for storing initial configuration values and generated data from actions. 
The initial configuration is loaded during the generation of the SOSContext object.
Information stored in the namespace is able to persist across invocations of SOS-Toolkit commands. 

### Services
The SOS-Toolkit services that the system uses. 
These objects are referenced by the service name and the simplest form gives them a value of `True` if they are used by the system. 
These objects can also include configuration settings for the service that is merged into the loaded service. 
Services are special types of SOS-Systems, and they are defined in their own YAML file: `sos-service.yaml`. 
These files are located in the SOS-Toolkit source tree in the service folder.
On loading a service, this file is parsed to generate an SOSContext object for the service and that object is included in the generated SOSContext for the system.

### Action (to be split: command - action)
The primary purpose of a system is to define a series of actions that SOS-Toolkit runs. 
These are listed under the object "action"; but this naming has caused confusion, and will be split into "command" and "action". 
Currently, the actions are utilized in two ways: first, they map directly to commands called from the SOS-Toolkit command line interface. 
Calling `sos-toolkit install`, will take the object: `context.action.sos_install`; and run any actions listed. 
The second possibility is for these actions to have arbitrary names not connected directly to SOS-Toolkit commands. 
These actions can then be used by other actions or can be directly run from the command line using: `sos-toolkit action`. 
The second usage is the reason for the refactoring to split the commands and actions. 
Commands will be specific keywords that are only usable via the SOS-Toolkit interface, actions will be any developer-defined objects.

### Hooks
A system can define actions that function as hooks at certain points during runtime. Currently the only hooks implemented are: 
 - `on_context_load`: A hook called during loading of an sos-context.yaml file into an SOSContext object.
 - `on_context_save`: A hook that is called during saving an SOSContext object into an sos-context.yaml file.
