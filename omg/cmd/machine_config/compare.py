import difflib
from omg.common.config import Config
from omg.cmd.get_main import get_resources
from omg.cmd.machine_config.decode_content import decode_content

def compare(m, show_contents):
    # NOTE TO SELF: Recursion has gone out of hand,
    # probably re-impelement the comparison logic without
    # using recursion
    try:
        mcs_res = get_resources('machineconfig', m[0], None)
        mc1 = [ mc['res'] for mc in mcs_res ][0]
    except:
        print('[ERROR] Failed to load machine-config', m[0])
        return
    
    try:
        mcs_res = get_resources('machineconfig', m[1], None)
        mc2 = [ mc['res'] for mc in mcs_res ][0]
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
                    if len(ld1) > 1 and l[lod_key] not in done_lod_keys:
                        print('    [WARNING] Duplicate (%i) entries found in 1st MachineConfig for %s:%s' %
                                (len(ld1), lod_key,l[lod_key]))
                    if len(ld2) > 1 and l[lod_key] not in done_lod_keys:
                        print('    [WARNING] Duplicate (%i) entries found in 2nd MachineConfig for %s:%s' %
                                (len(ld2), lod_key,l[lod_key]))

                    if len(ld1) == 0:
                        mc_diff( None, ld2[-1], path )
                    elif len(ld2) == 0:
                        mc_diff( ld1[-1], None, path )
                    elif l[lod_key] not in done_lod_keys:
                        mc_diff( ld1[-1], ld2[-1], path )
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
