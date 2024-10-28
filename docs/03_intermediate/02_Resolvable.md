## SOS-Resolvable
Resolvable objects enable actions to dynamically pull and push data from the context. 
The format for the objects will be modified in the 0.1.X refactor. 
The goal is to change the currently used MetaResolvable into a standard MetaRunnable object instead of an unique MetaResolvable object. 
This change will make defining them easier and more logical. 

Here is the current format for how they work to give you an idea of where they are going.

Resolvable objects are defined in YAML format as dictionary objects. 
Any location that supports MetaResolvable can either utilize a list of dictionaries that gets mapped to a list of MetaResolvables, or a single dictionary that gets mapped to a single MetaResolvable.

The simple fields of a Resolvable are:
 - `label`: a text description for the resolvable
 - `result`: the output key the resolvable should be returned to
 - `data`: the location of the data to be resolved

When a resolvable is run, SOS-Toolkit provides it with a source object and a result object. 
The source object is where the data is pulled from, and the result object is where the data should be placed. 
In the use case for a tool call, the source object will be the SOSContext object, and the result object will be a python dictionary: `__PARAMS__` that is unpacked for the tool call using dictionary unpacking.

### Example:
An SOSContext object with the following data:
```
__CTX__.namespace.foo = "bar"
__CTX__.namespace.bar = "bar2"

```

You can create a resolvable:
```
- label: get the value of foo
  result: foo_value
  data: namespace.foo
```
If used as a context_map for an action, this will generate a python dictionary:
```
__PARAMS__ = {"foo_value":"bar"}
```
Which is then used by the tool like this:
```
tool_function(**__PARAMS__)
tool_function(foo_value="bar")
```

It's also possible to provide a default value:
```
- label: get the value of bar
  result: bar_value
  data: namespace.bar
  default: bar_value
```

By providing multiple context_map objects, you can map data to different values in the output dictionary.
```
- label: get the value of foo
  result: foo_value
  data: namespace.foo
- label: get the value of bar
  result: bar_value
  data: namespace.bar
```
Will generate:
```
__PARAMS__ = {"foo_value":"bar", "bar_value":"bar2"}
```

## Dictionary Generation
Resolvables have more functionality then simple object lookups. 

The first useful feature is the ability to use multiple data objects to generate a dictionary. 
By providing the data parameter with a list of DataObjects, you can lookup multiple objects.
```
- label: generate foo_value
  result: foobar_value
  data:
    - source: namespace.foo
      target: foo
    - source: namespace.bar
      target: bar
```
Running this resolvable will generate the following object:
```
__PARAMS__ = {"foobar_value":{"foo":"bar", "bar":"bar2"}}
```

Data objects can also include default values or provide explicit string objects to include in the output.
```
- label: generate foo_value
  result: foobar_value
  data:
    - source: namespace.does_not_exist
      target: foo
      default: foo_default
    - source: null
      target: bar
      default: bar_default
```
Running this resolvable will generate:
```
__PARAMS__ = {"foobar_value":{"foo":"foo_default", "bar":"bar_default"}}
```


## String Formatting
A common use case is to combine multiple strings into a single string. 
This can be done by using the format_string parameter.
```
- label: generate foo_value
  result: foobar_value
  data:
    - source: namespace.foo
      target: foo
    - source: namespace.bar
      target: bar
  format_string: "foo_value: {foo} - bar_value: {bar}"
```
Running this resolvable first generates a data dictionary, then passes the dictionary to a python string format function.
```
format_string.format(**__DATA__)
```
Which then generates:
```
__PARAMS__ = {"foobar_value":"foo_value: bar - bar_value: bar2"}
```
THIS CAN BE UNSAFE! 
These objects will be run and passed on without any safety checks.


## Path Generation
Another common use case is to join objects together for a path. 
This can be done using the path_join parameter.
```
- label: generate foo_value
  result: foobar_value
  data:
    - source: namespace.foo
      target: foo
    - source: namespace.bar
      target: bar
    - source: null
      target: baz
      default: baz3
  path_join: True
```
This is done by first creating a list of the data and passing the list to the python function os.path.join.
```
__DATA__ = ["bar", "bar2", "baz3"]

os.path.join(*__DATA__)
```

Which will generate:
```
__PARAMS__ = {"foobar_value":"/bar/bar2/baz3"}
```
THIS CAN BE UNSAFE! 
These objects will be run and passed on without any safety checks.


## List Generation
One final common use case is the ability to return a list instead of a dictionary. 
This is done by using the to_list parameter.
```
- label: generate foo_value
  result: foobar_value
  data:
    - source: namespace.foo
      target: foo
    - source: namespace.bar
      target: bar
    - source: null
      target: baz
      default: baz3
  to_list: True
```
Which will generate:
```
__PARAMS__ = {"foobar_value":["bar", "bar2", "baz3"]}
```


## Recursive Resolvables
Data objects can also be Resolvable objects by including a label and defining the object as previously demonstrated.
```
- label: generate foo_value
  result: foobar_value
  data:
    - label: generate internal value1
      result: internal_value1
      data: 
        - source: namespace.foo
          target: foo
        - source: namespace.bar
          target: bar

    - label: generate internal value2
      result: internal_value2
      data: 
        - source: null
          target: v1
          default: value1
        - source: null
          target: v2
          default: value2
```
Which will generate:
```
__PARAMS__ = {"foobar_value":{"internal_value1":{"foo":"bar","bar":"bar2"}, "internal_value2":{"v1":"value1", "v2":"value2"}}}
```



## result_map
Using Resolvable objects it's possible to dynamically generate complex objects that are used for both getting data from the context and setting data in the context. 

The result_map parameter for an action works in the inverse direction as the context_map. 
The Resolvable object is provided a Result object from the tool run as the source location and the result location is the `__CTX__` object.

Defining a result_map object:
```
result_map:
  - label: test result_map
    data: output
    result: namespace.foobar
```

If the tool returns the following object:
```
return {"output":"test_value"}

```

Will map the output value to context.namespace.foobar

```
__CTX__.namespace.foobar = "test_value"
```

A result_map can utilize all the features already demonstrated for a Resolvable object.
