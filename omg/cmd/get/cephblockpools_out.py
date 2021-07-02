# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age, extract_labels


def cephblockpools_out(t, ns, res, output, show_type, show_labels):
    output_res = [[]]
    # header
    if ns == "_all":
        output_res[0].append("NAMESPACE")
    if show_labels:
        output_res[0].extend(["NAME", "AGE", "LABELS"])
    else:
        output_res[0].extend(["NAME", "AGE"])

    # resources
    for r in res:
        cf = r["res"]
        row = []
        # namespace (for --all-namespaces)
        if ns == "_all":
            row.append(cf["metadata"]["namespace"])
        # name
        if show_type:
            row.append(t + "/" + cf["metadata"]["name"])
        else:
            row.append(cf["metadata"]["name"])
        # age
        try:
            ct = str(cf["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        if show_labels:
            row.append(extract_labels(cf))

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))
