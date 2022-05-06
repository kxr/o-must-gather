# This module handles parsing of the omg's `get` command
# i.e, it normalizes whatever is passed after `omg get <....>`
# Since omg get can be called in a variety of ways, following is a
# detailed description of all the "varities" omg will handle:
#
# 1- SLASH Notation
#   Syntax:
#       omg get Type1/Name1 [Type2/Name2 Type3/Name3 ....]
#   Examples:
#       - omg get pod/httpd-sdf32
#       - omg get svc/httpd route/httpd
#
# 2- COMMA Notation
#   Syntax:
#       omg get Type1,Type2[,Type3,...] [Name1 Name2 ...]
#   Examples:
#       - omg get pods,svc
#       - omg get svc,route,deployment httpd nginx
#
# 3- PLAIN
#   Syntax:
#       omg get Type [Name1 Name2 Name3]
#   Examples:
#       - omg get pods
#       - omg get nodes node1 node2
#       - omg get all
#
# Note:
#   Any get request can fall into either one of these syntaxes
#   A mix of these types will not be supported


# What resources to show when `omg get all` is called
ALL_TYPES = ['pod', 'rc', 'svc', 'ds', 'deployment',
             'rs', 'statefulset', 'hpa', 'job', 'cronjob',
             'dc', 'bc', 'build.build.openshift.io', 'is']


class ParseError(Exception):
    """
    Error raised during parsing of `oc get` args.
    """
    pass


def _parse_slash(args):
    """
    Parses slash based get args
    """
    objects = []
    for arg in args:
        if '/' not in arg:
            raise ParseError("Invalid arguments to get")
        o_split = arg.split('/')
        r_type = o_split[0]
        r_name = o_split[1]
        objects.append((r_type, r_name))
    return objects


def _parse_comma(args):
    """
    Parses comma based get args
    """
    objects = []
    # The first arg contains comma sperated types
    first = args[0]
    types = first.split(",")
    if 'all' in types:
        types.extend(ALL_TYPES)
        types.remove("all")

    # If more than one args are present these are names of objects to get
    if len(args) > 1:
        names = args[1:]
    else:
        names = []

    for t in types:
        if names:
            for n in names:
                objects.append((t, n))
        else:
            objects.append((t, []))

    return objects


def _parse_plain(args):
    """
    Parses plain get args (e.g, without comma or slash)
    """
    objects = []
    # The first arg should be the type
    first = args[0]
    if first == 'all':
        types = tuple(ALL_TYPES)
    else:
        types = (first,)

    # If more than one args are present these are names of objects to get
    if len(args) > 1:
        # names are not allowed with "all"
        if first == 'all':
            raise ParseError("Resource names not allowed with 'all'")
        names = args[1:]
    else:
        names = []

    for t in types:
        if names:
            for n in names:
                objects.append((t, n))
        else:
            objects.append((t, None))

    return objects


def parse_get_args(objects):
    """
    Takes a tuple (examples below) of arguments passed to `omg get ...` and parses it.
    Returns a dict (key: "resource type", value: list("resource names")).

    Raises ResourceParseError if it runs into any issues.

    Example input -> output:
    ('pod', 'httpd')                -> {'pod': ['httpd']}
    ('pods', 'httpd1', 'httpd2')    -> {'pod': ['httpd1', 'httpd2']}
    ('dc/httpd', 'pod/httpd1')      -> {'dc': ['httpd'], 'pod': ['httpd1']}
    ('routes')                      -> {'routes': []}
    ('pod,svc')                     -> {'pod': [], 'svc': []}
    ('svc,route','httpd','nginx')   -> {'svc': ['httpd', 'nginx'], 'route': ['httpd', 'nginx']}
    """

    parsed_resources = {}

    if not objects:
        raise ParseError("Empty arguments to get")

    # Determine the type of args from the first arg
    first = objects[0]
    if '/' in first:
        parsed_objects = _parse_slash(objects)
    elif ',' in first:
        parsed_objects = _parse_comma(objects)
    else:
        parsed_objects = _parse_plain(objects)

    for r_type, r_name in parsed_objects:
        if r_type not in parsed_resources:
            parsed_resources[r_type] = []
        if r_name:
            parsed_resources[r_type].append(r_name)

    return parsed_resources
