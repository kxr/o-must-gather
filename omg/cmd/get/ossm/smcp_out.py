# -*- coding: utf-8 -*-
from dateutil.parser import parse
from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output SMCP or ServiceMeshControlPlane resource
# We will create an array of array and then print if with tabulate
def smcp_out(t, ns, res, output, show_type, show_labels):
    output_smcp = [[]]
    # header
    if ns == "_all":
        output_smcp[0].append("NAMESPACE")
        output_smcp[0].extend(["NAME", "READY", "STATUS", "PROFILES", "VERSION", "AGE" ])
    else: 
        output_smcp[0].extend(["NAME", "READY", "STATUS", "PROFILES", "VERSION", "AGE" ])
    # SMCP
    for s in res:
        smcp = s["res"]
        row = []
        # namespace (for --all-namespaces from all SMCP(s))
        if ns == "_all":
            row.append(smcp["metadata"]["namespace"])

        # Print the SMCP-name
        if show_type:
            row.append(t + "/" + smcp["metadata"]["name"])
        else:
            row.append(smcp["metadata"]["name"])
       
        # Print the current SMCP ready components.  
        row.append(smcp["status"]["annotations"]["readyComponentCount"])

        # Print the current SMCP status.
        # Output the whole conditions in status list.
        status = smcp["status"]["conditions"]

        # compr & compnr variable to traverse through the status list and extract ["reason"] if the ["message"] condition matches.
        compr = ''
        compnr = ''
        for message in status:
            if message["message"] == "All component deployments are Available" and message["type"] == "Ready" and message["status"] == "True":
                compr = (message["reason"])
                row.append(compr)
            elif message["status"] == "False":
                compnr = (message["reason"])
                row.append(compnr)
        # SMCP Profiles
        row.append(smcp["spec"]["profiles"])
       
        # SMCP Version
        row.append(smcp["status"]["chartVersion"])

        # SMCP Age
        try:
            ct = str(smcp["metadata"]["creationTimestamp"])
            ts = s["gen_ts"]
            row.append(age(ct, ts))
        except:
            row.append("Unknown")

        output_smcp.append(row)
          
    print(tabulate(output_smcp, tablefmt="plain"))