class NoValidMgFound(Exception):
    """
    Error raised when no valid must-gather directory is found
    """
    pass


class NameSpaceRequired(Exception):
    """
    Error raised when no must-gather is selected
    """
    pass


class UnkownResourceType(Exception):
    """
    Error raised when rdef for resource type is not found
    """
    pass


class InvalidResource(Exception):
    """
    Error raised when a loaded resource is invalid
    """
    pass


class NamespaceDirWithoutYaml(Exception):
    """
    Error raised namespace directory is present without its yaml
    """
    pass
