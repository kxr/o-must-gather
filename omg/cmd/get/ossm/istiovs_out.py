from dateutil.parser import parse
from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output Istio VirtualServices-Configuration resource.
# We will create an array of array and then print if with tabulate
def istiovs_out(t, ns, res, output, show_type, show_labels):
    output_vs = [[]]
    # header
    if ns == "_all":
        print ("This feature is in works")
        print ("Use 'omg get vs -n <namespace-name>'")
        quit()
        #output_vs[0].append("NAMESPACE")
        #output_vs[0].extend(["NAME", "GATEWAYS", "HOSTS", "AGE"])
    else:
        output_vs[0].extend(["NAME", "GATEWAYS", "HOSTS", "AGE"])
    # VirtualServices
    for v in res:
        vs = v["res"]
        row = []
        # namespace (for --all-namespaces from all virtualservices(s))
        if ns == "_all":
            row.append(vs["metadata"]["namespace"])

        # Print the virtualservice-name
        if show_type:
            row.append(t + "/" + vs["metadata"]["name"])
        else:
            row.append(vs["metadata"]["name"])

        # Print the VirtualService Gateways:
        row.append(vs["spec"]["gateways"])

        # Print the VirtualService Hosts:
        row.append(vs["spec"]["hosts"])

        # VirtualService Age
        try:
            ct = str(vs["metadata"]["creationTimestamp"])
            ts = v["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_vs.append(row)

    print(tabulate(output_vs, tablefmt="plain"))
