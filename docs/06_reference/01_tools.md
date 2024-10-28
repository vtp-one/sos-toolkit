# SOS-Tool
A non-complete list of available tools.

Tools are not described in any detail at this time.

Not all tools are fully functional.

Usage of tools in actions follows the format:
```
tool: tool_namespace.tool_command
```

# Tool Namespaces
 - `cli`
 - `context`
 - `docker`
 - `filesystem`
 - `git`

# cli
Call commands from the command line.

 - `cmd_popen`

# context
Preform operations on or with the context

 - `ctx_parse`
 - `ctx_format`
 - `ctx_resolve`
 - `ctx_flag`
 - `ctx_set`
 - `ctx_remove`
 - `ctx_has`
 - `ctx_get`
 - `ctx_merge`
 - `repo_remove`
 - `runtime_object`
 - `runtime_nested`
 - `runtime_breakpoint`
 - `runtime_exception`
 - `runtime_match`
 - `runtime_local`
 - `runtime_break`
 - `tool_remove`
 - `tool_string`
 - `tool_function`
 - `tool_file`
 - `tool_module`

# docker
Preform operations using docker

 - `compose_up`
 - `compose_down`
 - `network_create`
 - `network_remove`
 - `network_exists`
 - `container_run`
 - `container_stop`
 - `container_running`
 - `buildx_bake`
 - `buildx_build`
 - `image_load`
 - `image_exists`
 - `image_delete`
 - `volume_exists`
 - `volume_create`
 - `volume_delete`

# filesystem
Preform operations using filesystem objects

 - `directory_exists`
 - `directory_delete`
 - `directory_create`
 - `directory_list`
 - `path_join`
 - `path_exists`

# git
Preform operations using git

 - `repo_clone`
 - `repo_status`
 - `repo_commit`
 - `repo_fetch`
 - `repo_pull`
 - `repo_checkout`

# terminal
Preform operations using the current terminal interface

 - `input_prompt`
 - `print_result`
 - `print_object`
 - `print_context`
 - `print_callback`
