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
        if len(data) == 0:
            return content 
        form = head[5:].split(';')
        if ''.join(form) == '':
            return unquote(data)
        elif 'base64' in form:
            charset = next((x[8:] for x in form if x[0:8] == 'charset='),'utf-8')
            return b64decode(data).decode(charset)
    else:
        print('[Warning] Unable to recognize content (not starting with "data:")')
        return content

def get_mc(m):
    mc_map = map_res('machineconfig')
    mcs = from_yaml( rt = mc_map['type'], ns = None, names = m,
        yaml_loc = mc_map['yaml_loc'], need_ns = False)
    return([mc['res'] for mc in mcs])
    

def extract(m):
    mg_path = Config().path
    emc_dir = 'extracted-machine-configs'
    emc_path = os.path.join(mg_path, emc_dir)
    os.makedirs(emc_path, exist_ok=True)
    
    mcs = get_mc(m)
    for mc in mcs:
        if 'metadata' in mc and 'name' in mc['metadata']:
            mc_name = mc['metadata']['name']
        else:
            print('[WARNING] Skipping machine-config. Name not found')
            continue

        mc_path = os.path.join(emc_path, mc_name)
        os.makedirs(mc_path, exist_ok=True)

        if 'spec' in mc and 'config' in mc['spec']:
            # storage
            if 'storage' in mc['spec']['config']:
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
                # TODO directories, links, disks, raid, filesystems
            # systemd
            if 'systemd' in mc['spec']['config']:
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
            if 'passwd' in mc['spec']['config']:
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
                # TODO groups
                            )
            # TODO networkd

def compare(m, show_contents):
    # NOTE TO SELF: Recursion has gone out of hand,
    # probably re-impelement the comparison login without
    # using recursion
    try:
        mc1 = get_mc([m[0]])[0]
    except:
        print('[ERROR] Failed to load machine-config', m[0])
        return
    
    try:
        mc2 = get_mc([m[1]])[0]
    except:
        print('[ERROR] Failed to load machine-config', m[1])        
        return

    # Recursive function to show diff when --show-contents is set
    # We either get both strings in d1 and d2 ([*CHANGE]), or
    # we get on empty string on one and a dict on other ([+ADDED], [-REMOVED])
    def show_diff(d1,d2, indent=1, show_contents=show_contents ):
        #print(type(d1))
        #print(type(d2))
        if show_contents:
            if type(d1) in [str,int,bool] and type(d2) in [str,int,bool]:
                if str(d1).startswith('data:'):
                    data1 = decode_content(str(d1))
                else:
                    data1 = str(d1)
                if str(d2).startswith('data:'):
                    data2 = decode_content(str(d2))
                else:
                    data2 = str(d2)
                # Add new line at the end if missing
                if data1[-1:] != '\n' or data2[-1:] != '\n':
                    if data1 != '':
                        data1 += '\n'
                    if data2 != '':
                        data2 += '\n'
                diff = ''.join(
                        difflib.ndiff(
                            data1.splitlines(keepends=True),
                            data2.splitlines(keepends=True))
                        )
                for x in diff.splitlines():
                    print( '    '*indent + x)
                print('')
            elif type(d1) is dict and d2 == '':
                if len(d1) == 0:
                    show_diff('{}', '', indent)
                for key in d1:
                    print('    '*indent + '-> ' + key)
                    show_diff(d1[key], '', indent+1)
            elif type(d2) is dict and d1 == '':
                if len(d2) == 0:
                    show_diff('', '{}', indent)
                else:
                    for key in d2:
                        print('    '*indent + '-> ' + key)
                        show_diff('', d2[key], indent+1)

    # Recursive function to walk through two machine-configs,
    # and find differences between them
    def mc_diff(d1, d2, path=[]):
        # The two values are equal, nothing to do
        if d1 == d2:
            return
        # One of the two values is None
        elif d1 is None:
            print ("[+ADDED]", ' -> '.join(path), '\n')
            show_diff('',d2)
        elif d2 is None:
            print ("[-REMOVED]", ' -> '.join(path), '\n')
            show_diff(d1,'')
        # The two values are string/int/bool which are not equal
        elif (  (type(d1) is str  and type(d2) is str) or
                (type(d1) is int  and type(d2) is int) or
                (type(d1) is bool and type(d2) is bool)     ):
            print ("[*CHANGE]", ' -> '.join(path), '\n')
            show_diff( str(d1),str(d2))
        # The two values are dict which are not equal
        elif type(d1) is dict and type(d2) is dict:
            for k in set(list(d1.keys())+list(d2.keys())):
                path.append(k)
                if (k not in d2):
                    mc_diff( d1[k], None, path)
                elif (k not in d1):
                    mc_diff( None, d2[k])
                else:
                    mc_diff(d1[k],d2[k], path)
                path.pop()
        # The two values are lists which are not equal
        # We need to compare the two lists with some extended logic
        elif type(d1) is list and type(d2) is list:
            # The two lists contain different types of data
            ltypes = set([ type(x) for x in d1+d2 ])
            if len(ltypes) != 1:
                print('[WARNING] skipping inconsistent list: ', path)
                print('          Found mix types in list: ', ltypes)
                return
                
            done_lod_keys = []          
            # Traverse on both the list items
            for l in d1+d2:
                # If "list of dict" with kind/name/path keys,
                # we compare based on kind/name/path keys in the dicts
                if (type(l) is dict and
                   ('name' in l or 'path' in l or 'kind' in l) ):
                    if 'kind' in l:
                        lod_key = 'kind'
                    elif 'name' in l:
                        lod_key = 'name'
                    elif 'path' in l:
                        lod_key = 'path'
                    path.append(l[lod_key])
                    ld1 = [x for x in d1 if x[lod_key] == l[lod_key]]
                    ld2 = [x for x in d2 if x[lod_key] == l[lod_key]]
                    if len(ld1) > 1 or len(ld2) > 1:
                        print('[WARNING] Duplicate key found:', lod_key)
                    if len(ld1) == 0:
                        mc_diff( None, ld2[0], path )
                    elif len(ld2) == 0:
                        mc_diff( ld1[0], None, path )
                    elif l[lod_key] not in done_lod_keys:
                        mc_diff( ld1[0], ld2[0], path )
                        done_lod_keys.append(l[lod_key])
                    path.pop()
                else:
                    if l not in d2:
                        mc_diff( l, None, path)
                    if l not in d1:
                        mc_diff( None, l, path)
        else:
            print('[WARNING] Unhandled condition at', path)
    
    mc_diff(mc1,mc2)

def machine_config(a):
    if a.mc_op == 'extract':
        if len(a.mc_names) <= 0:
            extract('_all')
        else:
            extract(a.mc_names)
    elif a.mc_op == 'compare':
        if len(a.mc_names) == 2:
            compare(a.mc_names, show_contents=a.show_contents)
        else:
            print('[ERROR] Provide two machine-configs to compare')
