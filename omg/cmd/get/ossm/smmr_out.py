# -*- coding: utf-8 -*-
from tabulate import tabulate

from omg.common.helper import age, extract_labels


# Special function to output SMMR or Service Mesh Member Roll resource
# We will create an array of array and then print if with tabulate
def smmr_out(t, ns, res, output, show_type, show_labels):
    output_smmr = [[]]
    # header
    if ns == "_all":
        output_smmr[0].append("NAMESPACE")
        output_smmr[0].extend(["NAME", "READY", "STATUS", "AGE"])
    else:
        output_smmr[0].extend(["NAME", "READY", "STATUS",  "AGE"])
    # SMMR
    for s in res:
        smmr = s["res"]
        row = []
        # namespace (for --all-namespaces from all SMMR(s))
        if ns == "_all":
            row.append(smmr["metadata"]["namespace"])

        # Print the SMMR-name
        if show_type:
            row.append(t + "/" + smmr["metadata"]["name"])
        else:
            row.append(smmr["metadata"]["name"])

        # Print the current SMMR ready components.
        row.append(smmr["status"]["annotations"]["configuredMemberCount"])

        # Print the current SMMR status.
        # Output the current conditions in status list.
        status = smmr["status"]["conditions"]

        for st in status:
            row.append(st["reason"])

        # SMCP Age
        try:
            ct = str(smmr["metadata"]["creationTimestamp"])
            ts = s["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_smmr.append(row)

    print(tabulate(output_smmr, tablefmt="plain"))
