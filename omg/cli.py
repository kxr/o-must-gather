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
from omg.log import log
from omg.whoami import whoami
from omg.components.ceph import ceph
from omg.components.etcdctl import etcdctl
from omg.machine_config.compare import mc_compare
from omg.machine_config.extract import mc_extract


# Common Options used by multiple subcommands
o_filtered_path = click.option(
    "-P", "--path", type=int, default=0)

o_log_level = click.option(
    "-l", "--loglevel", type=click.Choice(["normal", "info", "debug", "trace"]))

o_namespace = click.option(
    "--namespace", "-n", required=False, shell_complete=complete_projects)

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
    if path:
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
@o_log_level
@o_filtered_path
def use_cmd(mg_paths, cwd, loglevel, path):
    """
    Select one or more must-gather(s) to use
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    use.cmd(mg_paths, cwd)


# omg *project*
@cli.command("project")
@click.argument("name", required=False,
                shell_complete=complete_projects)
@o_log_level
@o_filtered_path
def project_cmd(name, loglevel, path):
    """
    Switch to another project
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    project.cmd(name)


# omg *projects*
@cli.command("projects")
@o_log_level
@o_filtered_path
def projects_cmd(path, loglevel):
    """
    Display existing projects
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    projects.cmd()


# omg *get*
@cli.command("get")
@click.argument("objects", nargs=-1, shell_complete=complete_get)
@click.option("--output", "-o", type=click.Choice(["yaml", "json", "wide", "name"]))
@click.option("--show-labels", is_flag=True, type=bool)
@o_log_level
@o_namespace
@o_all_namespaces
@o_filtered_path
def get_cmd(objects, output, show_labels, loglevel, namespace, all_namespaces, path):
    """
    Display one or many resources
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    if namespace:
        config.namespace = namespace
    if all_namespaces:
        config.all_namespaces = all_namespaces
    get.cmd(objects, output, show_labels)


# omg *log*
@cli.command("logs")
@click.argument("resource", shell_complete=complete_pods)
@click.option("--container", "-c", shell_complete=complete_containers)
@click.option("--previous", "-p", is_flag=True)
@o_log_level
@o_filtered_path
@o_namespace
def logs_cmd(resource, container, previous, namespace, loglevel, path):
    """
    Print the logs for a container in a pod
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
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


# omg *ceph*
@cli.command("ceph", context_settings={"ignore_unknown_options": True})
@click.argument("ceph_args", nargs=-1)
@click.option("--output", "--format", "-o", type=click.Choice(["json", "json-pretty"]))
@o_log_level
@o_filtered_path
def ceph_cmd(ceph_args, output, loglevel, path):
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    ceph.cmd(ceph_args, output, com="ceph")


# omg *rados*
@cli.command("rados", context_settings={"ignore_unknown_options": True})
@click.argument("ceph_args", nargs=-1)
@o_log_level
@o_filtered_path
def rados_cmd(ceph_args, loglevel, path):
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    ceph.cmd(ceph_args, None, com="rados")


# omg *rbd*
@cli.command("rbd", context_settings={"ignore_unknown_options": True})
@click.argument("ceph_args", nargs=-1)
@o_log_level
@o_filtered_path
def rbd_cmd(ceph_args, loglevel, path):
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    ceph.cmd(ceph_args, None, com="rbd")


# omg *etcdctl*
@cli.command("etcdctl", context_settings={"ignore_unknown_options": True})
@click.option("--output", "--write-out", "-o", type=click.Choice(["json", "table", "simple"]))
@click.argument("etcdctl_args", nargs=-1)
@o_log_level
@o_filtered_path
def etcdctl_cmd(etcdctl_args, output, loglevel, path):
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    etcdctl.cmd(etcdctl_args, output)


# Click group for machine-config
@cli.group("machine-config")
def mc_cmd():
    """
    Explore Machine Configs
    """
    pass


# omg machine-config *extract*
@mc_cmd.command("extract")
@click.argument("mc_names", nargs=-1)
@o_log_level
@o_filtered_path
def extract_mc_cmd(mc_names, loglevel, path):
    """
    Extract Machine Configs
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    mc_extract(mc_names)


# omg machine-config *compare*
@mc_cmd.command("compare")
@click.argument("mc_names", nargs=2)
@click.option("--show-contents", is_flag=True)
@o_log_level
@o_filtered_path
def compare_mc_cmd(mc_names, show_contents, loglevel, path):
    """
    Compare Machine Configs
    """
    if loglevel:
        logging.setup_logging(loglevel)
    if path:
        config.filtered_path = path
    mc_compare(mc_names, show_contents)
