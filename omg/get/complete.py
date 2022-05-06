from omg.must_gather.RDEFS import RDEFS
from omg.must_gather.get_rdef import get_generated_rdefs
from omg.get.get_resources import get_all_resource_names
from omg.get.parse import parse_get_args, ParseError
from omg.config import config
from omg.utils.dget import dget
from loguru import logger as lg


def _suggest_type(incomplete_type):
    """
    Match type based on incomplete string
    """
    all_rdefs = []
    all_rdefs.extend(RDEFS)
    all_rdefs.extend(get_generated_rdefs())

    all_types = set()
    for rdef in all_rdefs:
        singular = dget(rdef, ["singular"])
        plural = dget(rdef, ["plural"])
        # shortNames = dget(rdef, ["shortNames"])
        group = dget(rdef, ["group"])

        if group != "core":
            all_types.add(plural + "." + group)
        else:
            all_types.add(singular)
            all_types.add(plural)
            # if shortNames:
            #     all_types.update(shortNames)

    match = [f for f in all_types if f.startswith(incomplete_type)]
    return match


def complete_get(ctx, args, incomplete):
    """
    Pull out objects args from Click context and return completions.
    """
    lg.remove()
    try:
        cfg = config.get()
        project = dget(cfg, ["project"])
        namespace = ctx.params.get("namespace") or project

        objects = ctx.params.get("objects")

        if "/" in incomplete:
            # We're completing something like `oc get pod/<tab>`.
            in_rtype = incomplete.split("/")[0]
            in_rname = incomplete.split("/")[1]
            names = get_all_resource_names({in_rtype: []}, namespace)
            return [
                in_rtype + "/" + n
                for n in names
                if n.startswith(in_rname) and in_rtype + "/" + n not in objects
            ]

        if "," in incomplete or [o for o in objects if "," in o]:
            # This is a NOP like oc
            return []

        slash_mode = False
        comma_mode = False
        if objects:
            try:
                parsed_objects = parse_get_args(objects)
            except ParseError:
                return []
            else:
                slash_mode = all("/" in o for o in objects)
                comma_mode = all("," in o for o in objects)

        # First arg after get, autocomplete type
        # or autocompleting after existing slash-notation arg
        if not objects or slash_mode:
            if slash_mode:
                add_slash = "/"
            else:
                add_slash = ""
            sugg = _suggest_type(incomplete)
            return [s + add_slash for s in sugg]

        if not slash_mode and not comma_mode and len(parsed_objects) > 0:
            # Autocomplete resource names based on the type: oc get pod mypod1 mypod2
            names = get_all_resource_names(parsed_objects, namespace)
            return [n for n in names if n.startswith(incomplete) and n not in objects]
        # Catch all
        return []

    except Exception:
        # Swallow any exception
        return []
