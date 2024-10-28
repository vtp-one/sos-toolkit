# Roadmap Focus
1. Concept
 - What is Digital Intelligence?
 - What does SOS-Toolkit do?
 - What does SOS-Toolkit not do?

2. SOS-Toolkit
 - Balancing functionality with accessibility
 - What do developers need?
 - What do users need?
 - What should we be opinionated about?
 - Where should we include pluggable points or provide hooks?

3. Review / Iterate
 - Development will require deciding if parts have been implemented incorrectly or if they aren't meeting an intended purpose
 - Components need to be modular in order to be easily refactor-able or replaceable
 - Components need to be distinct in order to prevent confused purpose or blurred intent

4. Annotations / Documentations
 - What information does Analog Intelligence need
 - What information does Digital Intelligence need
 - How can we automate the documentation to dynamically generate and refine content
 - How can we use the documentation as a metric to measure if components aren't meeting their intent or purpose

5. Digital Intelligence Integration
 - How do we enable new functionality?
 - What are the security and safety concerns?
 - How can we steer the direction of research to help our functionality?
 - When can Digital Intelligence start asking for features?


# Version Targets

## 0.0.1
 - Initial Version
 - Proof of Concept
 - Basic Examples
 - Basic Documentation

## 0.1.X
 - Refactor Redundant/Confusing Objects
 - Refactor MetaRunnable: sos_obj => Runnable, Resolvable, Condition, Repository
 - Refactor SOSContext:
   - change sos_action into sos_command 
   - change meta types to Namespace / Repository
 - Refactor action => command
 - Refactor tools/commands for JIT import (feasibility => what do we need to import versus what can we wait to import)
 - Refactor services
 - Basic Development Documentation
 - Initial Platforms

## 0.2.X
 - Tools / Basic Documentation
 - meta tool
 - tool git
 - tool config
 - tool docker
 - (other tools)

## 0.3.X
 - Services / Basic Documentation
 - meta service
 - docker service
 - git service
 - diffusion
 - text-to-speech
 - speech-to-text
 - audio generation
 - service service (meta service to generate services)
 - (other services)

## 0.4.X
 - Systems / Basic Documentation
 - System templates: system, service, internal, application, builder, generic, default, etc
 - System design
 - System functions
 - System support
 - (other systems)

## 0.5.X
 - Examples / Documentation
 - Development Examples
 - Usage Examples
 - Configuration Examples
 - Tutorials
 - Playground
 - command: sos-toolkit create 
 - other development commands

## 0.6.X
 - Refactor/Cleanup
 - buildout typing
 - buildout tests
 - Standardize internal path handling => absolute vs relative vs sos
 - Implement /sos path

## 0.7.X
 - Initial Permissions Implementations: global, toolkit, user, system, runtime, etc

## 0.8.X
 - sandboxing

## 0.9.X
 - Platform Implementation
 - Toolkit Versions Support
 - Service Versions Support
 - System Versions Support

## 0.10.X
 - System to Service Capability (meta services)

## 0.11.X
 - Refactor/Cleanup
 - Standardize Annotations
 - Finalize Permission Implementation

## 0.12.X
 - command: sos-toolkit serve
 - command: sos-toolkit web
 - command: sos-toolkit load / save
 - command: etc
 - Pluggable Commands

## 0.X.X
 - Unknown Breaking Changes

## 1.0.0
 - Initial Stable Version
 - Move from sos-toolkit namespace to sos namespace
 - OS level wrapper for sos-toolkit environment
 - Complete Documentation
 - Examples / Tutorial / Playground
 - Version Support

## 2.0.0
 - Digital Intelligence Integration
 - User Interface Support/Frontends
 - Internal Function Calling

## 3.0.0
 - OS Integration

## 4.0.0
 - Local Network Integration

## 5.0.0
 - Mesh Network Integration
