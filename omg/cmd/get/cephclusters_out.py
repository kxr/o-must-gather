# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age, extract_labels


def cephclusters_out(t, ns, res, output, show_type, show_labels):
    output_res = [[]]
    # header
    if ns == "_all":
        output_res[0].append("NAMESPACE")
    if show_labels:
        output_res[0].extend(["NAME", "DATADIRHOSTPATH", "MONCOUNT", "AGE","PHASE" , "MESSAGE", "HEALTH", "LABELS"])
    else:
        output_res[0].extend(["NAME", "DATADIRHOSTPATH", "MONCOUNT", "AGE","PHASE" , "MESSAGE", "HEALTH"])

    # resources
    for r in res:
        cs = r["res"]
        row = []
        # namespace (for --all-namespaces)
        if ns == "_all":
            row.append(cs["metadata"]["namespace"])
        # name
        if show_type:
            row.append(t + "/" + cs["metadata"]["name"])
        else:
            row.append(cs["metadata"]["name"])
        # dataDirHostPath
        row.append(cs["spec"]["dataDirHostPath"])
        # mon.count
        row.append(cs["spec"]["mon"]["count"])
        # age
        try:
            ct = str(cs["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")
        # phase
        row.append(cs["status"]["phase"])
        # message
        row.append(cs["status"]["message"])
        # health
        row.append(cs["status"]["ceph"]["health"])

        if show_labels:
            row.append(extract_labels(cs))

        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))
