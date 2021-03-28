import click

import subprocess
import os

from omg import version
from omg.cmd.use import use
from omg.cmd.project import project, projects, complete_projects
from omg.cmd.get_main import get_main
from omg.cmd.get.complete_get import complete_get
from omg.cmd.describe import describe
from omg.cmd.log import log, complete_pods, complete_containers
from omg.cmd.whoami import whoami
from omg.cmd.machine_config.machine_config import machine_config, complete_mc
from omg.completion import bash

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# Namespace related options shared by a few commands
_global_namespace_options = [
    click.option("--namespace", "-n", required=False, autocompletion=complete_projects),
    click.option("--all-namespaces", "-A", required=False, is_flag=True),
]


# Decorator lets us use namespace related options above
def global_namespace_options(func):
    for option in reversed(_global_namespace_options):
        func = option(func)
    return func


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command("use")
@click.argument("mg_path", required=False,
                type=click.Path(exists=True, file_okay=False, resolve_path=True, allow_dash=False))
@click.option("--cwd", is_flag=True)
def use_cmd(mg_path, cwd):
    """
    Select the must-gather to use
    """
    use(mg_path, cwd)


@cli.command("project")
@click.argument("name", required=False, autocompletion=complete_projects)
def project_cmd(name):
    """
    Display information about the current active project and existing projects
    """
    project(name)


@cli.command("projects")
def projects_cmd():
    """
    Display information about the current active project and existing projects
    """
    projects()


@cli.command("get")
@click.argument("objects", nargs=-1, autocompletion=complete_get)
@click.option("--output", "-o", type=click.Choice(["yaml", "json", "wide"]))
@click.option("--show-labels",is_flag=True,type=bool,help="When printing, show all labels as the last column (default hide labels column)")
@global_namespace_options
def get_cmd(objects, output, namespace, all_namespaces,show_labels):
    """
    Display one or many resources
    """
    get_main(objects, output, namespace, all_namespaces,show_labels)


@cli.command("describe")
@click.argument("objects", nargs=-1)
@global_namespace_options
def describe_cmd(objects, namespace, all_namespaces):
    """
    This command joins many API calls together to form a detailed description of a given resource.
    """
    describe(None)


@cli.command("logs")
@click.argument("resource", autocompletion=complete_pods)
@click.option("--container", "-c", autocompletion=complete_containers)
@click.option("--previous", "-p", is_flag=True)
@global_namespace_options  # TODO: Only support -n
def logs_cmd(resource, container, previous, namespace, all_namespaces):
    """
    Display logs
    """
    log(resource, container, previous, namespace, False)


@cli.command("whoami")
def whoami_cmd():
    """
    Display who you are
    """
    whoami(None)


@cli.command("version")
def version_cmd():
    """
    Display omg version
    """
    print('omg version ' + version + ' (https://github.com/kxr/o-must-gather)')


@cli.command("completion")
@click.argument("shell", nargs=1, type=click.Choice(["bash"]))  # TODO: zsh, fish
def completion(shell):
    """
    Output shell completion code for bash.

    \b
    For example:
      # omg completion bash > omg-completion.sh
      # source omg-completion.sh
    """
    if shell == "bash":
        print(bash.SCRIPT)
    else:
        print("Unsupported shell")


@cli.group("machine-config")
def mc_cmd():
    """
    Explore Machine Configs
    """
    pass


@mc_cmd.command("extract")
@click.argument("mc_names", nargs=-1, autocompletion=complete_mc)
def extract_mc_cmd(mc_names):
    """
    Extract a Machine Config
    """
    machine_config("extract", mc_names, False)


@mc_cmd.command("compare")
@click.argument("mc_names", nargs=2, autocompletion=complete_mc)
@click.option("--show-contents", is_flag=True)
def compare_mc_cmd(mc_names, show_contents):
    """
    Compare Machine Configs
    """
    machine_config("compare", mc_names, show_contents)
