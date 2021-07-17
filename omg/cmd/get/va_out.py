# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


def va_out(t, ns, res, output, show_type, show_labels):
    output_res = []
    # header
    if show_labels:
        header = [
            "NAME",
            "ATTACHER",
            "PV",
            "NODE",
            "ATTACHED",
            "AGE",
            "LABELS",
        ]
    else:
        header = [
            "NAME",
            "ATTACHER",
            "PV",
            "NODE",
            "ATTACHED",
            "AGE",
        ]
    # resources
    for r in res:
        va = r["res"]
        row = []
        # name
        if show_type:
            row.append(t + "/" + va["metadata"]["name"])
        else:
            row.append(va["metadata"]["name"])
        # attacher
        row.append(va["spec"]["attacher"])
        # pv
        row.append(va["spec"]["source"]["persistentVolumeName"])
        # node
        row.append(va["spec"]["nodeName"])
        # attached
        row.append(va["status"]["attached"])
        # age
        try:
            ct = str(va["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_res.append(row)

    # sort by 1st column
    sorted_output = sorted(output_res)
    sorted_output.insert(0, header)
    print(tabulate(sorted_output, tablefmt="plain"))
