from dateutil.parser import parse
from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output Istio Sidecar-Configuration resource.
# We will create an array of array and then print if with tabulate
def istiosidecar_out(t, ns, res, output, show_type, show_labels):
    output_s = [[]]
    # header
    if ns == "_all":
        output_s[0].append("NAMESPACE")
        output_s[0].extend(["NAME", "AGE"])
    else:
        output_s[0].extend(["NAME", "AGE"])
    # Gateway
    for s in res:
        sidecar = s["res"]
        row = []
        # namespace (for --all-namespaces from all Sidecar(s))
        if ns == "_all":
            row.append(sidecar["metadata"]["namespace"])

        # Print the Sidecar-name
        if show_type:
            row.append(t + "/" + sidecar["metadata"]["name"])
        else:
            row.append(sidecar["metadata"]["name"])

        # Gateway Age
        try:
            ct = str(sidecar["metadata"]["creationTimestamp"])
            ts = s["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_s.append(row)

    print(tabulate(output_s, tablefmt="plain"))
