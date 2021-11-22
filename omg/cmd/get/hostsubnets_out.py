# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


def hostsubnets_out(t, ns, res, output, show_type, show_labels):
    output_res = [[]]
    # header
    output_res[0].extend(["NAME", "HOST", "HOST IP", "SUBNET", "EGRESS CIDRS", "EGRESS IPS"])
    # resources
    for r in res:
        h = r["res"]
        row = []
        # name
        if show_type:
            row.append(t + "/" + h["metadata"]["name"])
        else:
            row.append(h["metadata"]["name"])
        # netid
        try:
            row.append(str(h["host"]))
        except:
            row.append("Unknown")
        # hostIP
        try:
            row.append(str(h["hostIP"]))
        except:
            row.append("Unknown")
        # subnet
        try:
            row.append(str(h["subnet"]))
        except:
            row.append("Unknown")
        # egressCIDRs
        try:
            row.append(str(h["egressCIDRs"]))
        except:
            row.append("")
        # egressIPs
        try:
            row.append(str(h["egressIPs"]))
        except:
            row.append("")

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))
