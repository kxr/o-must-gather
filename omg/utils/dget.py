def dget(_dict, keys, default=None):
    """Safely get key values from nested dictionary

    Args:
        _dict (dict): Dictionary to get the key from
        keys (list): Iterable list of keys to get
        default (any optional): Value to return if key is missing. Defaults to None.

    Returns:
        any: Value found at the key or the default value if key is not found
    """
    for key in keys:
        if isinstance(_dict, dict):
            _dict = _dict.get(key, default)
        else:
            return default
    return _dict
