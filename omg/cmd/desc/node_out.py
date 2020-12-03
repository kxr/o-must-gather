import tabulate as tb
from tabulate import tabulate
# preserve whitespace for displaying indents
tb.PRESERVE_WHITESPACE = True

from omg.common.helper import age

# We will create an array of array and then print if with tabulate
def node_out(t, ns, res, events, show_type):

    for node in res:
        output_res=[]
        n = node['res']
        # name
        row = []
        row.append('Name:')
        row.append(n['metadata']['name'])
        output_res.append(row)
        # roles
        row = []
        row.append('Roles:')
        role = ""
        labels = n['metadata']['labels']
        for l in labels:
            if "node-role.kubernetes.io" in l:
                role = l.split('/')[1]
        row.append(role)
        output_res.append(row)
        # labels
        first_label = True
        for l in labels:
            row = []
            if first_label == True:
                row.append('Labels:')
                first_label = False
            else:
                row.append('')
            row.append(l + '=' + labels[l])
            output_res.append(row)
        # annotations
        # annotations
        if 'annotations' in n['spec']:
            annotations = n['spec']['annotations']
        else:
            annotations = []
        first_annotation = True
        if len(annotations) == 0:
            row = []
            row.append('Annotations:')
            row.append('<none>')
            output_res.append(row)
        for a in annotations:
            row = []
            if first_annotation == True:
                row.append('Annotations:')
                first_annotation = False
            else:
                row.append('')
            row.append(a + '=' + annotations[a])
            output_res.append(row)
        # creationtimestamp
        row = []
        row.append('CreationTimestamp:')
        ### TODO: convert timestamp format i.e. Tue, 21 Jul 2020 16:53:19 -0400
        row.append(n['metadata']['creationTimestamp'])
        output_res.append(row)
        # taints
        if 'taints' in n['spec']:
            taints = n['spec']['taints']
        else:
            taints = []
        first_taint = True
        if len(taints) == 0:
            row = []
            row.append('Taints:')
            row.append('<none>')
            output_res.append(row)
        for t in taints:
            row = []
            if first_taint == True:
                row.append('Taints:')
                first_taint = False
            else:
                row.append('')
            if 'value' in t:
                row.append(t['key'] + '=' + t['value'] + ':' + t['effect'])
            else:
                row.append(t['key'] + ':' + t['effect'])
            output_res.append(row)
        # unschedulable
        row = []
        row.append('Unschedulable:')
        if 'unschedulable' in n['spec']:
            row.append('true')
        else:
            row.append('false')
        output_res.append(row)
        
        # lease
        row = []
        row.append('Lease:')
        ### TODO: determine if we actually capture lease data for output
        row.append('This field is not implemented yet!')
        output_res.append(row)
        
        # print out what we have so far, next table(s) will have new indents
        print(tabulate(output_res,tablefmt="plain"))
        output_res = []

        # conditions
        row = []
        row.append('Conditions:')
        output_res.append(row)
        header = []
        header.append('  Type')
        header.append('Status')
        header.append('LastHeartbeatTime')
        header.append('LastTransitionTime')
        header.append('Reason')
        header.append('Message')
        output_res.append(header)
        header = []
        header.append('  ----')
        header.append('------')
        header.append('-----------------')
        header.append('------------------')
        header.append('------')
        header.append('-------')
        output_res.append(header)
        conditions = n['status']['conditions']
        for c in conditions:
            row = []
            row.append('  ' + c['type'])
            row.append(c['status'])
            row.append(c['lastHeartbeatTime'])
            row.append(c['lastTransitionTime'])
            row.append(c['reason'])
            row.append(c['message'])
            output_res.append(row)
        
        # print out what we have so far, next table(s) will have new indents
        print(tabulate(output_res,tablefmt="plain"))
        output_res = []
        
        # addresses
        row = []
        row.append('Addresses:')
        output_res.append(row)
        addresses = n['status']['addresses']
        for a in addresses:
            row = []
            row.append('  ' + a['type'] + ':')
            row.append(a['address'])
            output_res.append(row)
        
        # print out what we have so far, next table(s) will have new indents
        print(tabulate(output_res,tablefmt="plain"))
        output_res = []
        
        # capacity
        row = []
        row.append('Capacity:')
        output_res.append(row)
        capacity = n['status']['capacity']
        for c in capacity:
            row = []
            row.append('  ' + c + ':')
            row.append(capacity[c])
            output_res.append(row)
        # allocatable
        row = []
        row.append('Allocatable:')
        output_res.append(row)
        allocatable = n['status']['allocatable']
        for a in allocatable:
            row = []
            row.append('  ' + a + ':')
            row.append(allocatable[a])
            output_res.append(row)
        
        # print out what we have so far, next table(s) will have new indents
        print(tabulate(output_res,tablefmt="plain"))
        output_res = []
        
        # system info
        row = []
        row.append('System Info:')
        output_res.append(row)
        row = []
        row.append('  Machine ID:')
        row.append(n['status']['nodeInfo']['machineID'])
        output_res.append(row)
        row = []
        row.append('  System UUID:')
        row.append(n['status']['nodeInfo']['systemUUID'])
        output_res.append(row)
        row = []
        row.append('  Boot ID:')
        row.append(n['status']['nodeInfo']['bootID'])
        output_res.append(row)
        row = []
        row.append('  Kernel Version:')
        row.append(n['status']['nodeInfo']['kernelVersion'])
        output_res.append(row)
        row = []
        row.append('  OS Image:')
        row.append(n['status']['nodeInfo']['osImage'])
        output_res.append(row)
        row = []
        row.append('  Operating System:')
        row.append(n['status']['nodeInfo']['operatingSystem'])
        output_res.append(row)
        row = []
        row.append('  Architecture:')
        row.append(n['status']['nodeInfo']['architecture'])
        output_res.append(row)
        row = []
        row.append('  Container Runtime Version:')
        row.append(n['status']['nodeInfo']['containerRuntimeVersion'])
        output_res.append(row)
        row = []
        row.append('  Kubelet Version:')
        row.append(n['status']['nodeInfo']['kubeletVersion'])
        output_res.append(row)
        row = []
        row.append('  Kube-Proxy Version:')
        row.append(n['status']['nodeInfo']['kubeProxyVersion'])
        output_res.append(row)
        # pod cidr
        if 'spec' in n:
            if 'podCIDR' in n['spec']:
                podcidr = n['spec']['podCIDR']
                row = []
                row.append('PodCIDR:')
                row.append(podcidr)
                output_res.append(row)
            if 'podCIDRs' in n['spec']:
                podcidrs = n['spec']['podCIDRs'][0]
                row = []
                row.append('PodCIDRs:')
                row.append(podcidrs)
                output_res.append(row)
        
        ### TODO: need to gather all pods residing on this node from other YAMLs to output the non-terminated pods
        # non-terminated pods
        row = []
        row.append('Non-terminated Pods:')
        row.append('This field is not implemented yet!')
        output_res.append(row)
        # allocated resources
        row = []
        row.append('Allocated resources:')
        row.append('This field is not implemented yet!')
        output_res.append(row)
        # events
        matchedevents = []
        for event in events:
            e = event['res']
            # cycle through involvedObject to match events for our pod
            if 'involvedObject' in e:
                if e['involvedObject']['kind'] == 'Node' and e['involvedObject']['name'] == n['metadata']['name']:
                    matchedevents.append(e)
        if len(matchedevents) == 0:
            row = []
            row.append('Events:')
            row.append('<none>')
            output_res.append(row)
        else:
            # refresh indent for events table only if we have matched events
            # print out what we have so far, next table(s) will have new indents
            print(tabulate(output_res,tablefmt="plain"))
            output_res = []
        
            row = []
            row.append('Events:')
            output_res.append(row)
            header = []
            header.append('  Type')
            header.append('Reason')
            header.append('Age')
            header.append('From')
            header.append('Message')
            output_res.append(header)
            header = []
            header.append('  ----')
            header.append('------')
            header.append('----')
            header.append('----')
            header.append('-------')
            output_res.append(header)
            for m in matchedevents:
                row = []
                row.append('  ' + m['type'])
                row.append(m['reason'])
                # age
                try:
                    ct = str(m['lastTimestamp'])
                    ts = node['gen_ts']
                    row.append(age(ct,ts))
                except:
                    row.append('Unknown')
                row.append(m['source']['component'])
                row.append(m['message'])
                output_res.append(row)
        
        output_res.append('')
        print(tabulate(output_res,tablefmt="plain"))

