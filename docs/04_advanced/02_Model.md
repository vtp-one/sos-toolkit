## SOS-Model
Objects in SOS-Toolkit are built from a custom object based from pydantic BaseModel.

The specific objects are located in the sos-toolkit source under `meta/_model.py`. 
The two objects are called `ModelGet` and `ModelDict`. 
All other SOS-Toolkit objects are sub-classed from these two objects.

As part of the 0.1.X refactor, these objects will be modified.


## ModelGet
ModelGet is the primary object and ModelDict is a sub-class of it. 
The ModelGet base object is a pydantic BaseModel, and it inherits it's base functionality from there. 
It implements additional functionality to enable the usage of dot-notation to traverse arbitrary depth levels of ModelGet objects. 
This can be used in two ways, either directly through the object:
```
context.foo.bar.baz = "foobar"
```
Or by using the methods provided by ModelGet: `get`, `set`, `remove`, `has`.
```
context.get("foo.bar.baz")
context.set("foo.bar.baz", "foobar")
context.remove("foo.bar.baz")
context.has("foo.bar.baz")
```

This functionality can include the usage of internal lists by utilizing the `[IDX]` syntax. 
This functionality has not been very well tested, and does not work for multiple adjacent lists: `[IDX][IDX]`.
It also will have some strange results if you are attempting to create a new list or extend a list.
```
context.set("foo.bar[12].baz.bam[6]", "foobar")
context.get("foo.bar[12].baz.bam[6]")
```


Two additional methods provided by ModelGet are `print` and `pp`. 
Print will print the complete object to the terminal, pp generates a pretty_repr string of the object.


## ModelDict
ModelDict differs from ModelGet by enabling the pydantic config flags: `extra` and `arbitrary_types_allowed`. 

Using these config flags allows us to utilize the object directly as a dictionary and to also dynamically define model fields that can be utilized with the dot-notation.

ModelDict provides standard dictionary methods: `values`, `items`, `keys`, and `__dir__`.

The use of these objects as dictionaries works second to their existence as pydantic models. 
What that means is that the dictionary these objects represent, only includes the pydantic fields they contain. 
This also allows for objects to be added to the dictionary to be included in the output from the pydantic BaseModel.dict method when turning the object back into a python dictionary.


## SOS-Models
The sub-classes of these objects implement their own `@classmethods` that work to generate the functional internals for these features. 

Currently these objects are stored in various locations and will be refactored as part of 0.1.X. A current list of these objects includes:
 - `MetaConfig`
 - `SystemNamespace`
 - `SOSContext`
 - `ActionRepo`
 - `ActionRoot`
 - `ActionParams`
 - `ActionTask`
 - `ActionObject`
 - `ActionConfig`
 - `HookParams`
 - `HookTask`
 - `HookObject`
 - `HookConfig`
 - `MetaRepo`
 - `MetaRoot`
 - `MetaAnnotation`
 - `MetaSchema`
 - `MetaCondition`
 - `MetaResolvable`
 - `MetaRunnable`
 - `MetaObject`
 - `MetaConfig`
 - `ResultData`
 - `ResultObject`
 - `ResultRepo`
 - `ServiceParams`
 - `ServiceTask`
 - `ServiceObject`
 - `ServiceConfig`
 - `ToolObject`
 - `ToolRepo`
 - `ToolRoot`

Most of the useful objects have been discussed elsewhere, but the list is obviously convoluted. 
The intent of 0.1.X refactoring is to shrink this list into a more sensible grouping of object functionality.

After these objects are refactored, more documentation about their unique fields, attributes, functions, and usage will be added.
