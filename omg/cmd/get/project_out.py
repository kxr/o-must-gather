from tabulate import tabulate

from omg.common.helper import age

# Special function to output project
# We will create an array of array and then print if with tabulate
def project_out(t, ns, res, output, show_type):
    output_projects=[[]]
    # header
    output_projects[0].extend(['NAME','DISPLAY NAME','STATUS'])
    # project
    for project in res:
        p = project['res']
        row = []
        # name
        row.append(p['metadata']['name'])
        # display name
        if 'openshift.io/display-name' in p['metadata']['annotations']:
            display_name = p['metadata']['annotations']['openshift.io/display-name']
        else:
            display_name = ''
        row.append(display_name)
        # status
        row.append(p['status']['phase'])
        
        output_projects.append(row)

    print(tabulate(output_projects,tablefmt="plain"))
