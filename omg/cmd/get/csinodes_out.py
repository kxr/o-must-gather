# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


def csinodes_out(t, ns, res, output, show_type, show_labels):
    output_res = []
    # header
    if show_labels:
        header = [
            "NAME",
            "DRIVERS",
            "AGE",
            "LABELS",
        ]
    else:
        header = [
            "NAME",
            "DRIVERS",
            "AGE",
        ]
    # resources
    for r in res:
        cn = r["res"]
        row = []
        # name
        if show_type:
            row.append(t + "/" + cn["metadata"]["name"])
        else:
            row.append(cn["metadata"]["name"])
        # drivers
        try:
            row.append(len(cn["spec"]["drivers"]))
        except:
            row.append("0")
        # age
        try:
            ct = str(cn["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_res.append(row)

    # sort by 1st column
    sorted_output = sorted(output_res)
    sorted_output.insert(0, header)
    print(tabulate(sorted_output, tablefmt="plain"))
