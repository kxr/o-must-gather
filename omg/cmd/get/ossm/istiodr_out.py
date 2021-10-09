from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output Istio DestinationRules-Configuration resource.
# We will create an array of array and then print if with tabulate
def istiodr_out(t, ns, res, output, show_type, show_labels):
    output_dr = [[]]
    # header
    if ns == "_all":
        output_dr[0].append("NAMESPACE")
        output_dr[0].extend(["NAME", "HOST" "AGE"])
    else:
        output_dr[0].extend(["NAME", "HOST", "AGE"])
    # DestinationRule
    for d in res:
        dr = d["res"]
        row = []
        # namespace (for --all-namespaces from all destinationRule(s))
        if ns == "_all":
            row.append(dr["metadata"]["namespace"])

        # Print the destinationrule-name
        if show_type:
            row.append(t + "/" + dr["metadata"]["name"])
        else:
            row.append(dr["metadata"]["name"])

        # Print the DestinationRule-host
        row.append(dr["spec"]["host"])

        # DestinationRule Age
        try:
            ct = str(dr["metadata"]["creationTimestamp"])
            ts = d["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_dr.append(row)

    print(tabulate(output_dr, tablefmt="plain"))
