from click import Context

from omg.common.config import Config
from omg.cmd.get import parse
from omg.cmd.get_main import get_resource_names
from omg.common.resource_map import map, map_res

def complete_get(ctx: Context, args, incomplete):
    """
    Pull out objects args from Click context and return completions.
    """
    try:
        c = Config()
        objects = ctx.params.get("objects")
        # If user has set namespace ( with -n), we use that
        # else we use namespace set by `omg project`
        namespace = ctx.params.get("namespace") or c.project
        
        return generate_completions(objects, incomplete, namespace)
    except:
        # Swallow any exception
        return []

def _suggest_type(incomplete_type):
    """
    Smart matching for type/alias based on incomplete string
    Suggest one type if matched types and aliases belongs to the the same type
    e.g,:
        if incomplete = 'po' return ['po'] instead of ['po', 'pod', 'pods']
        if incomplete = 'ser' return ['service'] instead of ['service','services']
        but
        if incomplete = 'buil' return ['build','buildconfigs','builds','buildconfig']
    """
    fullset = set(
          [t['type'] for t in map]
        + [ a for aliases in [ t['aliases'] for t in map ] for a in aliases ] )
    
    match = [ f for f in fullset if f.startswith(incomplete_type) ]

    if len(match) > 1 and len(match) <= 3:
        unique_types = set( [ map_res(m)['type'] for m in match ] )
        if len(unique_types) == 1:
            return list(unique_types)
        else:
            return match
    else:
            return match


def generate_completions(objects, incomplete, namespace):
    # We're completing something like `oc get pod/<tab>`.
    if "/" in incomplete:
        restypein = incomplete.split("/")[0]
        resname = incomplete.split("/")[1]
        names = get_resource_names(restypein, '_all', namespace)
        return [ restypein + "/" + n
                    for n in names
                    if  n.startswith(resname) 
                    and restypein + "/" + n not in objects]
    
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
        sugg = _suggest_type(incomplete)
        return [ s + add_slash for s in sugg ]

    if get_method == parse.Method.PLAIN and len(resource_list) > 0:
        # Autocomplete resource names based on the type: oc get pod mypod1 mypod2
        restypein, _ = next(resource_list)
        names = get_resource_names(restypein, '_all', namespace)
        return [ n for n in names
                if  n.startswith(incomplete)
                and n not in objects ]
    # Catch all
    return []
