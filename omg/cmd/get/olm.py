# -*- coding: utf-8 -*-
from tabulate import tabulate
from omg.common.helper import age, extract_labels


def opcsv_out(*args):
    """
    Operator ClusterServiceVersions parser.

    # Positional args #:
    # 0: t
    # 1: ns
    # 2: res
    # 3: output
    # 4: show_type
    # 5: show_labels
    """
    ns = args[1]
    show_labels = args[5]

    output_res = [[]]
    if ns == "_all": # ns
        output_res[0].append("NAMESPACE")

    output_res[0].extend([
        "NAME",
        "DISPLAY",
        "VERSION",
        "REPLACES",
        "PHASE"
    ])
    if show_labels: # show_labels
        output_res[0].extend(["LABELS"])

    for r in args[2]: # resource
        rs = r["res"]
        row = []

        if ns == "_all":
            row.append(rs["metadata"]["namespace"])

        row.append(rs["metadata"]["name"])
        row.append(rs["spec"]["displayName"])
        row.append(rs["spec"]["version"])
        try:
            row.append(rs["spec"]["replaces"])
        except KeyError:
            row.append('')
        row.append(rs["status"]["phase"])

        if show_labels:
            row.append(extract_labels(rs))

        output_res.append(row)
    print(tabulate(output_res, tablefmt="plain"))


def opip_out(*args):
    print("WIP")


def op_out(*args):
    print("WIP")


def opcatsrc_out(*args):
    print("WIP")


def opgrp_out(*args):
    print("WIP")


def opsub_out(*args):
    print("WIP")

