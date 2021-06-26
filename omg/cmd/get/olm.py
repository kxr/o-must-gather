# -*- coding: utf-8 -*-
from tabulate import tabulate
from omg.common.helper import age, extract_labels


def _build_output_res(*args, fields=[]):
    """
    Build common output response header.

    Helper to positional args #:
    0: t
    1: ns
    2: res
    3: output
    4: show_type
    5: show_labels
    """
    ns = args[1]
    show_labels = args[5]

    output_res = [[]]
    if ns == "_all": # ns
        output_res[0].append("NAMESPACE")

    output_res[0].extend(fields)

    if show_labels: # show_labels
        output_res[0].extend(["LABELS"])

    return output_res


def opcsv_out(*args):
    """
    Operator ClusterServiceVersions parser.
    """
    ns = args[1]
    show_labels = args[5]

    output_res = _build_output_res(*args, fields=[
        "NAME",
        "DISPLAY",
        "VERSION",
        "REPLACES",
        "PHASE"
    ])

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
    """
    Operator InstallPlans parser.
    """
    ns = args[1]
    show_labels = args[5]

    output_res = _build_output_res(*args, fields=[
        "NAME",
        "CSV",
        "APPROVAL",
        "APPROVED"
    ])

    for r in args[2]: # resource
        rs = r["res"]

        # If there's more than on CSV on this IP, duplicate the row.
        # TODO check if that is same behavior of CLI.
        for csv_name in rs["spec"]["clusterServiceVersionNames"]:
            row = []

            if ns == "_all":
                row.append(rs["metadata"]["namespace"])

            row.append(rs["metadata"]["name"])
            row.append(csv_name)
            row.append(rs["spec"]["approval"])
            row.append(rs["spec"]["approved"])

            if show_labels:
                row.append(extract_labels(rs))

            output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))


def opcatsrc_out(*args):
    """
    Operator CatalogSources parser.
    """
    ns = args[1]
    show_labels = args[5]

    output_res = _build_output_res(*args, fields=[
        "NAME",
        "DISPLAY",
        "TYPE",
        "PUBLISHER",
        "AGE"
    ])

    for r in args[2]: # resource
        rs = r["res"]
        row = []

        if ns == "_all":
            row.append(rs["metadata"]["namespace"])

        row.append(rs["metadata"]["name"])
        row.append(rs["spec"]["displayName"])
        row.append(rs["spec"]["sourceType"])
        row.append(rs["spec"]["publisher"])
        row.append(age(rs["metadata"]["creationTimestamp"], r["gen_ts"]))

        if show_labels:
            row.append(extract_labels(rs))

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))


def opgrp_out(*args):
    """
    Operator OperatorGroups parser.
    """
    ns = args[1]
    show_labels = args[5]

    output_res = _build_output_res(*args, fields=[
        "NAME",
        "AGE"
    ])

    for r in args[2]: # resource
        rs = r["res"]
        row = []

        if ns == "_all":
            row.append(rs["metadata"]["namespace"])

        row.append(rs["metadata"]["name"])
        row.append(age(rs["metadata"]["creationTimestamp"], r["gen_ts"]))

        if show_labels:
            row.append(extract_labels(rs))

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))


def opsub_out(*args):
    """
    Operator Subscriptions parser.
    """
    ns = args[1]
    show_labels = args[5]

    output_res = _build_output_res(*args, fields=[
        "NAME",
        "PACKAGE",
        "SOURCE",
        "CHANNEL"
    ])

    for r in args[2]: # resource
        rs = r["res"]
        row = []

        if ns == "_all":
            row.append(rs["metadata"]["namespace"])

        row.append(rs["metadata"]["name"])
        row.append(rs["spec"]["name"])
        row.append(rs["spec"]["source"])
        row.append(rs["spec"]["channel"])

        if show_labels:
            row.append(extract_labels(rs))

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))
