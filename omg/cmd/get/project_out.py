from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Special function to output project
# We will create an array of array and then print if with tabulate
def project_out(t, ns, res, output, show_type, show_labels):
    output_projects=[[]]
    # header
    if show_labels:
        output_projects[0].extend(['NAME','DISPLAY NAME','STATUS','LABELS'])
    else:
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

        # show-labels
        if show_labels:
            row.append(extract_labels(p))
        
        output_projects.append(row)

    print(tabulate(output_projects,tablefmt="plain"))
