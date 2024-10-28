# Digital Intelligence
Digital Intelligence is the capability for digital systems to utilize accumulated state to be intelligent. 
Accumulated state can take many forms, but one example is the model file for a Large Language Model. 
By running billions of calculations and accumulating data using specialized algorithms, systems can use the data to preform intelligent interactions with inputs. 

The data is digital, the state is digital, the systems are digital; which makes them digital intelligence.


Digital Intelligence is also more than a single layer of this accumulated state. 
The newest types of digital intelligence are already showing emergent capabilities related to how they use and interact with these state objects. 
Some of the most notable examples would be fine-tuned LLM models, LORA models for diffusion, and vector databases for retrieval-augmented generation.
These capabilities have the potential to change how the systems interact with us and the wider world.

Currently these systems are stuck in specialized environments that force them to remain static in respect to their software and hardware dependencies.
A LORA model only works with the base model it was trained with. 
Vector databases can have inconsistent results due to differences in environments.
The developer description would be dependency hell taken to an extreme, and anyone who has tried to use even a simple system on local hardware has certainly experienced it.


Which brings us to the first goal of the SOS-Toolkit: 
 - Define what Digital Intelligence Systems are and what is needed to distribute them

Many of the ideas needed are in beta forms in various disconnected projects, but most of them are imitating the closed-source companies that are trying to define specifications as a means of vendor lock-in instead of user functionality.
Breaking out of this trend will not be easy, but it has to be done if we want these systems to reach their full potential.


# Digital Intelligence Systems
The broadest interpretation would be any application, program, or system that exists. 
Intelligence isn't a very well-defined metric when we are talking about computer programs.
Defining boundaries between programmed intelligence, generative intelligence, emergent intelligence, or any other type of intelligence is even more confusing.

SOS-Toolkit is able to function as a general purpose tool because it has the capability to wrap, normalize, and utilize existing tools.
If you want to use it as a helpful wrapper for a traditional docker container based application or any other build system your traditional application might use; it will work and we aim to support those use cases as well.

Our intent for Digital Intelligence Systems is the next generation of machine learning based systems. 
These systems will require multiple layers of interacting machine learning based processes.
A simple example is to take the current iteration of agent-based systems and give them access to more capabilities.
Those capabilities could be working with agents from different systems, interacting with function calling, other machine learning components (text, speech, audio, images, etc), vector-databases, long-term databases, recursive fine-tuning; and who knows what else we can come up with.

What we do know is that these types of multi-layered systems are very difficult to develop and almost impossible to distribute.
Our current focus is providing the functionality to distribute some of the currently existing single-layer digital intelligence systems.
These represent the services that will make up the building blocks for a future Digital Intelligence System.
Once we are able to accommodate the different quirks for these services, we can start connecting them together in new ways.


# Local Digital Intelligence Systems
The current standard method is building a static environment inside a docker container. 
There will be multiple versions of the container for different targets, but the container is an attempt to standardize the runtime environment. 
This works well-enough for a single layer system such as an ollama server. 

Getting these systems to work for users is often difficult because they need to manage interactions with resources external to the container such as folders for storing outputs and inputs, network addresses for other containers, or remote targets for data.
Implementing these basic forms of user configuration is a free-for-all with each project using their own methods.

More problems arise if your system requires multiple layers of these specialized containers.
By adding additional layers, you introduce new and increasingly difficult to debug errors that break systems in often invisible ways.


An example is how do you distribute a pre-built vector database for [Retrieval-Augmented Generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)? 


The easy answer would be to include it as a file like any other, but that won't work outside of the specific generation environment. 
The database is dependent on the entire stack of software and hardware used for it's generation. 
It is possible to make a static distribution of this process in a containerized form, but you now have another separate container that will need to be provided for multiple platforms, and there will be compatibility issues. 
It's possible, but with a simple addition to the system, you've taken something that was difficult to maintain and made it exponentially harder. 

What happens if you want to completely swap out the embedding model for something brand new that runs 10X faster? 
Most likely, the stack collapses and you are left rebuilding. 
Even if you are able to effectively package it, how do you provide an update path from the old database to the new database? 

One more thought, are you going to try to support the now abandoned container stack as well? 

These types of breaking changes seem to be happening almost monthly for some part of the digital intelligence eco-system, and to keep your system on that cutting edge, you need to be able to integrate constant changes.

We need a way for the tools we use to solve these issues and more.


# SOS-Toolkit
There are too many different development/environment/configuration/management/whatever tools; but we need another. 

The goal is to reinvent as little as possible. 
Instead we are trying to create a System of Systems (SOS) that functions how we need in order to quickly and effectively build things that work. 
Using the already existing tools will allow us to develop faster, but we will quickly inherit legacy problems instead of focusing on features. 
There are many reasons why the current tools aren't able to do what we need. 
We will need to find a balance between new and old. 
This requires implementing a modular approach to as much of SOS-Toolkit as possible – parts will need to be replaced for something better without breaking everything else.


That is the current iteration for SOS-Toolkit. 
Using a mixture of three old systems: python, docker, and git; we can create something functional to start from and use it until it breaks.


SOS-Toolkit is meant as a developer tool, which allows it to focus on functionality more than usability. 
You are going to need to read documentation before being able to use it and it will have the potential to break catastrophically when you least expect it. 
It is in a pre-alpha state, and there is a long road before we have something stable. 
There will be arbitrary breaking changes and we don't know when they will occur.


The end result is a tool that works in the background turning digital intelligence from a dependency hell into something as simple as clicking a link or calling a function. 
Developers will directly interact with SOS-Toolkit as they need, but users won't even know it's there.


# Annotate The Tools
The next stage of the project is that we are not creating a tool for only humans to use. 
We want to create something that digital intelligence will be able to use as well. 

We have the starting ideas for how that will work: documentation and annotation. 

Generative LLM systems are already able to utilize these forms of information in surprisingly efficient ways. 
As we start moving beyond initial functionality, we can start to focus on how best to generate and use this information to allow the systems to use the tools as well.


# Input / Output Interfaces
This is our goal for SOS-Toolkit and Digital Intelligence. 

These systems function extremely well as input/output interfaces to new or already existing systems. 
Most systems and startups are focused on trying to build the "killer app" that everyone needs, we've been thinking a better model is the introduction of touch-screen displays. 
Smartphones ushered in the widest and fastest technological change ever, because they fundamentally changed the way we interact with computers in a way that made them both more functional and more accessible. 
How we interact with systems and how the systems present information to us; both parts can be improved by digital intelligence. 
Using digital intelligence as a user interface for already existing systems opens the possibilities for the digital intelligence to learn how to personalize the process to work better for each individual user. 

Once we get to that point is when things get really interesting, especially when the systems start building new tools for us and for themselves.
```
Computer make me a sandwich.
[Permission Denied]
Computer please make me a sandwich.
                                                                                
                                ▒▓▒▒░                                           
                             ░▓▓▒▒░▒▒▒▓▓▓▓▓▒░                                   
                           ▓▓▓░            ▒▓▓▓▓▓▓▓▒░                           
                        ▒▓▓▒                     ░▒▒▓▓▓▓▓▒░                     
                      ▓▓▓░                               ▒▓▓▓▓▓▓▒░              
                   ░▓▓▒                                        ░▒▓▓▓▓▒          
                 ▓▓▓▒                                                ▒▓▓▓▓      
               ▒▓▓                                                    ▒▓▓▓      
            ░▓▓▓                                                    ▒▓▓▓▓▓      
          ▒▓▓▒                                                     ▓▓▓▓▓▓▓      
        ░▓▓▒                                                     ▒▓▓▓▓▓▓▓▒      
       ▒▓▒                                                     ▒▓▓▓▓▓▓░▒▓▓      
      ▒▓▓▒                                                   ▒▓▓▓▓▓▓▒   ▒▓▓     
      ▓▓▓▓                                                 ▒▓▓▓▓▓▓▒    ▓▓▒▓▓░   
      ▒▓▓▓▓▓▒                                            ▒▓▓▓▓▓▓▒    ▒▓▒   ▒▓▒  
       ▒▓▓▓▓▓▓▓▒▒▒░░  ░░░▒                             ▒▓▓▓▓▓▓▒     ▓▓▒     ▒▓  
        ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒                         ▓▓▓▓▓▓▓▒      ▓▓       ▒▓░ 
        ▒▓▓▓▒▒▒▓▓▓▓▓▓▓▒▒▓▓▓▓▓                     ░▓▓▓▓▓▓▓░      ▒▓▓        ▓▒  
     ▒▓▓▓▓▓▓▓            ▓▓▓▓▓▓▒                ▒▓▓▓▓▓▓▓░       ▓▓▒        ▒▓▒  
   ▒▓▓▒  ▒▓▓▓▓▒           ▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒        ▓▓▓░        ▓▓▓░  
  ▒▓▒     ▓▓▓▓▓▓▒           ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒       ▒▓▓▓▒        ▓▓▓▓▓▒  
 ░▓▒       ▒▓▓▓▓▓▓▒             ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒        ▒▓▓▓▒       ▒▓▓▓▒ ▓▓▓▒  
  ▓▒         ▒▓▓▓▓▓▓         ░░▒▒▓▓▓▓▓▓▓▓▓▓▓▒         ▒▓▓▓░       ▓▓▒░    ▓▓▓▒  
  ░▓▒             ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒    ▒▓▓▓▒        ▒▓▒      ▓▓▓▓   
    ▒▓▓▓▓▓▒                 ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒          ▓▓▒     ▒▓▓▓▓░   
      ▓▓▓▓▓▓▓▓░                  ░▒▓▓▓▓▓▓▓▒    ▒▓▓▒         ░▓▓▓     ▒▓▓▓▓▓     
       ▒▓▓▓▓▓▓▓▓▓▒                                     ▒▒▓▓▓▒░     ▒▓▓▓▓▒       
       ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░               ▓▓▓▓       ░▓▓▓▓▓▓         
       ▓▓▓      ░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒           ░▓▓▓░      ░▓▓▓▓▓▓           
       ▒▓▓▓                ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒      ▓▓▓▒      ▒▓▓▓▓▓▓░            
       ░▓▓▓▓▓▒                   ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒      ▒▓▓▓▓▓▓               
         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░           ▓▓▓▓▓▓▓▓▓▓▓▓░      ▓▓▓▓▓▓▓                 
           ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                ░         ░▓▓▓▓▓▓▓                   
                ▒▒▓▓▓▓▓▓▓▓▓▓▓                      ▓▓▓▓▓▓▓▓                     
                         ▒▓▓▓▓▓▓▒             ░▒▓▓▓▓▓▓▓▓▒                       
                           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒                         
                             ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░                            
                                ░▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒                                
```

# More To Come
SOS-Toolkit is just one part of a much larger project, but it is the introductory component that starts progress towards the rest. 

As work continues on SOS-Toolkit, more information about the surrounding parts will be added when time permits.
If you want to get involved, the current central point for communication is this repository.
Additional channels will be added as needed or requested, but this is enough for now.
