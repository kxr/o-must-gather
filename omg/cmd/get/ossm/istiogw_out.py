from dateutil.parser import parse
from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output Istio Gateway-Configuration resource.
# We will create an array of array and then print if with tabulate
def istiogw_out(t, ns, res, output, show_type, show_labels):
    output_gw = [[]]
    # header
    if ns == "_all":
        output_gw[0].append("NAMESPACE")
        output_gw[0].extend(["NAME", "AGE"])
    else:
        output_gw[0].extend(["NAME", "AGE"])
    # Gateway
    for g in res:
        gw = g["res"]
        row = []
        # namespace (for --all-namespaces from all gateway(s))
        if ns == "_all":
            row.append(gw["metadata"]["namespace"])

        # Print the gateway-name
        if show_type:
            row.append(t + "/" + gw["metadata"]["name"])
        else:
            row.append(gw["metadata"]["name"])

        # Gateway Age
        try:
            ct = str(gw["metadata"]["creationTimestamp"])
            ts = g["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_gw.append(row)

    print(tabulate(output_gw, tablefmt="plain"))
