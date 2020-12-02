import tabulate as tb
from tabulate import tabulate
# preserve whitespace for displaying indents
tb.PRESERVE_WHITESPACE = True

from omg.common.helper import age

# We will create an array of array and then print if with tabulate
def pod_out(t, ns, res, show_type):
        
    for pod in res:
        output_res=[]
        p = pod['res']
        # name
        row = []
        row.append('Name:')
        row.append(p['metadata']['name'])
        output_res.append(row)
        # namespace
        row = []
        row.append('Namespace:')
        row.append(p['metadata']['namespace'])
        output_res.append(row)
        # priority
        row = []
        row.append('Priority:')
        row.append(p['spec']['priority'])
        output_res.append(row)
        # priority class name
        if 'priorityClassName' in p['spec']:
            row = []
            row.append('Priority Class Name:')
            row.append(p['spec']['priorityClassName'])
            output_res.append(row)
        # node
        row = []
        row.append('Node:')
        row.append(p['spec']['nodeName'] + '/' + p['status']['hostIP'])
        output_res.append(row)
        # start time
        row = []
        row.append('Start Time')
        row.append(p['status']['startTime'])
        output_res.append(row)
        # labels
        labels = p['metadata']['labels']
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
        if 'annotations' in p['spec']:
            annotations = p['spec']['annotations']
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
        # status
        row = []
        row.append('Status:')
        row.append(p['status']['phase'])
        output_res.append(row)
        # pod ip
        row = []
        row.append('IP:')
        row.append(p['status']['podIP'])
        output_res.append(row)
        # pod ips
        row = []
        row.append('IPs:')
        output_res.append(row)
        podips = p['status']['podIPs']
        for i in podips:
            row = []
            row.append('  IP:')
            row.append(i['ip'])
            output_res.append(row)
        # controlled by
        if 'ownerReferences' in p['metadata']:
            row = []
            row.append('Controlled By:')
            row.append(p['metadata']['ownerReferences'][0]['kind'] + '/' + p['metadata']['ownerReferences'][0]['name'])
            output_res.append(row)
        # containers
        row = []
        row.append('Containers:')
        row.append('This field is not implemented yet!')
        output_res.append(row)
        # conditions
        row = []
        row.append('Conditions:')
        output_res.append(row)
        row = []
        row.append('Type')
        row.append('Status')
        output_res.append(row)
        conditions = p['status']['conditions']
        for c in conditions:
            row = []
            row.append('  ' + c['type'])
            row.append(c['status'])
            output_res.append(row)
        # volumes
        row = []
        row.append('Volumes:')
        row.append('This field is not implemented yet!')
        output_res.append(row)
        # qos class
        row = []
        row.append('QoS Class:')
        row.append(p['status']['qosClass'])
        output_res.append(row)
        # node selectors
        if 'nodeSelector' in p['spec']:
            nodeselectors = p['spec']['nodeSelector']
        else:
            nodeselectors = []
        first_nodeselector = True
        if len(nodeselectors) == 0:
            row = []
            row.append('Node Selectors:')
            row.append('<none>')
            output_res.append(row)
        for n in nodeselectors:
            row = []
            if first_nodeselector == True:
                row.append('Node Selectors:')
                first_nodeselector = False
            else:
                row.append('')
            row.append(n + '=' + nodeselectors[n])
            output_res.append(row)
        # tolerations
        if 'tolerations' in p['spec']:
            tolerations = p['spec']['tolerations']
        else:
            tolerations = []
        first_toleration = True
        if len(tolerations) == 0:
            row = []
            row.append('Tolerations:')
            row.append('<none>')
            output_res.append(row)
        for t in tolerations:
            row = []
            if first_toleration == True:
                row.append('Tolerations:')
                first_toleration = False
            else:
                row.append('')
            toleration = ''
            if 'key' in t and 'effect' in t:
                toleration = t['key'] + ':' + t['effect'] + ' '
            if 'operator' in t:
                toleration = toleration + 'op=' + t['operator'] + ' '
            if 'tolerationSeconds' in t:
                toleration = toleration + 'for ' + str(t['tolerationSeconds']) + 's'
            row.append(toleration)
            output_res.append(row)
        # events
        row = []
        row.append('Events:')
        row.append('This field is not implemented yet!')
        output_res.append(row)
        
        output_res.append('')
        print(tabulate(output_res,tablefmt="plain"))

