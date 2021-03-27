from tabulate import tabulate

from omg.common.helper import age, extract_labels

def is_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','IMAGE REPOSITORY','TAGS','UPDATED','LABELS'])
    else:
        output_res[0].extend(['NAME','IMAGE REPOSITORY','TAGS','UPDATED'])
    # resources
    for r in res:
        is_ = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(is_['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + is_['metadata']['name'])
        else:
            row.append(is_['metadata']['name'])
        # image repository
        try:
            row.append(is_['status']['publicDockerImageRepository'])
        except:
            row.append('')
        # tags
        try:
            tags = []
            for tag in is_['status']['tags']:
                tags.append(tag['tag'])
            row.append(','.join(tags))
        except:
            row.append('')
        # updated
        ## TODO: should update this to parse list of tags and determine latest updated image, rather than use metadata.creationTimestamp
        try:
            ## TODO: replace this check when reimplementing latest updated image
            if len(is_['status']['tags']) > 0:
                ct = str(is_['metadata']['creationTimestamp'])
                ts = r['gen_ts']
                row.append(age(ct,ts))
            else:
                row.append('')
        except:
            row.append('')
        # show-labels
        if show_labels:
            row.append(extract_labels(is_))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
