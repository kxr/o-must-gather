# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age, extract_labels


def cephobjectstoreusers_out(t, ns, res, output, show_type, show_labels):
    output_res = [[]]
    # header
    header = []
    if ns == "_all":
        output_res[0].append("NAMESPACE")
    if show_labels:
        output_res[0].extend(["NAME", "AGE", "LABELS"])
    else:
        output_res[0].extend(["NAME", "AGE"])
        
    # resources
    for r in res:
        co = r["res"]
        row = []
        # namespace (for --all-namespaces)
        if ns == "_all":
            row.append(co["metadata"]["namespace"])
        # name
        if show_type:
            row.append(t + "/" + co["metadata"]["name"])
        else:
            row.append(co["metadata"]["name"])
        # age
        try:
            ct = str(co["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        if show_labels:
            row.append(extract_labels(co))

        output_res.append(row)

    # sort by NAME column whose index will be
    # 1 if we are showing namespaces otherwise 0
    ni = 1 if ns == "_all" else 0
    sorted_output = sorted(output_res, key=lambda x: x[ni])
    sorted_output.insert(0, header)

    print(tabulate(sorted_output, tablefmt="plain"))
