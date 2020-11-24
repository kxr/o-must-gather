import tabulate as tb
from tabulate import tabulate
# preserve whitespace for displaying indents
tb.PRESERVE_WHITESPACE = True

from omg.common.helper import age

# We will create an array of array and then print if with tabulate
def node_out(t, ns, res, show_type):
        
    for node in res:
        output_nodes=[]
        n = node['res']
        row = []
        # name
        row.append('Name:')
        row.append(n['metadata']['name'])
        output_nodes.append(row)
        # roles
        row = []
        row.append('Roles:')
        ### TODO: implement roles
        row.append('This field is not implemented yet!')
        output_nodes.append(row)
        # labels
        row = []
        labels = n['metadata']['labels']
        first_label = True
        for l in labels:
            if first_label == True:
                row.append('Labels:')
                first_label = False
            else:
                row.append('')
            row.append(l + '=' + labels[l])
            output_nodes.append(row)
            row = [] # clear contents after printing each row
        # annotations
        row = []
        annotations = n['metadata']['annotations']
        first_annotation = True
        for annotation in annotations:
            if first_annotation == True:
                row.append('Annotations:')
                first_annotation = False
            else:
                row.append('')
            row.append(annotation + '=' + annotations[annotation])
            output_nodes.append(row)
            row = [] # clear contents after printing each row
        # creationtimestamp
        row = []
        row.append('CreationTimestamp:')
        ### TODO: convert timestamp format i.e. Tue, 21 Jul 2020 16:53:19 -0400
        row.append(n['metadata']['creationTimestamp'])
        output_nodes.append(row)
        # taints
        row = []
        if 'taints' in n['spec']:
            taints = n['spec']['taints']
        else:
            taints = []
        first_taint = True
        if len(taints) == 0:
            row.append('Taints:')
            row.append('<none>')
            output_nodes.append(row)
        for t in taints:
            if first_taint == True:
                row.append('Taints:')
                first_taint = False
            else:
                row.append('')
            if 'value' in t:
                row.append(t['key'] + '=' + t['value'] + ':' + t['effect'])
            else:
                row.append(t['key'] + ':' + t['effect'])
            output_nodes.append(row)
            row = [] # clear contents after printing each row
        # unschedulable
        row = []
        row.append('Unschedulable:')
        if 'unschedulable' in n['spec']:
            row.append('true')
        else:
            row.append('false')
        output_nodes.append(row)
        # lease
        row = []
        row.append('Lease:')
        ### TODO: determine if we actually capture lease data for output
        row.append('This field is not implemented yet!')
        output_nodes.append(row)
        
        # print out what we have so far, so we can preserve indents on the next table
        print(tabulate(output_nodes,tablefmt="plain"))
        output_nodes = []

        # conditions
        row = []
        row.append('Conditions:')
        output_nodes.append(row)
        header = []
        header.append('  Type')
        header.append('Status')
        header.append('LastHeartbeatTime')
        header.append('LastTransitionTime')
        header.append('Reason')
        header.append('Message')
        output_nodes.append(header)
        header = []
        header.append('  ----')
        header.append('------')
        header.append('-----------------')
        header.append('------------------')
        header.append('------')
        header.append('-------')
        output_nodes.append(header)
        conditions = n['status']['conditions']
        for c in conditions:
            row = []
            row.append('  ' + c['type'])
            row.append(c['status'])
            row.append(c['lastHeartbeatTime'])
            row.append(c['lastTransitionTime'])
            row.append(c['reason'])
            row.append(c['message'])
            output_nodes.append(row)
        
        print(tabulate(output_nodes,tablefmt="plain"))
        output_nodes = []
        
        # addresses
        row = []
        row.append('Addresses:')
        output_nodes.append(row)
        addresses = n['status']['addresses']
        for a in addresses:
            row = []
            row.append('  ' + a['type'] + ':')
            row.append(a['address'])
            output_nodes.append(row)
        # capacity
        row = []
        row.append('Capacity:')
        output_nodes.append(row)
        capacity = n['status']['capacity']
        for c in capacity:
            row = []
            row.append('  ' + c + ':')
            row.append(capacity[c])
            output_nodes.append(row)
        # allocatable
        row = []
        row.append('Allocatable:')
        output_nodes.append(row)
        allocatable = n['status']['allocatable']
        for a in allocatable:
            row = []
            row.append('  ' + a + ':')
            row.append(allocatable[a])
            output_nodes.append(row)
        # system info
        row = []
        row.append('System Info:')
        output_nodes.append(row)
        row = []
        row.append('  Machine ID:')
        row.append(n['status']['nodeInfo']['machineID'])
        output_nodes.append(row)
        row = []
        row.append('  System UUID:')
        row.append(n['status']['nodeInfo']['systemUUID'])
        output_nodes.append(row)
        row = []
        row.append('  Boot ID:')
        row.append(n['status']['nodeInfo']['bootID'])
        output_nodes.append(row)
        row = []
        row.append('  Kernel Version:')
        row.append(n['status']['nodeInfo']['kernelVersion'])
        output_nodes.append(row)
        row = []
        row.append('  OS Image:')
        row.append(n['status']['nodeInfo']['osImage'])
        output_nodes.append(row)
        row = []
        row.append('  Operating System:')
        row.append(n['status']['nodeInfo']['operatingSystem'])
        output_nodes.append(row)
        row = []
        row.append('  Architecture:')
        row.append(n['status']['nodeInfo']['architecture'])
        output_nodes.append(row)
        row = []
        row.append('  Container Runtime Version:')
        row.append(n['status']['nodeInfo']['containerRuntimeVersion'])
        output_nodes.append(row)
        row = []
        row.append('  Kubelet Version:')
        row.append(n['status']['nodeInfo']['kubeletVersion'])
        output_nodes.append(row)
        row = []
        row.append('  Kube-Proxy Version:')
        row.append(n['status']['nodeInfo']['kubeProxyVersion'])
        output_nodes.append(row)
        # pod cidr
        if 'spec' in n:
            if 'podCIDR' in n['spec']:
                podcidr = n['spec']['podCIDR']
                row = []
                row.append('PodCIDR:')
                row.append(podcidr)
                output_nodes.append(row)
            if 'podCIDRs' in n['spec']:
                podcidrs = n['spec']['podCIDRs'][0]
                row = []
                row.append('PodCIDRs:')
                row.append(podcidrs)
                output_nodes.append(row)
        
        ### TODO: need to gather all pods residing on this node from other YAMLs to output the non-terminated pods
        # non-terminated pods
        row = []
        row.append('Non-terminated Pods:')
        row.append('This field is not implemented yet!')
        output_nodes.append(row)
        # allocated resources
        row = []
        row.append('Allocated resources:')
        row.append('This field is not implemented yet!')
        output_nodes.append(row)
        # events
        row = []
        row.append('Events:')
        row.append('This field is not implemented yet!')
        output_nodes.append(row)
        
        output_nodes.append('')
        print(tabulate(output_nodes,tablefmt="plain"))

