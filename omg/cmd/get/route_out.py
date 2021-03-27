from tabulate import tabulate

from omg.common.helper import age, extract_labels


# Simple out put with just name and age
def route_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','HOST/PORT','PATH','SERVICES','PORT','TERMINATION','WILDCARD','LABELS'])
    else:
        output_res[0].extend(['NAME','HOST/PORT','PATH','SERVICES','PORT','TERMINATION','WILDCARD'])
    # resources
    for r in res:
        route = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(route['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + route['metadata']['name'])
        else:
            row.append(route['metadata']['name'])
        # host/port
        row.append(route['spec']['host'])
        # path
        if 'path' in route['spec']:
            row.append(route['spec']['path'])
        else:
            row.append('')
        # services
        try:
            svc = route['spec']['to']['name'] if route['spec']['to']['kind'] == 'Service' else '?'
            row.append(svc)
        except:
            row.append('??')
        # port
        try:
            port = route['spec']['port']['targetPort']
            row.append(port)
        except:
            row.append('??')
        # termination
        try:
            term = route['spec']['tls']
            term_str = ''
            if 'termination' in term:
                term_str += term['termination']
            if 'insecureEdgeTerminationPolicy' in term:
                term_str += '/' + term['insecureEdgeTerminationPolicy']
            row.append(term_str)
        except:
            row.append('??')
        # wildcard
        try:
            row.append(route['spec']['wildcardPolicy'])
        except:
            row.append('??')
        # # age
        # try:
        #     ct = p['metadata']['creationTimestamp']
        #     ts = r['gen_ts']
        #     row.append(age(ct,ts))
        # except:
        #     row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(route))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
