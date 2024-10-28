## SOS-Action
The functionality for SOS-Toolkit is defined in Action objects. 

Currently the naming of the objects and the associated classes is a convoluted mess that is the current focus of refactoring for version 0.1.X. 
This document will attempt to describe the general concepts behind Actions, but will be rewritten to better reflect the future objects.

## Action
Action objects are derived from an `sos-system.yaml` file.
In the file, they are written as YAML dictionary objects.

An Action object is defined with the following properties:
 - `label`: A text description of what the action does
 - `tool`: A dot-notation reference to the tool the action uses - `tool_namespace.tool_name`
 - `disabled`: A boolean flag if the action is disabled
 - `condition`: A list of MetaCondition objects that are evaluated prior to running the action
 - `params`: A dictionary of key-value pairs that provides parameters to the tool when run
 - `context_map`: A list of MetaResolvable objects that are used to map values from the SOSContext object to parameter keywords for the tool to use
 - `result_map`: A list of MetaResolvable objects that are used to map return values from the tool run to an SOSContext key
 - `callbacks`: A list of MetaRunnable objects that are called after the initial tool is run


Broadly speaking, an action needs only one value: tool. When run the tool is called as a function. 
```
test_action:
  tool: terminal.print_context
```
This will call the function `print_context`, located in the SOS-Toolkit tool namespace: `terminal`
```
print_context()
```

Simple values can be passed directly as parameters to the called function using the params field.
```
test_action:
  tool: terminal.print_object
  params:
    obj: "Hello SOS!"
```
This will call the function `print_object`, located in the SOS-Toolkit tool namespace: `terminal`, with the keyword argument `obj="hello SOS"`
```
print_object(obj="Hello SOS!")
```


The capabilities of SOS-Toolkit comes from the usage of the `condition`, `context_map`, and `result_map`

More information about their use is provided in the files:
 - [Resolvables](02_Resolvable.md)
 - [Condition](03_Condition.md)

These fields allow for interacting with objects from the SOSContext. 
Using these capabilities you can generate complex variable resolutions. 
By saving return values from one tool, you then use the value using subsequent actions.


## ActionRepo
Action objects can be stored in ActionRepo objects which act as lists of Actions that get called in sequence. 
When run they function as sequential lists, but they are defined in an `sos-system.yaml` file as a YAML dictionary.
```
test_repo:
  action1:
    tool: terminal.print_object
    params:
      obj: action1
  action2:
    tool: terminal.print_object
    params:
      obj: action2
```
As SOS-Toolkit progresses through the ActionRepo list of Actions, it checks if the action is disabled through the usage of the disabled field along with checking all the provided conditions. 

If an action is not disabled, it gets run, otherwise it proceeds to the next Action in the ActionRepo list. 

Actions can pass values to subsequent actions using two special SOSContext objects: `__TARGET__` and `__RESULT__`. 
These objects are stored in the SOSContext and are removed after running through an ActionRepo.

An ActionRepo can contain other ActionRepo objects.
Certain commands use this functionality to allow control over calling a specific ActionRepo by using other control tools and methods.

Actions can modify runtime flow be utilizing special tools. 
This includes features such as branching execution, matching cases, breaking out of a running ActionRepo, and raising or handling exceptions.
Information about these tools will be added in 0.2.X once their functionality is stable.
