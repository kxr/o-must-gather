# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


def csr_out(t, ns, res, output, show_type, show_labels):
    output_res = []
    # header
    header = ["NAME", "AGE", "SIGNERNAME", "REQUESTOR", "CONDITION"]
    # resources
    for r in res:
        csr = r["res"]
        row = []
        # name
        if show_type:
            row.append(t + "/" + csr["metadata"]["name"])
        else:
            row.append(csr["metadata"]["name"])

        # age
        try:
            ct = str(csr["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")
        # signername
        signername = csr["spec"]["signerName"]
        row.append(signername)
        # requestor
        requestor = csr["spec"]["username"]
        row.append(requestor)
        # conditions
        condition = ""
        # empty status block means this request is still pending
        if csr.get("status", {}) == {}:
            condition = "Pending"
        else:
            conds = csr["status"]["conditions"]
            for c in conds:
                if c["type"] == "Approved":
                    condition = "Approved,Issued"
                elif c["type"] == "Denied":
                    condition = "Denied"
                elif c["type"] == "Failed":
                    condition = "Failed"
                else:
                    condition = "Unknown"

        row.append(condition)

        output_res.append(row)

    # print(tabulate(output_res,tablefmt="plain"))
    # sort by 1st column (name)
    sorted_output = sorted(output_res, key=lambda x: x[0])
    sorted_output.insert(0, header)

    print(tabulate(sorted_output, tablefmt="plain"))
