import enum

from omg.common.resource_map import map_res, map

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


ALL_RESOURCES = "_all"
ALL_TYPES = ['pod', 'rc', 'svc', 'ds', 'deployment', 'rs', 'statefulset', 'hpa', 'job', 'cronjob', 'dc', 'bc', 'build',
             'is']


class ResourceMap:
    """
    Wrapper around a dictionary that contains type->set<Resource>.
    """
    def __init__(self):
        self.dict = {}
        self.__res_generator = None

    def add_type(self, resource_type):
        """
        Add a resource type (e.g. pod, service, route) to inner dict.
        """
        if resource_type not in self.dict:
            self.dict[resource_type] = set()

    def add_resource(self, resource_type, resource_name):
        """
        Add resource name of given type to inner dict.
        """
        self.add_type(resource_type)
        self.dict[resource_type].add(resource_name)

    def has_type(self, resource_type):
        """
        Check if inner dict knows about given type.
        """
        return resource_type in self.dict

    def get_types(self):
        """
        Get a list of resource types.
        """
        return self.dict.keys()

    def get_resources(self, resource_type):
        """
        Get a set of resource names for given type or empty set if type is not known.
        """
        return self.dict.get(resource_type) or set()

    def generator(self):
        """
        Yields all resources types -> set<Resource>.
        """
        for r_type in self.get_types():
            yield r_type, self.get_resources(r_type)

    def __contains__(self, item):
        """
        Check if given resource type exists.
        """
        res = map_res(item)
        if res is not None:
            return self.has_type(res['type'])

    def __iter__(self):
        """
        Initialize iterator from ResourceMap generator
        """
        self.__res_generator = self.generator()
        return self

    def __next__(self):
        """
        Pull next item from ResourceMap generator.
        """
        if self.__res_generator is None:
            self.__iter__()
        r_type, r_name = next(self.__res_generator)
        return r_type, r_name

    def __len__(self):
        """
        Length of ResourceMap.
        """
        return len(self.dict)

    def __str__(self):
        return str(self.dict)


class Method(enum.Enum):
    """
    Enumeration of various methods `omg get` can be called.
    """
    UNKNOWN = 0  # ¯\_(ツ)_/¯
    SLASH = 1  # e.g. omg get pod/mypod
    COMMA = 2  # e.g. omg get svc,ep,ds dns-default
    PLAIN = 3  # e.g. omg get pod mypod myotherpod


class ResourceParseError(Exception):
    """
    Error raised during parsing of `oc get` args.
    """
    pass

def _validate_type(t):
    checked_type = map_res(t)
    if checked_type is None:
        raise ResourceParseError("[ERROR] Invalid object type: " + t)
    else:
        return checked_type['type']

def _parse_slash(args):
    """
    Parses slash based get args,
    validates the type is known and returns: [(type_name, resource_name)]
    """
    objects = []
    for arg in args:
        if '/' not in arg:
            raise ResourceParseError("[ERROR] Invalid arguments to get")
        o_split = arg.split('/')
        r_type = _validate_type(o_split[0])
        r_name = o_split[1]
        objects.append( (r_type, r_name) )
    return objects

def _parse_comma(args):
    """
    Parses comma based get args,
    validates the type is known and returns: [(type_name, resource_name)]
    """
    objects = []
    # The first arg contains comma sperated types
    first = args[0]
    t_split = first.split(',')
    if 'all' in t_split:
        t_split.extend(ALL_TYPES)
    types = tuple( _validate_type(t) for t in t_split if t != 'all' )

    # If more than one args are present these are names of objects to get
    if len(args) > 1:
        names = args[1:]
    else:
        names = (ALL_RESOURCES,)

    for t in types:
        for n in names:
            objects.append( (t,n) )

    return objects

def _parse_plain(args):
    """
    Parses plain get args (e.g, without comma or slash),
    validates the type is known and returns: [(type_name, resource_name)]
    """
    objects = []
    # The first arg should be the type
    first = args[0]
    if first == 'all':
        types = tuple( _validate_type(t) for t in ALL_TYPES )
    else:
        types = (_validate_type(first),)
    
    # If more than one args are present these are names of objects to get
    if len(args) > 1:
        # names are not allowed with "all"
        if first == 'all':
            raise ResourceParseError("[ERROR] Invalid arguments to get")
        names = args[1:]
    else:
        names = (ALL_RESOURCES,)

    for t in types:
        for n in names:
            objects.append( (t,n) )

    return objects


def parse_get_resources(objects: tuple) -> (Method, ResourceMap):
    """
    Takes a tuple (examples below) of arguments passed to `omg get ...` and parses it into
    manageable class. Returns a tuple containing the Method enum and resource mapping.

    Raises ResourceParseError if it runs into any issues.

    Example object contents:
    ('pod', 'httpd')
    ('pods', 'httpd1', 'httpd2')
    ('dc/httpd', 'pod/httpd1')
    ('routes')
    ('pod,svc')
    ('svc,route','httpd','nginx')
    """
    method = Method.UNKNOWN
    resources = ResourceMap()

    if len(objects) == 0:
        # We've nothing to parse right now.
        return method, resources

    # Determine the type of args from the first arg
    first = objects[0]
    if '/' in first:
        method = Method.SLASH
        parsed_objects = _parse_slash(objects)
    elif ',' in first:
        method = Method.COMMA
        parsed_objects = _parse_comma(objects)
    else:
        method = Method.PLAIN
        parsed_objects = _parse_plain(objects)

    for r_type,r_name in parsed_objects:
        resources.add_resource(r_type, r_name)

    return method, resources
