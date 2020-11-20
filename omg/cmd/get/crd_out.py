from tabulate import tabulate

from omg.common.helper import age


# Simple out put with just name and age
def crd_out(t, ns, res, output, show_type):
    output_res=[]
    # header
    # we will append the header array at last after sorting
    header = ['NAME','CREATED AT']
    # resources
    for r in res:
        p = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + p['metadata']['name'])
        else:
            row.append(p['metadata']['name'])
        # creation timestamp
        try:
            row.append(p['metadata']['creationTimestamp'])
        except:
            row.append('Unknown')

        output_res.append(row)

    # sort by 1st column
    sorted_output = sorted(output_res)
    sorted_output.insert(0,header)

    print(tabulate(sorted_output,tablefmt="plain"))
