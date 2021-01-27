from click import Context

from omg.common.config import Config
from omg.cmd.get import parse
from omg.cmd.get_main import get_resources
from omg.common.resource_map import map

def complete_get(ctx: Context, args, incomplete):
    """
    Pull out objects args from Click context and return completions.
    """
    try:
        c = Config()
        objects = ctx.params.get("objects")
        # If user has set namespace ( with -n), we use that
        # else we use namespace set by `omg project`
        namespace = ctx.params.get("namespace")
        if not namespace:
            namespace = c.project
        
        # We're completing something like `oc get pod/<tab>`.
        if "/" in incomplete:
            restypein = incomplete.split("/")[0]
            resname = incomplete.split("/")[1]
            resources = get_resources(restypein, '_all', namespace)
            return [ restypein + "/" + r['res']['metadata']['name']
                        for r in resources
                        if  r['res']['metadata']['name'].startswith(resname) 
                        and restypein + "/" + r['res']['metadata']['name'] not in objects]
        
        if ',' in incomplete or [ o for o in objects if ',' in o]:
            # This is a NOP like oc
            return []

        get_method, resource_list = parse.parse_get_resources(objects)

        # First arg after get, autocomplete type
        # or autocompleting after existing slash-notation arg
        if not objects or get_method == parse.Method.SLASH:
            if get_method == parse.Method.SLASH:
                add_slash = '/'
            else:
                add_slash = ''
            fullset = set(
                [t['type'] + add_slash for t in map]
                + [ a + add_slash for aliases in [ t['aliases'] for t in map ] for a in aliases ] )
            return [t for t in fullset if t.startswith(incomplete)]

        if get_method == parse.Method.PLAIN and len(resource_list) > 0:
            # Autocomplete resource names based on the type: oc get pod mypod1 mypod2
            restypein, _ = next(resource_list)
            resources = get_resources(restypein, '_all', namespace)
            return [r['res']['metadata']['name'] for r in resources
                    if  r['res']['metadata']['name'].startswith(incomplete)
                    and r['res']['metadata']['name'] not in objects ]
    except:
        # Swallow any exception
        return []
    # Catch all
    return []
