## SOS-Context
The first step in using a System is to generate an `SOSContext` object. 
Generating this context object is done using the command: 
```
(sos)$ sos-toolkit setup 
```
The generated object is stored as an `sos-context.yaml` file, which contains the translation of the internal SOSContext python object into YAML. 
This is done by first dumping the SOSContext python object to a python dictionary then outputting the dictionary to YAML. 
Once an `sos-context.yaml` file exists, the Toolkit will use it for further commands. 
Most commands require an `sos-context.yaml` file in the current working directory to function. 

If an `sos-context.yaml` object exists in the current working directory, the default is to not overwrite it. 
You can force the setup command to overwrite the file using the --overwrite switch.
```
(sos)$ sos-toolkit setup --overwrite
```

When running a command that requires an SOSContext: 
 - the context is loaded from the `sos-context.yaml` file
 - whatever actions defined for that command in the file are run in order
 - the resulting context is then output back to the `sos-context.yaml` file. 

Runtime actions can modify the SOSContext and subsequent commands use the updated data.


### Generation
Context generation is done through three primary operations: merging objects, service parsing, and OmegaConf resolve. 

Besides the `sos-system.yaml` file, the generation uses additional files: 
 - `sos-root.yaml`: a configuration file located in the sos-toolkit source tree that contains SOS-Toolkit global values
 - `sos-local.yaml`: a configuration file located in the system's runtime directory that includes system local configuration
 - `sos-user.yaml (NOT IMPLEMENTED)`: a configuration file located in a user specified location that contains user configuration
 - `runtime configuration`: a dictionary of key-value objects provided to the generation function

These different objects are all loaded and used to generate the context. 
The objects are loaded using [OmegaConf](https://omegaconf.readthedocs.io/en/2.3_branch/) and merged as OmegaConf dictionaries. 
This merge process uses the following order for precedence with the first listed being lowest precedence:
 - `sos-root.yaml`
 - `sos-user.yaml`
 - `sos-system.yaml`
 - `sos-local.yaml`
 - `runtime configuration`

What this means is that you can modify an object from an `sos-system.yaml` by re-defining it in an `sos-local.yaml` file.

Example:
```
[ sos-system.yaml ]
namespace:
  foo: bar

[ sos-local.yaml ]
namespace:
  foo: not bar

[ generated sos-context.yaml ]
namespace:
 foo: not bar
```

The next step for generation is resolving the service objects. 
This operation iterates through the defined services in the `sos-system.yaml`; any service that has a value of either True or a dictionary for configuration is included. 

Services are resolved recursively, meaning a service can include additional services. 
Currently each service will only by included once, so recursive services do not generate colliding service objects. 

Resolving a service is done by preforming the context generation process on the `sos-service.yaml` file for the defined service. 
Configuration of the service is done at this stage by including the dictionary object fron the service definition in the `sos-system.yaml` file. 
This dictionary is used by the generation process during the merge process as a runtime configuration dictionary.

After generating the SOSContext object for the service, the entire SOSContext object for the service is included in the higher-level SOSContext object being generated for the system. 
This is done so that objects (meta, namespace, actions), defined for the service can be referenced by actions defined for the system.

The final step of generation is done through OmegaConf.resolve. 
OmegaConf provides for the ability to define variables to copy objects using the syntax: `$OBJECT`. 
This can be used to copy any object from the current internal OmegaConf dictionary representation. 
For example, this can be used to link an action from a service into an action for a system.
```
service_action: $service.service_name.action.debug_action
```

This will copy the entire object from `service.service_name.action.debug_action` and replace it as the value for service_action.


### Format
The generated SOSContext object contains these objects:
 - `meta`: the meta information for the system
   - `sos_version`: The SOS-Toolkit version the system was built for
   - `sos_path`: The folder path of the SOS-Toolkit used to generate the context
   - `system_name`: The name of the system
   - `system_version`: The version of the system
   - `system_internal`: The folder path of the internal directory the system will use
   - `system_description`: The description of the system
   - `platform`: The platform the system is built for
   - `network (NOT USED)`: The network the system should use
   - `sandbox (NOT USED)`: The sandbox the system should use
   - `system_path`: The folder path for the system
   - `is_installed`: A boolean flag for whether the system has been installed and is runnable
   - `input_method (NOT USED)`: The default input method the system has been built to use
   - `local_file`: The file path for the sos-local.yaml file that was used for generating the context
   - `user_file`: The file path for the sos-user.yaml file that was used for generating the context
   - `system_file`: The file path for the sos-system.yaml file that was used for generating the context
   - `root_file`: The file path for the sos-root.yaml file that was used for generating the context
   - `context_file`: The file path for the sos-context.yaml file that is used for the context

 - `namespace`: the internal namespace for the system
 - `service`: the generated service objects for the system
 - `action` (TO BE SPLIT: command / action): the actions defined for the system
 - `hook`: the hook objects defined for the system


### Usage
After generating a context using the `sos-toolkit setup` command, the `sos-context.yaml` file will be loaded by SOS-Toolkit for commands. 
It is possible to manually edit the file, but this can cause serious problems including deleting your entire file-system. 
It can be viewed and edited in a text editor, but the recommended methods are to use SOS-Toolkit commands to interact with it. 

The first command is:
```
(sos)$ sos-toolkit context
```

Entering this command will print the entire context object to the terminal. It is possible to specify a target object for the command to return:
```
(sos)$ sos-toolkit context --target=namespace
```
This will allow you to only return the object you want to see, and the objects are index-able using dot-notation:

```
(sos)$ sos-toolkit context --target=namespace.foo.bar
```

You must include the SOSContext object identifier: `meta`, `namespace`, `service`, `action`, or `hook`.

It's possible to set the value of objects. 
This currently only supports string values, and you can completely break a context by targeting the wrong key or supplying the wrong value.

This is done using the `--value` switch for the command.
```
(sos)$ sos-toolkit context --target=namespace.foo.bar.baz --value=foobar
```

This will set the targeted context object to the provided value.

### Interactive CLI
For more in depth editing of a context object, it is possible to operate on the object directly from an ipython interpreter. This is done using the command: `sos-toolkit cli`
```
(sos)$ sos-toolkit cli
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [1]: 
```
The shell is a standard ipython interface, and is exited using the command: `exit`

```
In [1]: exit
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI EXIT      *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*

```
Any changes made to the context will be saved, and you can break a context by doing this. 

It is possible to disable context saving by running the command with the `--no-save-on-exit` flag.
```
(sos)$ sos-toolkit cli --no-save-on-exit
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: False *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [1]: 

```
If you call exit now:
```
In [1]: exit
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI EXIT      *SOS*
*SOS*   ON EXIT SAVE __CTX__: False *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
```
Preforming actions without saving the context can also break systems if the actions make changes to the context that the system requires.


While in the shell, the context object can be interacted with via the object: `__CTX__`

For example, you can print the entire context by using the print method:
```
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [1]: __CTX__.print()

[CONTEXT PRINT OUTPUT]

```

To set a value in the context use the set method with the corresponding dot-notation:
```
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [1]: __CTX__.set("namespace.foo.bar.baz", "foobar")
```


To get a value from the context use the get method with the corresponding dot-notation:

```
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [2]: __CTX__.get("namespace.foo.bar.baz")
Out[2]: "foobar"

```

Using this interface you can interact with more complex objects besides strings.

You can also run action objects from this interface by using the run method.
```
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [1]: __CTX__.run("action.sos_debug")

[ SOS_DEBUG RUN OUTPUT ]
```

This can target any runnable object in the context including sub-actions using dot-notation:
```
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
*SOS*                               *SOS*
*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*
*SOS*    CURRENT CONTEXT: __CTX__   *SOS*
*SOS*   TO EXIT CONSOLE USE: exit   *SOS*
*SOS*   ON EXIT SAVE __CTX__: True  *SOS*
*SOS*                               *SOS*
*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*
In [1]: __CTX__.run("action.sos_debug.test_debug.foo.bar")

[ SOS_DEBUG.FOO.BAR RUN OUTPUT ]
```
