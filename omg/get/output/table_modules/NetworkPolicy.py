# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_pod_selector(res):
    selectors = []
    # matchExpressions
    me = dget(res, ["res", "spec", "podSelector", "matchExpressions"], [])
    for exp in me:
        selectors.append(
             "{} {} ({})".format(
                 dget(exp, ["key"]),
                 dget(exp, ["operator"]).lower(),
                 ",".join(dget(exp, ["values"], []))
             )
        )
    # matchLabels
    ml = dget(res, ["res", "spec", "podSelector", "matchLabels"], {})
    for k, v in ml.items():
        selectors.append("{}={}".format(k, v))

    if selectors:
        return ",".join(selectors)
    else:
        return "<none>"


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "POD-SELECTOR": _col_pod_selector,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
