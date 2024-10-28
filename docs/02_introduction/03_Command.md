## SOS-Command
Commands are the objects that SOS-Toolkit makes available through the command line interface. 
The commands represent important steps and functions that provide a cohesive interface to systems. 
By using standardized commands, it makes systems easier to work with.

Currently they are in an `sos-system.yaml` file in the `action` object and are prefaced with an `sos_` tag. 
As part of the first round of refactoring, these will be migrated into a separate `command` object. 
This separation will be functionally the same, but provide clearer separation between the commands and actions.

Internally the commands are python functions that are (currently) located in the action folder of the SOS-Toolkit source tree. 
Again, this will be migrated to command for clarity. 

To see the available commands, you can use the `--help` tag from the command line.
```
(sos)$ sos-toolkit --help
```
This will list all the available commands. 
Not all commands are currently implemented, but you can see the direction SOS-Toolkit is heading by the commands that we aim to provide. 

The early versions of SOS-Toolkit are intended for developers, and these commands mirror the steps that developers need to develop.

To get more information about a specific command, you can use the `--help` tag along with target command.
```
(sos)$ sos-toolkit pull --help

 Usage: sos-toolkit pull [OPTIONS] REMOTE_TARGET 
 Pull a System from a Git Repo 
╭─ Arguments ─────────────────────────────────────────────────────────────╮
│ * remote_target TEXT  Remote Git Repo to Pull [default: None] [required]│
╰─────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────╮
│ --local-target     TEXT                                  Local Folder to use or create │
│ --remote-branch    TEXT                          Remote Branch to Pull [default: main] │
│ --force   --no-force        If folder exists DELETE it before pull [default: no-force] │
│ --help                                                     Show this message and exit. │
╰────────────────────────────────────────────────────────────────────────────────────────╯

```


Most commands require an `sos-context.yaml` file in the current working directory. 
SOS-Toolkit looks up the action object of the associated command from the context. 
The associated object is (currently) defined in `context.actions` with the preface `sos_` followed by the target command name. 
```
sos-toolkit install ==> context.actions.sos_install
```


## Configuration
The first method for configuring a system is to manually edit an `sos-context.yaml` file in a text editor. 
This works, but is not recommended and can cause problems.


The second method for configuration is by creating an `sos-local.yaml` file and modifying a generated SOSContext using it. 
This usually requires generating a new context object using the setup command, but there is an `sos-toolkit update` command which can be used instead. 
Using `sos-local.yaml` requires knowing what you want to edit, and that will need documentation on the system developer's part, but most usage "should" be relatively self-explanatory. 
The system namespace will be the primary target for these changes, and depending on the system's usage of the namespace, it can provide access to modify a wide range of options.

The `sos-toolkit update` command is used to selectively modify data in an already existing SOSContext. 
It works by first loading the previous `sos-context.yaml` file. 
It generates a new SOSContext object using the SOSContext generation steps based on the modified files. 
Finally, you provide a target object to the command: only the specific target will be copied from the new context to update the value in the output context. 
Everything else from the previous context object will remain the same.

Example:
```
[ previous sos-context.yaml ]
namespace:
  foo: bar
  baz: boo

[ new sos-local.yaml ]
namespace:
  foo: bar2

[ command ]
(sos)$ sos-toolkit update namespace.foo

[ output sos-context.yaml ]
namespace:
  foo: bar2
  baz: boo

```
This can also include changes made to an `sos-system.yaml` file, or any of the other files used for generating a context object, but only the specific target object will be updated. These changes will be persisted if you create a new SOSContext.


The third method is system defined config methods and this is the recommended method. 
Config actions will function to modify the context as needed to achieve whatever configuration changes are defined by the developers. 
Configuration changes can include changes that require re-running the install method for a system, and these can be implemented by toggling the is_installed flag in an SOSContext.meta object by a config action.

These methods are utilized by using the `sos-toolkit config` command. 
When calling this command, you can provide a target object to configure.
``` 
(sos)$ sos-toolkit config --target=model_foo
```
This will have SOS-Toolkit lookup the object: `context.action.sos_config.model_foo` and attempt to run it. 

A system can also define a default configuration method which would be intended for an entry-point to a fully designed configuration interface. Calling the config command without a target will provide this functionality.
```
(sos)$ sos-toolkit config
```
This has the effect of running the object: `context.action.sos_config.default`

If a default action isn't defined for the system, it will run through all of the available config actions: `context.actions.sos_config`


This can also be used to access configuration methods for services by starting the target with the service tag and the name of the service:
```
(sos)$ sos-toolkit config --target=service.ollama.model_data
```
This will have SOS-Toolkit lookup the object: `context.service.ollama.action.model_data` and attempt to run it.

Changes using config actions will not be persisted if you generate a new context. 
It is possible for the system developers to make these changes persistent by writing the changes to an sos-local.yaml file.


The fourth method is to utilize the context command to directly modify context values. 
By calling the command with a target and a value, the object in the context will be set to the new value.
```
(sos)$ sos-toolkit context --target=namespace.foo.bar --value="new value"

[ sos-context.yaml ]
namespace:
  foo:
    bar: "new value"
```
Using this method will require knowing what the target object is and how changing the target object will affect the system.
Changing values in this way can cause serious problems if you target an incorrect object, provide an incorrect value, or if the system isn't designed to handle changes to the value. Changes using this command will not be persisted if you generate a new context.


## User Flow
The flow for a user using the SOS-Toolkit to run a system includes these commands:
```
(sos)$ sos-toolkit pull [ REMOTE_TARGET ]
(sos)$ cd [ system directory ]
(sos)$ sos-toolkit setup
(sos)$ sos-toolkit config
(sos)$ sos-toolkit update
(sos)$ sos-toolkit install
(sos)$ sos-toolkit up
(sos)$ sos-toolkit down
(sos)$ sos-toolkit clean
```

Since we are focused on developers for now, this flow should be accessible enough for general use.

## Developer Flow
The flow for a developer using the SOS-Toolkit includes these commands:
```
(sos)$ sos-toolkit pull [ REMOTE_TARGET ]
(sos)$ cd [ system directory ]
(sos)$ sos-toolkit setup
(sos)$ sos-toolkit config
(sos)$ sos-toolkit dev
(sos)$ sos-toolkit build
(sos)$ sos-toolkit up
(sos)$ sos-toolkit down
(sos)$ sos-toolkit update
(sos)$ sos-toolkit status
(sos)$ sos-toolkit commit
(sos)$ sos-toolkit fetch
(sos)$ sos-toolkit migrate
(sos)$ sos-toolkit clean
```
This method of using systems enables a clean separation between released versions for end-users, and development versions for developers. 
Advanced usage of these commands can enable you to target development on only certain component of a system, such as a backend versus a frontend. 
Each component can be targeted separately by the commands to preform different actions.

```
sos-toolkit build --target=backend ==> context.action.sos_build.backend
sos-toolkit up --target=backend ==> context.action.sos_up.backend
```

The workflow will be dependent on the way you define the actions in your system, and it can enable easy standardization between developers by implementing these actions uniformly. 
The commands on their own don't do anything, the actions are defined by the developer to meet whatever needs you have using whatever tools you want.

While developing, local repositories are assumed to be authoritative. 
This can cause problems of desyncing between local and remote repositories. 
Currently SOS-Toolkit does not have the capability to manage these conflicts, but that is intended to be included in the future.
If these problems occur, you will be required to manually work with the global installed git on the problem repository to fix the issue.
Developers can directly access both the system's repository or any sub-repositories, they are just folders.
The folders are git repositories, and you can interact with directly using any git commands.

One specific tool that still needs to be built, is the ability to begin working in a new development branch. 
Currently this is done by creating the branch from the git repository's interface, then manually switching the system to target it. 
This has worked up until now, but is obviously not very effective for large systems with many developers working independently.
It's possible to define a custom action to do this, but this is an example of a useful development action that SOS-Toolkit should specifically bundle.

The main goal of this version is a proof-of-concept for the Toolkit, full support of these features is intended for implementation with versions 0.2.X and 0.3.X, but we need to know what you want in order to implement it. 
 - What tools and what actions are needed for your workflows? 
 - How can we integrate these actions into already existing projects? 
 - How can we integrate these actions into other forms of development automation?
