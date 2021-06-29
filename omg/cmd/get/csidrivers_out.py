# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age


def csidrivers_out(t, ns, res, output, show_type, show_labels):
    output_res = []
    # header
    if show_labels:
        header = [
            "NAME",
            "ATTACHREQUIRED",
            "PODINFOONMOUNT",
            "MODES",
            "AGE",
            "LABELS",
        ]
    else:
        header = [
            "NAME",
            "ATTACHREQUIRED",
            "PODINFOONMOUNT",
            "MODES",
            "AGE",
        ]
    # resources
    for r in res:
        cd = r["res"]
        row = []
        # name
        if show_type:
            row.append(t + "/" + cd["metadata"]["name"])
        else:
            row.append(cd["metadata"]["name"])
        # attachRequired
        row.append(cd["spec"]["attachRequired"])
        # podInfoOnMount
        row.append(cd["spec"]["podInfoOnMount"])
        # volumeLifecycleModes
        row.append(cd["spec"]["volumeLifecycleModes"][0])
        # age
        try:
            ct = str(cd["metadata"]["creationTimestamp"])
            ts = r["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_res.append(row)

    # sort by 1st column
    sorted_output = sorted(output_res)
    sorted_output.insert(0, header)
    print(tabulate(sorted_output, tablefmt="plain"))
