## SOS-Service
One of the primary functions of the SOS-Toolkit is to provide simple, direct access to platform dependent services. 
These services need to be able to dynamically modify their operation in order to accommodate the diverse environments of users. 

This is not an easy task, and is essentially impossible to get working 100% of the time. 

Currently, we are starting with the default target being the Jetson platform. 
This is beneficial because while the services work on Jetson, we often need to preform custom actions in order to get a specific service working well. 
By implementing these actions, we can learn the best way to generalize this process to handle other architectures.

Services will largely remain "as-is" until we start working on version 0.3.X. 
We need both previous versions completed before we can start to implement these features.

The general idea is that a Service is a System. 
We can already implement the functionality of the services using the current SOS-Toolkit `sos-system.yaml` design style. 
This works for a specific environment, but it doesn't yet have the capability to be dynamic enough for generalized environments. 

In order to get where we want to be, we need to implement functionality that is able to efficiently finger-print environments in order to generate the target runtime for the service. 
By using the fingerprinting, we will be able to modify the runtime flow of Service actions using the SOS-Toolkit tools. 

Additional complexity comes from having to solve service dependency on other services. 
Services need to be able to require other services. 
This will run into issues with conflicting service versions or needing independent service instances.

It is a difficult goal, and the simpler path is by providing a default runtime environment that is intended to be as universal as possible based on CPU-only operation. 
This will work for many cases, but won't work for all; and it has the added flaw of poor performance to the extent of being unusable for many use-cases.

Figuring out how to work between these options is the goal for Services, and using the SOS-Toolkit's Systems, it is doable. 
We first need to fully implement the Runnable objects, the Tools, and runtime-branching.

For a listing of the currently included services: [SOS-Service](../06_reference/02_service.md)
