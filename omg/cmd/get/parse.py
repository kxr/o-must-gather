import enum

from omg.common.resource_map import map_res, map


ALL_RESOURCES = "_all"
ALL_TYPES = ['pod', 'rc', 'svc', 'ds', 'deployment', 'rs', 'statefulset', 'hpa', 'job', 'cronjob', 'dc', 'bc', 'build',
             'is']


class ResourceMap:
    """
    Wrapper around a dictionary that contains type->set<Resource>.
    """
    def __init__(self):
        self.dict = {}

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


class Method(enum.Enum):
    """
    Enumeration of various methods `omg get` can be called.
    """
    UNKNOWN = 0  # ¯\_(ツ)_/¯
    SINGLE_TYPE = 1  # e.g. omg get pod/mypod
    MULTI_TYPE_SINGLE_RESOURCE = 2  # e.g. omg get svc,ep,ds dns-default
    MULTI_TYPE_MULTI_RESOURCE = 3  # e.g. omg get pod mypod myotherpod
    ALL = 4  # e.g. oc get all


class ResourceParseError(Exception):
    """
    Error raised during parsing of `oc get` args.
    """
    pass


class ResourceList:
    def __init__(self, objects: tuple):
        """
        Takes a tuple (examples below) of arguments passed to `omg get ...` and parses it into
        manageable class.

        objects: Tuple of arguments passed to `omg get ...`

        Example object contents:
        ('pod', 'httpd')
        ('pods', 'httpd1', 'httpd2')
        ('dc/httpd', 'pod/httpd1')
        ('routes')
        ('pod,svc')
        """

        self._objects = objects
        self.get_method: Method = Method.UNKNOWN
        self._resources = ResourceMap()
        self._num = 0
        self.__res_generator = None

        self._parse()

    def is_multitype(self):
        return len(self._resources.get_types()) > 1

    def _parse_slash(self, arg):
        """
        Parses out a single word containing a slash, validates the type is known and returns: type name, resource name
        """
        try:
            o_split = arg.split('/')
            r_type = o_split[0]
            r_name = o_split[1]
            checked_type = map_res(r_type)
            if r_type is None:
                raise ResourceParseError("[ERROR] Invalid object type: " + r_type)
            return checked_type['type'], r_name
        except Exception:
            raise ResourceParseError("[ERROR] Invalid object type: " + arg)

    def _parse(self):
        """
        The meat of parsing for the omg get command. Parses the arguments (omg get ...) into a ResourceMap.

        Raises ResourceParseError if it runs into any issues.
        """
        if len(self._objects) == 0:
            # We've nothing to parse right now.
            return

        last_object = []

        # Check first arg to see if we're doing multiple or single resources
        first = self._objects[0]
        if '/' in first:
            self.get_method = Method.MULTI_TYPE_MULTI_RESOURCE
        elif ',' in first:
            self.get_method = Method.MULTI_TYPE_SINGLE_RESOURCE
        else:
            self.get_method = Method.SINGLE_TYPE

        for o in self._objects:
            if '/' in o:
                r_type, r_name = self._parse_slash(o)
                self._resources.add_resource(r_type, r_name)
            elif ',' in o:
                pass
            else:
                pass

        for o in self._objects:
            # Case where we have a '/'
            # e.g omg get pod/httpd
            if '/' in o:
                self.get_method = Method.MULTI_TYPE_MULTI_RESOURCE
                if not last_object:
                    pre = o.split('/')[0]
                    r_type = map_res(pre)['type']
                    r_name = o.split('/')[1]
                    # If its a valid resource type, append it to objects
                    if r_type is not None:
                        self._resources.add_resource(r_type, r_name)
                    else:
                        raise ResourceParseError("[ERROR] Invalid object type: " + pre)

            # Convert 'all' to list of resource types in a specific order
            elif o == 'all':
                for rt in ALL_TYPES:
                    # TODO Simplify to just: last_object.append(rt)?
                    check_rt = map_res(rt)
                    if check_rt is None:
                        raise ResourceParseError("[ERROR] Invalid object type: " + rt)
                    else:
                        last_object.append(check_rt['type'])

            # Case where we have a ',' e.g `get dc,svc,pod httpd`
            # These all will be resource_types, not names,
            # resource_name will come it next iteration (if any)
            elif ',' in o:
                self.get_method = Method.MULTI_TYPE_SINGLE_RESOURCE
                if not last_object:
                    r_types = o.split(',')
                    # if all is present, we will replace it with all_types
                    if 'all' in r_types:
                        ai = r_types.index('all')
                        r_types.remove('all')
                        r_types[ai:ai] = ALL_TYPES
                    for rt in r_types:
                        check_rt = map_res(rt)
                        if check_rt is None:
                            raise ResourceParseError("[ERROR] Invalid object type: " + rt)
                        else:
                            last_object.append(check_rt['type'])
                else:
                    # last_object was set, meaning this should be object name
                    raise ResourceParseError("[ERROR] Invalid resources to get: " + self.objects)

            # Simple word (without , or /)
            # If last_object was not set, means this is a resource_type
            elif not last_object:
                self.get_method = Method.SINGLE_TYPE
                check_rt = map_res(o)
                if check_rt is not None:
                    last_object = [check_rt['type']]
                else:
                    raise ResourceParseError("[ERROR] Invalid resource type to get: " + o)
            # Simple word (without , or /)
            # If the last_object was set, means we got resource_type last time,
            # and this should be a resource_name.
            elif last_object:
                self.get_method = Method.SINGLE_TYPE
                for rt in last_object:
                    self._resources.add_resource(rt, o)
            else:
                # Should never happen
                raise ResourceParseError("[ERROR] Invalid resources to get: " + o)

        if last_object:
            for rt in last_object:
                check_rt = map_res(rt)
                if check_rt is None:
                    continue
                r_type = check_rt['type']
                if not self._resources.has_type(r_type) or len(self._resources.get_resources(r_type)) == 0:
                    self.get_method = Method.ALL
                    self._resources.add_resource(r_type, ALL_RESOURCES)

    def __iter__(self):
        """
        Initialize iterator from ResourceMap generator
        """
        self.__res_generator = self._resources.generator()
        return self

    def __next__(self):
        """
        Pull next item from ResourceMap generator.
        """
        if self.__res_generator is None:
            self.__iter__()
        r_type, r_name = next(self.__res_generator)
        return r_type, r_name

    def __contains__(self, item):
        """
        Check if given resource type exists.
        """
        res = map_res(item)
        if res is not None:
            return self._resources.has_type(res['type'])

    def __len__(self):
        """
        Length of ResourceMap.
        """
        return len(self._resources.dict)