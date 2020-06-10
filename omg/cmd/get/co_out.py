from tabulate import tabulate
from dateutil.parser import parse

from omg.common.helper import age

# Special function to output clusteroperator
def co_out(t, ns, res, output, show_type):
    # Generate output table if -o not set or 'wide'
    # We will create an array of array and then print if with tabulate
    # header
    output_res = [['NAME','VERSION','AVAILABLE','PROGRESSING','DEGRADED','SINCE']]
    # resources
    for r in res:
        co = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + co['metadata']['name'])
        else:
            row.append(co['metadata']['name'])
        # version
        vers = co['status']['versions']
        ver = next( v['version'] for v in vers if v['name'] == 'operator' )
        row.append(ver)
        # available,progressing,degraded,since
        transitions = []
        cond = co['status']['conditions']
        for c in cond:
            if c['type'] == 'Degraded':
                dg = c['status']
                transitions.append(c['lastTransitionTime'])
            elif c['type'] == 'Progressing':
                pr = c['status']
                transitions.append(c['lastTransitionTime'])
            elif c['type'] == 'Available':
                av = c['status']
                transitions.append(c['lastTransitionTime'])
        row.append(av)
        row.append(pr)
        row.append(dg)
        # since
        latest_trans = None
        for t in transitions:
            if latest_trans is None:
                latest_trans = t
            else:
                if parse(t) > parse(latest_trans):
                    latest_trans = t
        since = age(latest_trans,r['gen_ts'])
        row.append(since)

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
