import os, sys, yaml, json
from urllib.parse import unquote
from base64 import b64decode
import difflib
from omg.common.config import Config
from omg.common.resource_map import map_res
from omg.cmd.get.from_yaml import from_yaml

def decode_content(content):
    split = content.split(',', 1)
    head = split[0]
    data = split[1]
    #if head[0:5] ==  'data:':
    if head.startswith('data:'):
        form = head[5:].split(';')
        if ''.join(form) == '':
            return(unquote(data))
        elif 'base64' in form:
            charset = next((x[8:] for x in form if x[0:8] == 'charset='),'utf-8')
            return(b64decode(data).decode(charset))
    else:
        print('[Warning] Unable to recognize content (not starting with "data:")')
        return(content)

def get_mc(m):
    mc_map = map_res('machineconfig')
    mcs = from_yaml(
        rt = mc_map['type'],
        ns=None,
        names=m,
        yaml_loc = mc_map['yaml_loc'],
        need_ns=False
    )
    return([mc['res'] for mc in mcs])
    

def extract(m):
    mg_path = Config().path
    emc_dir = 'extracted-machine-configs'
    emc_path = os.path.join(mg_path, emc_dir)
    os.makedirs(emc_path, exist_ok=True)
    
    mcs = get_mc(m)
    for mc in mcs:
        mc_name = mc['metadata']['name']

        mc_path = os.path.join(emc_path, mc_name)
        os.makedirs(mc_path, exist_ok=True)

        # storage
        storage_path = os.path.join(mc_path, 'storage')
        storage = mc['spec']['config']['storage']
        if 'files' in storage:
            for fi in storage['files']:
                path = fi['path']
                rel_fil = path[1:]
                rel_dir = os.path.dirname(rel_fil)
                abs_dir = os.path.join(storage_path, rel_dir)
                abs_fil = os.path.join(storage_path, rel_fil)
                os.makedirs(abs_dir,exist_ok=True)
                with open(abs_fil, 'w') as fh:
                    print(abs_fil)
                    fh.write(
                        decode_content(fi['contents']['source'])
                    )
        
        # systemd
        systemd_path = os.path.join(mc_path, 'systemd')
        systemd = mc['spec']['config']['systemd']
        if 'units' in systemd:
            for unit in systemd['units']:
                os.makedirs(systemd_path,exist_ok=True)
                name = unit['name']
                if unit['enabled'] is not True:
                    name += '.disabled'
                abs_fil = os.path.join(systemd_path, name)
                with open(abs_fil, 'w') as fh:
                    print(abs_fil)
                    fh.write(
                        unit['contents']
                    )

        # passwd
        passwd  = mc['spec']['config']['passwd']
        passwd_path = os.path.join(mc_path, 'passwd')
        if 'users' in passwd:
            for user in passwd['users']:
                os.makedirs(passwd_path,exist_ok=True)
                name = user['name']
                abs_fil = os.path.join(passwd_path, name)
                with open(abs_fil, 'w') as fh:
                    print(abs_fil)
                    fh.write(
                        yaml.dump(user)
                    )

def compare(m):
    mc1 = get_mc(m[0])[0]
    mc2 = get_mc(m[1])[0]

    def findDiff(d1, d2, path=[]):
        # print('path=',path)
        # print('XXXXd1=',d1)
        # print('XXXXd2=',d2)
        if d1 == d2:
            return
        elif type(d1) != type(d2):
            print ("[WARNING] Type mismatch at: ", ' -> '.join(path))
            print ('')
        elif type(d1) is str:
           if d1 != d2:
                print ("[CHANGE]", ' -> '.join(path), ":")
                print ('')
                #print ("    - ", d1)
                #print ("    + ", d2)
                #print ('')
                if d1.startswith('data:') and d2.startswith('data:'):
                    data1 = decode_content(d1).splitlines(keepends=True)
                    data2 = decode_content(d2).splitlines(keepends=True)
                else:
                    data1 = d1.splitlines(keepends=True)
                    data2 = d2.splitlines(keepends=True)
                diff = difflib.context_diff(data1,data2)
                print(''.join(diff))
                #print(list(diff))
        elif type(d1) is dict:
            for k in set(list(d1.keys())+list(d2.keys())):
                path.append(k)
                if (k not in d2):
                    print ("[-REMOVED]", ' -> '.join(path), ":")
                    print('')
                elif (k not in d1):
                    print ("[+ADDED]", ' -> '.join(path), ":")
                    print('')
                else:
                    findDiff(d1[k],d2[k], path)
                path.pop()
        elif type(d1) is list:
            ltypes = set([ type(x) for x in d1+d2 ])
            if len(ltypes) != 1:
                print('[WARNING] skipping inconsistent list: ', path)
                print('          Found mix types in list: ', ltypes)
                return
            #ltype = next(ltypes)                
            for l in d1+d2:
                # print('d1=',d1)
                # print('d2=',d2)
                # print('pathx=',path)
                # If list of dict with kind/name/path we compare based on
                # kind/name/path keys in the dicts
                if (type(l) is dict and
                   ('name' in l or 'path' in l or 'kind' in l) ):
                    if 'kind' in l:
                        lod_key = 'kind'
                    elif 'name' in l:
                        lod_key = 'name'
                    elif 'path' in l:
                        lod_key = 'path'
                    # print('lodkey=',lod_key)
                    path.append(l[lod_key])
                    ld1 = [x for x in d1 if x[lod_key] == l[lod_key]]
                    ld2 = [x for x in d2 if x[lod_key] == l[lod_key]]
                    if len(ld1) > 1 or len(ld2) > 2:
                        print('[WARNING] Duplicate key found:', lod_key)
                    if len(ld1) == 0:
                        findDiff( {}, ld2[0], path )
                    elif len(ld2) == 0:
                        findDiff( ld1[0], {}, path )
                    else:
                        findDiff( ld1[0], ld2[0], path )
                    path.pop()
                else:
                    print('Unhandled XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        else:
            print('Unhandled2 XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            
    findDiff(mc1,mc2)

def machine_config(a):
    if a.mc_op == 'extract':
        if len(a.mc_names) <= 0:
            extract('_all')
        else:
            extract(a.mc_names)
    elif a.mc_op == 'compare':
        if len(a.mc_names) == 2:
            compare(a.mc_names)
        else:
            print('[ERROR] Provide two machine-configs to compare')

