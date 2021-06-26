# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


# Simple out put with just name, podSelector and age
def networkpolicy_out(t, ns, res, output, show_type, show_labels):
    output_res = [[]]
    # header
    if ns == "_all":
        output_res[0].append("NAMESPACE")
    output_res[0].extend(["NAME", "POD-SELECTOR", "AGE"])
    # resources
    for r in res:
        p = r["res"]
        row = []
        # namespace (for --all-namespaces)
        if ns == "_all":
            row.append(p["metadata"]["namespace"])
        # name
        if show_type:
            row.append(t + "/" + p["metadata"]["name"])
        else:
            row.append(p["metadata"]["name"])
        # podSelector
        try:
            row.append(str(p["spec"]["podSelector"]))
        except:
            row.append("Unknown") 
        # age
        try:
            ct = str(p["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")       

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))
