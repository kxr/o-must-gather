from tabulate import tabulate
from dateutil.parser import parse

from omg.common.helper import age

# Simple out put with just name and age
def cv_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    output_res[0].extend(['NAME','VERSION','AVAILABLE','PROGRESSING','SINCE','STATUS'])
    # resources
    for r in res:
        cv = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + cv['metadata']['name'])
        else:
            row.append(cv['metadata']['name'])
        # version
        cur_ver = ''
        history = cv['status']['history']
        for h in history:
            if h['state'] == 'Completed':
                cur_ver = h['version']
            break
        row.append(cur_ver)
        # available,progressing,status
        avail = ''
        prog = ''
        status = ''
        transitions = []
        conds = cv['status']['conditions']
        for c in conds:
            if c['type'] == 'Available':
                avail = c['status']
                transitions.append(c['lastTransitionTime'])
            elif c['type'] == 'Progressing':
                prog = c['status']
                status = c['message']
                transitions.append(c['lastTransitionTime'])
            elif c['type'] == 'Failing':
                transitions.append(c['lastTransitionTime'])
            
        row.append(avail)
        row.append(prog)
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

        # status
        row.append(status)

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
