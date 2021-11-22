# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


def netnamespaces_out(t, ns, res, output, show_type, show_labels):
    output_res = [[]]
    # header
    output_res[0].extend(["NAME", "NETID", "EGRESS IPS"])
    # resources
    for r in res:
        n = r["res"]
        row = []
        # name
        if show_type:
            row.append(t + "/" + n["metadata"]["name"])
        else:
            row.append(n["metadata"]["name"])
        # netid
        try:
            row.append(str(n["netid"]))
        except:
            row.append("Unknown")
        # egressIPs
        try:
            row.append(str(n["egressIPs"]))
        except:
            row.append("")

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))
