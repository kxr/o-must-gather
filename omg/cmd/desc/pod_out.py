import tabulate as tb
from tabulate import tabulate
# preserve whitespace for displaying indents
tb.PRESERVE_WHITESPACE = True

from omg.common.helper import age

# We will create an array of array and then print if with tabulate
def pod_out(t, ns, res, events, show_type):
        
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
        output_res.append(row)
        
        # parse through both containers and initContainers
        containers = []
        if 'containers' in p['spec']:
            containers = p['spec']['containers']
        if 'initContainers' in p['spec']:
            containers = containers + p['spec']['initContainers']
        for c in containers:
            # also parse through status.containerStatuses for matching container
            container_statuses = []
            if 'containerStatuses' in p['status']:
                container_statuses = p['status']['containerStatuses']
            if 'initContainerStatuses' in p['status']:
                container_statuses = container_statuses + p['status']['initContainerStatuses']
            container_status = []
            for cs in container_statuses:
                if cs['name'] == c['name']:
                    container_status = cs
            
            row = []
            row.append('  ' + c['name'] + ':')
            output_res.append(row)
            row = []
            row.append('    Container ID:')
            row.append(container_status['containerID'])
            output_res.append(row)
            row = []
            row.append('    Image:')
            row.append(c['image'])
            output_res.append(row)
            row = []
            row.append('    Image ID:')
            row.append(c['image'])
            output_res.append(row)
            if 'ports' in c:
                if 'containerPort' in c['ports'][0]:
                    row = []
                    row.append('    Port:')
                    row.append(str(c['ports'][0]['containerPort']) + '/' + c['ports'][0]['protocol'])
                    output_res.append(row)
                if 'hostPort' in c['ports'][0]:
                    row = []
                    row.append('    Host Port:')
                    row.append(str(c['ports'][0]['hostPort']) + '/' + c['ports'][0]['protocol'])
                    output_res.append(row)
            
            # print out what we have so far, next table(s) will have new indents
            print(tabulate(output_res,tablefmt="plain"))
            output_res = []
            
            if 'command' in c:
                command = c['command']
                row = []
                row.append('    Command:')
                output_res.append(row)
                for com in command:
                    row = []
                    row.append('      ' + com)
                    output_res.append(row)
                if 'args' in c:
                    args = c['args']
                    row = []
                    row.append('    Args:')
                    output_res.append(row)
                    for a in args:
                        row = []
                        row.append('      ' + a)
                        output_res.append(row)
            
            # print out what we have so far, next table(s) will have new indents
            print(tabulate(output_res,tablefmt="plain"))
            output_res = []
            
            # container state
            state = container_status['state']
            row = []
            row.append('    State:')
            row.append(list(state.keys())[0].capitalize())
            output_res.append(row)
            # print nested container state, if applicable
            if state.get(list(state.keys())[0], {}).get('reason') is not None:
                row = []
                row.append('      Reason:')
                row.append(state.get(list(state.keys())[0], {}).get('reason'))
                output_res.append(row)
            if state.get(list(state.keys())[0], {}).get('exitCode') is not None:
                row = []
                row.append('      Exit Code:')
                row.append(state.get(list(state.keys())[0], {}).get('exitCode'))
                output_res.append(row)
            if state.get(list(state.keys())[0], {}).get('startedAt') is not None:
                row = []
                row.append('      Started:')
                row.append(state.get(list(state.keys())[0], {}).get('startedAt'))
                output_res.append(row)
            if state.get(list(state.keys())[0], {}).get('finishedAt') is not None:
                row = []
                row.append('      Finished:')
                row.append(state.get(list(state.keys())[0], {}).get('finishedAt'))
                output_res.append(row)
            
            # container last state
            last_state = []
            if 'lastState' in container_status:
                last_state = container_status['lastState']
                if len(last_state) != 0:
                    row = []
                    row.append('    Last State:')
                    row.append(list(last_state.keys())[0].capitalize())
                    output_res.append(row)
                    # print nested container last state, if applicable
                    if last_state.get(list(last_state.keys())[0], {}).get('reason') is not None:
                        row = []
                        row.append('      Reason:')
                        row.append(last_state.get(list(last_state.keys())[0], {}).get('reason'))
                        output_res.append(row)
                    if last_state.get(list(last_state.keys())[0], {}).get('exitCode') is not None:
                        row = []
                        row.append('      Exit Code:')
                        row.append(last_state.get(list(last_state.keys())[0], {}).get('exitCode'))
                        output_res.append(row)
                    if last_state.get(list(last_state.keys())[0], {}).get('startedAt') is not None:
                        row = []
                        row.append('      Started:')
                        row.append(last_state.get(list(last_state.keys())[0], {}).get('startedAt'))
                        output_res.append(row)
                    if last_state.get(list(last_state.keys())[0], {}).get('finishedAt') is not None:
                        row = []
                        row.append('      Finished:')
                        row.append(last_state.get(list(last_state.keys())[0], {}).get('finishedAt'))
                        output_res.append(row)
            
            row = []
            row.append('    Ready:')
            row.append(container_status['ready'])
            output_res.append(row)
            row = []
            row.append('    Restart Count:')
            row.append(container_status['restartCount'])
            output_res.append(row)
            if 'resources' in c and 'requests' in c['resources']:
                row = []
                row.append('    Requests:')
                output_res.append(row)
                if 'cpu' in c['resources']['requests']:
                    row = []
                    row.append('      cpu:')
                    row.append(c['resources']['requests']['cpu'])
                    output_res.append(row)
                if 'memory' in c['resources']['requests']:
                    row = []
                    row.append('      memory:')
                    row.append(c['resources']['requests']['memory'])
                    output_res.append(row)
            
            
            # environment
            if 'env' in c:
                row = []
                row.append('    Environment:')
                output_res.append(row)
                env = c['env']
            
                for e in env:
                    row = []
                    row.append('      ' + e['name'])
                    if 'value' in e:
                        row.append(e['value'])
                    ## TODO: implement valueFrom where used in the below example
                    ##    - name: K8S_NODE_NAME
                    ##      valueFrom:
                    ##        fieldRef:
                    ##          apiVersion: v1
                    ##          fieldPath: spec.nodeName
                    output_res.append(row)
            else:
                row = []
                row.append('    Environment:')
                row.append('<none>')
                output_res.append(row)
            
            # print out what we have so far, next table(s) will have new indents
            print(tabulate(output_res,tablefmt="plain"))
            output_res = []
            
            # mounts
            if 'volumeMounts' in c:
                row = []
                row.append('    Mounts:')
                output_res.append(row)
                mounts = c['volumeMounts']
                
                for m in mounts:
                    row = []
                    # parse through optional readOnly and subPath fields
                    rw = 'rw' # read-write if not defined
                    if 'readOnly' in mounts:
                        if m['readOnly'] == True:
                            rw = 'ro'
                    if 'subPath' in mounts:
                        mount_options = '(' + rw + ',path="' + m['subPath'] + '")'
                    else:
                        mount_options = '(' + rw + ')'
                    row.append('      ' + m['mountPath'] + ' from ' + m['name'] + ' ' + mount_options)
                    output_res.append(row)
            else:
                row = []
                row.append('    Mounts:')
                row.append('<none>')
                output_res.append(row)
            
        # print out what we have so far, next table(s) will have new indents
        print(tabulate(output_res,tablefmt="plain"))
        output_res = []
            
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
        output_res.append(row)
        
        volumes = p['spec']['volumes']
        for v in volumes:
            row = []
            row.append('  ' + v['name'] + ':')
            output_res.append(row)
            
            # print out what we have so far, next table(s) will have new indents
            print(tabulate(output_res,tablefmt="plain"))
            output_res = []
            
            if 'hostPath' in v:
                row = []
                row.append('    Type:')
                row.append('HostPath (bare host directory volume)')
                output_res.append(row)
                row = []
                row.append('    Path:')
                row.append(v['hostPath']['path'])
                output_res.append(row)
                row = []
                row.append('    HostPathType:')
                row.append(v['hostPath']['type'])
                output_res.append(row)
            elif 'configMap' in v:
                row = []
                row.append('    Type:')
                row.append('ConfigMap (a volume populated by a ConfigMap)')
                output_res.append(row)
                row = []
                row.append('    Name:')
                row.append(v['configMap']['name'])
                output_res.append(row)
                if 'optional' in v['configMap']:
                    row = []
                    row.append('    Optional:')
                    row.append(str(v['configMap']['optional']).lower())
                    output_res.append(row)
                else:
                    row = []
                    row.append('    Optional:')
                    row.append('false')
                    output_res.append(row)
            elif 'secret' in v:
                row = []
                row.append('    Type:')
                row.append('Secret (a volume populated by a Secret)')
                output_res.append(row)
                row = []
                row.append('    SecretName:')
                row.append(v['secret']['secretName'])
                output_res.append(row)
                if 'optional' in v['secret']:
                    row = []
                    row.append('    Optional:')
                    row.append(str(v['secret']['optional']).lower())
                    output_res.append(row)
                else:
                    row = []
                    row.append('    Optional:')
                    row.append('false')
                    output_res.append(row)
            elif 'persistentVolumeClaim' in v:
                row = []
                row.append('    Type:')
                row.append('PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)')
                output_res.append(row)
                row = []
                row.append('    ClaimName:')
                row.append(v['persistentVolumeClaim']['claimName'])
                output_res.append(row)
                ## TODO: need a working example to validate this
                if 'readOnly' in v['persistentVolumeClaim']:
                    row = []
                    row.append('    ReadOnly:')
                    row.append(str(v['persistentVolumeClaim']['readOnly']).lower())
                    output_res.append(row)
                else:
                    row = []
                    row.append('    ReadOnly:')
                    row.append('false')
                    output_res.append(row)
            elif 'projected' in v:
                row = []
                row.append('    Type:')
                row.append('Projected (a volume that contains injected data from multiple sources)')
                output_res.append(row)
                row = []
                row.append('    SecretName:')
                row.append(v['projected']['sources'][0]['secret']['name'])
                output_res.append(row)
                ## TODO: need a working example to implement this
                row = []
                row.append('    SecretOptionalName:')
                row.append('<nil>')
                output_res.append(row)
            elif 'emptyDir' in v:
                row = []
                row.append('    Type:')
                row.append("EmptyDir (a temporary directory that shares a pod's lifetime)")
                output_res.append(row)
                ## TODO: need a working example to implement this
                row = []
                row.append('    Medium:')
                output_res.append(row)
                row = []
                row.append('    SizeLimit:')
                row.append('<unset>')
                output_res.append(row)
        
            # print out what we have so far, next table(s) will have new indents
            print(tabulate(output_res,tablefmt="plain"))
            output_res = []
        
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
        matchedevents = []
        for event in events:
            e = event['res']
            # cycle through involvedObject to match events for our pod
            if 'involvedObject' in e:
                if e['involvedObject']['kind'] == 'Pod' and e['involvedObject']['name'] == p['metadata']['name']:
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
                    ts = pod['gen_ts']
                    row.append(age(ct,ts))
                except:
                    row.append('Unknown')
                row.append(m['source']['component'])
                row.append(m['message'])
                output_res.append(row)
        
        output_res.append('')
        print(tabulate(output_res,tablefmt="plain"))

