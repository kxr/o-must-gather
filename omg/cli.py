import click
import os
import subprocess

from omg import version
from omg.config import logging, config
from omg.use import use
from omg.project import project, projects
from omg.project.complete import complete_projects
from omg.get import get
from omg.get.complete import complete_get
from omg.log.complete import complete_pods, complete_containers
from omg.whoami import whoami
from omg.log import log
# from omg import machine_config


# Common Options used by multiple subcommands
o_filtered_path = click.option(
    "-p", "--path", type=int, default=0)

o_log_level = click.option(
    "-l", "--loglevel", type=click.Choice(["normal", "info", "debug", "trace"]))

o_namespace = click.option(
    "--namespace", "-n", required=False, autocompletion=complete_projects)

o_all_namespaces = click.option(
    "--all-namespaces", "-A", required=False, is_flag=True)


# Main click group
@click.group()
@o_log_level
@o_filtered_path
@o_namespace
@o_all_namespaces
def cli(loglevel, path, namespace, all_namespaces):
    logging.setup_logging(loglevel)
    config.filtered_path = path
    if namespace:
        config.namespace = namespace
    if all_namespaces:
        config.all_namespaces = all_namespaces


# omg *use*
@cli.command("use")
@click.argument("mg_paths", nargs=-1, required=False, type=click.Path(
                    exists=True, file_okay=False, resolve_path=True, allow_dash=False))
@click.option("--cwd", is_flag=True)
def use_cmd(mg_paths, cwd):
    """
    Select one or more must-gather(s) to use
    """
    use.cmd(mg_paths, cwd)


# omg *project*
@cli.command("project")
@click.argument("name", required=False,
                autocompletion=complete_projects)
def project_cmd(name):
    """
    Switch to another project
    """
    project.cmd(name)


# omg *projects*
@cli.command("projects")
def projects_cmd():
    """
    Display existing projects
    """
    projects.cmd()


# omg *get*
@cli.command("get")
@click.argument("objects", nargs=-1, autocompletion=complete_get)
@click.option("--output", "-o", type=click.Choice(["yaml", "json", "wide", "name"]))
@click.option("--show-labels", is_flag=True, type=bool)
@o_namespace
@o_all_namespaces
def get_cmd(objects, output, show_labels, namespace, all_namespaces):
    """
    Display one or many resources
    """
    if namespace:
        config.namespace = namespace
    if all_namespaces:
        config.all_namespaces = all_namespaces
    get.cmd(objects, output, show_labels)


# omg *log*
@cli.command("logs")
@click.argument("resource", autocompletion=complete_pods)
@click.option("--container", "-c", autocompletion=complete_containers)
@click.option("--previous", "-p", is_flag=True)
@o_namespace
def logs_cmd(resource, container, previous, namespace):
    """
    Print the logs for a container in a pod
    """
    if namespace:
        config.namespace = namespace
    log.cmd(resource, container, previous)


# omg *whoami*
@cli.command("whoami")
def whoami_cmd():
    """
    Tell you who you are
    """
    whoami.cmd()


# omg *version*
@cli.command("version")
def version_cmd():
    """
    Prints the version of o-must-gather
    """
    print()
    print("omg version " + str(version) + " (https://github.com/kxr/o-must-gather)")
    print()


@cli.command("completion")
@click.argument("shell", nargs=1, type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell):
    """
    Output shell completion code for the specified shell (bash or zsh)
    """
    newenv = os.environ.copy()
    newenv["_OMG_COMPLETE"] = "{}_source".format(shell)
    subprocess.run("omg", env=newenv)


# Click group for machine-config
@cli.group("machine-config")
def mc_cmd():
    """
    Explore Machine Configs
    """
    pass


# # omg machine-config *extract*
# @mc_cmd.command("extract")
# @click.argument("mc_names", nargs=-1, autocompletion=complete_mc)
# @click.option("--yaml-loc", "-y", required=False,
#               type=click.Path(exists=True, file_okay=True, resolve_path=True, allow_dash=False))
# @click.option('--out-dir', '-d',  required=False,
#                 type=click.Path(exists=True, file_okay=False, resolve_path=True, allow_dash=False)) # noqa
# def extract_mc_cmd(mc_names):
#     machine_config("extract", mc_names, False, yaml_loc, out_dir)


# # omg machine-config *compare*
# @mc_cmd.command("compare")
# @click.argument("mc_names", nargs=2, autocompletion=complete_mc)
# @click.option('--yaml-loc', '-y', required=False,
#                 type=click.Path(exists=True, file_okay=True, resolve_path=True, allow_dash=False))
# @click.option("--show-contents", is_flag=True)
# def compare_mc_cmd(mc_names, show_contents):
#     """
#     Compare Machine Configs
#     """
#     machine_config("compare", mc_names, show_contents, yaml_loc, None)
