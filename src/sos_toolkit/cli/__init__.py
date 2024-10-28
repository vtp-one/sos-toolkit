###
#
from typing import Annotated, Optional
import inspect
import os
import forge

import rich
import typer
from click import Context

import git

import sos_toolkit

from sos_toolkit.meta._global import DEBUG_ENABLE, SOS_SOURCE
from sos_toolkit.root import TOOLKIT_PATH

RICH_ERRORS = DEBUG_ENABLE and os.environ.get("RICH_ERRORS", True)

#
###

###
#
# change command list order to insertion order
class OrderCommands(typer.core.TyperGroup):
    def list_commands(self, ctx: Context):
        """Return list of commands in the order appear."""

        # get commands using self.commands
        return list(self.commands)

cli_app = typer.Typer(cls=OrderCommands, pretty_exceptions_enable=RICH_ERRORS)

#
###

###
#
@cli_app.command()
def test():
    rich.print(f"SOS_TOOLKIT CLI TEST - version: [green]{sos_toolkit.__version__}[/green]")

    # test toolkit source
    remote = git.repo.Repo(TOOLKIT_PATH).remote().url.removesuffix(".git")
    if remote != SOS_SOURCE:
        rich.print(f"[red]SOS_TOOLKIT SOURCE INCORRECT[/red] - valid: {SOS_SOURCE} - current: {remote}")

#
###

###
#
#
# TODO
# - change this to differentiate between sos_action and system_action
# - how? move all sos_actions up to this level?
# - parse actions at runtime?
# - this is neat functionality that is intended for usage much latter
# - do we need this?
#
for action in sos_toolkit.meta.SOS_ACTION.sos.values():
    optional = []
    required = []
    if "__CTX__" in action.sos_schema.keys():
        e = "SOS_ACTION SHOULD NOT HAVE __CTX__ PARAMETER"
        raise RuntimeError(e)

    for schema in action.sos_schema.values():
        #
        # TODO
        # - need to get an actual required value vs none vs default
        # - value = None vs value = ""
        # - need to make sure the typing works correctly
        # - need to be work with return types => needs to be implemented in metaschema
        #
        match schema.default:
            case None:
                _type = Annotated[schema.kind, typer.Argument(help=schema.description)]
                p = forge.arg(schema.key, type=_type)
                required.append(p)

            case _:
                _type = Annotated[schema.kind, typer.Option(help=schema.description)]
                p = forge.arg(schema.key, type=_type, default=schema.default)
                optional.append(p)

    parameters = required + optional

    #
    # TODO
    # - return types => need to add to sos_schema
    # - def foo() => str:
    #
    sig = forge.FSignature(parameters=parameters)

    action.function.__signature__ = sig.native

    cli_app.registered_commands.append(
        typer.models.CommandInfo(
            name=action.key,
            cls=typer.core.TyperCommand,
            context_settings=None,
            callback=action.function,
            help=action.description,
            epilog=None,
            short_help=None,
            options_metavar="[OPTIONS]",
            add_help_option=True,
            no_args_is_help=False,
            hidden=False,
            deprecated=False,
            # Rich settings
            rich_help_panel=typer.models.Default(None),
        )
    )

#
###


###
#
sos_placeholder = typer.Typer(pretty_exceptions_enable=RICH_ERRORS)
@sos_placeholder.command()
def not_implemented():
    raise NotImplementedError()

#
###