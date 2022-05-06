def extract_labels(obj):
    """Receives an object/resource and returns the labels in flat/string format.
    Helper function to print labels when --show-labels is passed

    Args:
        o (dict): object

    Returns:
        str: Labels in plain string e.g: "app=console,component=ui"
             Returns '<none>' if 'labels' is absent in object -> metadata

    """
    if "labels" in obj["metadata"]:
        try:
            lab = obj["metadata"]["labels"]
            l_str = ",".join(["%s=%s" % (k, v) for k, v in lab.items()])
            return l_str
        except Exception:
            return "<error parsing labels>"
    else:
        return "<none>"
