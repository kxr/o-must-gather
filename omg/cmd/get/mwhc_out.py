from tabulate import tabulate

from omg.common.helper import age


def mwhc_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    output_res[0].extend(['NAME','WEBHOOKS','AGE'])
    # resources
    for r in res:
        mwhc = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + mwhc['metadata']['name'])
        else:
            row.append(mwhc['metadata']['name'])
        # webhooks
        if 'webhooks' in mwhc:
            webhooks = len(mwhc['webhooks'])
        else:
            webhooks = 0
        row.append(webhooks)
        # age
        try:
            ct = str(mwhc['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
