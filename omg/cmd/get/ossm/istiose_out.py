from dateutil.parser import parse
from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output Istio ServiceEntry-Configuration resource.
# We will create an array of array and then print if with tabulate
def istiose_out(t, ns, res, output, show_type, show_labels):
    output_se = [[]]
    # header
    if ns == "_all":
        output_se[0].append("NAMESPACE")
        output_se[0].extend(["NAME", "HOSTS", "LOCATION", "RESOLUTION", "AGE"])
    else:
        output_se[0].extend(["NAME", "HOSTS", "LOCATION", "RESOLUTION", "AGE"])
    # ServiceEntry
    for s in res:
        se = s["res"]
        row = []
        # namespace (for --all-namespaces from all ServiceEntry(s))
        if ns == "_all":
            row.append(se["metadata"]["namespace"])

        # Print the serviceentry-name
        if show_type:
            row.append(t + "/" + se["metadata"]["name"])
        else:
            row.append(se["metadata"]["name"])

        # Print the ServiceEntry-host
        row.append(se["spec"]["hosts"])

        # Print the ServiceEntry-location
        row.append(se["spec"]["location"])

        # Print the ServiceEntry-resolution
        row.append(se["spec"]["resolution"])

        # ServiceEntry Age
        try:
            ct = str(se["metadata"]["creationTimestamp"])
            ts = s["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_se.append(row)

    print(tabulate(output_se, tablefmt="plain"))
