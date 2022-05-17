from importlib import import_module
from loguru import logger as lg

from omg.utils.dget import dget
from omg.utils.age import age


def _col_ns(res):
    return dget(res, ["res", "metadata", "namespace"], "")


def _col_name(res):
    return dget(res, ["res", "metadata", "name"], "")


def _col_name_wtype(res):
    group = dget(res, ["rdef", "group"])
    singular = dget(res, ["rdef", "singular"])
    if group == "core":
        out_type = singular
    else:
        out_type = str(singular) + "." + str(group)
    name = dget(res, ["res", "metadata", "name"], "")
    return "{}/{}".format(out_type, name)


def _col_age(res):
    pod_ct = dget(res, ["res", "metadata", "creationTimestamp"])
    yfile_ts = dget(res, ["yfile_ts"])
    return age(pod_ct, yfile_ts)


def _col_labels(res):
    lab = dget(res, ["res", "metadata", "labels"])
    if lab:
        return ",".join(["{}={}".format(k, v) for k, v in lab.items()])
    else:
        return "<none>"


def build_table(res, ns, output, show_type, show_labels):
    lg.debug("FUNC_INIT: {}".format(locals()))

    rdef = dget(res[0], ["rdef"])

    # Get columns for the type of resources we are building table for
    # If we find the matching module in table_modules we will use that
    # Otherwise the default NAME and AGE columns will be used.
    kind = dget(rdef, ["kind"])
    try:
        table_mod = import_module("omg.get.output.table_modules.{}".format(kind))
        def_cols = table_mod.DEFAULT_COLUMNS
        wid_cols = table_mod.WIDE_COLUMNS
    except ModuleNotFoundError:
        def_cols = {
            "NAME": None,
            "AGE": None
        }
        wid_cols = {}
    pass

    # Header and respective header functions
    # We build the table header in header array and alongside,
    # populate the respective functions for that column in head_f array
    header = []
    head_f = []

    scope = dget(rdef, ["scope"])

    # Populate NAME/AGE in default column dict
    if dget(def_cols, ["NAME"], "") is None:
        if show_type:
            def_cols["NAME"] = _col_name_wtype
        else:
            def_cols["NAME"] = _col_name
    if dget(def_cols, ["AGE"], "") is None:
        def_cols["AGE"] = _col_age

    # Go over default/wide column dicts and populate
    # header and header_fn. Namespace and Labels are added
    # (first and last respectively) if needed
    if ns == "_all" and scope == "Namespaced":
        header.append("NAMESPACE")
        head_f.append(_col_ns)
    for hd, fn in def_cols.items():
        header.append(hd)
        head_f.append(fn)
    if output == "wide":
        for hd, fn in wid_cols.items():
            header.append(hd)
            head_f.append(fn)
    if show_labels:
        header.append("LABELS")
        head_f.append(_col_labels)

    # Iterate over resources and call the header function
    # to build the table body
    body = []
    for r in res:
        row = []
        for hf in head_f:
            try:
                row.append(hf(r))
            except Exception as e:
                lg.debug("table cell execption: {}".format(e))
                row.append("?Unknown?")
        body.append(row)

    return [header] + body
