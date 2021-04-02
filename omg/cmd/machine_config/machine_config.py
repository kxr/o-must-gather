from omg.cmd.machine_config.compare import compare
from omg.cmd.machine_config.extract import extract
from omg.cmd.get_main import get_resource_names

def complete_mc(ctx, args, incomplete):
    """
    Callback for machine-config name autocompletion
    :return: List of matching machine-config names or empty list.
    """
    if incomplete is not None:
        mc_listing = get_resource_names('mc')
        suggestions = [ns for ns in mc_listing if ns.startswith(incomplete)]
        return suggestions
    return []



def machine_config(mc_op, mc_names, show_contents):
    if mc_op == 'extract':
        if len(mc_names) <= 0:
            extract('_all')
        else:
            extract(mc_names)
    elif mc_op == 'compare':
        if len(mc_names) == 2:
            compare(mc_names, show_contents=show_contents)
        else:
            print('[ERROR] Provide two machine-configs to compare')
