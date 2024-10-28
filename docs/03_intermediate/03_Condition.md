## SOS-Condition
Condition objects allow you to create conditions that are resolved from the SOSContext in order to disable or enable Actions. 
As part of the version 0.1.X refactor, they are intended to be migrated from their current object of a MetaCondition into a Runnable object. 

Currently they are defined in an `sos-system.yaml` file by using a list of dictionary objects. 
In order for the Action to be enabled, all the provided Condition objects must return `True`. 
Each dictionary object is used to create a MetaCondition object which is evaluated individually.

The current format for these objects is:
 - `label`: A text label for the condition
 - `ctx_key`: The Context object that is used for the comparison
 - `comparison`: A string object that defines the type of comparison the condition checks
 - `valid`: The valid values for the comparison
 - `raise_exc`: A boolean value to toggle if the condition fails whether it should return False or raise an exception
 - `is_inverse`: A boolean value that defines if the condition should return the inverse truthiness of the comparison

Currently the only implemented comparisons are: "in" or "equal", but future support is intended to include handling numerical values with comparisons such as "range", "<", ">", "<=", and ">=". 
Other comparisons will be added as needed.

An example of a condition object is:
```
- label: test condition
  ctx_key: namespace.foo
  comparison: equal
  valid: True
  raise_exc: False
```

Running this condition will check if the Context object `namespace.foo` equals `True`. 
It will then return the result of the comparison.


## Object is not None
Usage of conditions is currently convoluted, but functional. 
Advanced usage can include the ability to check if an object is not None.

For an example of this, we can use a condition to check if a value has been set. 
By creating an `sos-system.yaml` namespace object with the initial value of null, we can use this condition to run an action only if the context object has set.
```
[sos-system.yaml]
namespace:
  foo: null
```
The `null` value in a YAML file is parsed into python as a `None` object.

```
- label: test condition
  ctx_key: namespace.foo
  comparison: equal
  valid: null
  is_inverse: True
```
If the value of `namespace.foo` is not `None`, this condition will pass. We use the `is_inverse` paramater because we don't want the value to be `None`, we want the inverse of the comparison. These is_inverse conditions may be changed to instead use a different comparison string in the future: equal vs not_equal.


## Object in Values
Another use is the ability to provide lists of valid objects. If the context value is in the list, it will return `True`.
```
- label: test condition
  ctx_key: namespace.foo
  comparison: in
  valid: 
    - foo
    - bar
```
If the value of `namespace.foo` is either `"foo"` or `"bar"`, the condition will pass.
