import json


def _load_buffer_as_json(buffer):
    """
    wrapper function to open a json from a given buffer.
    Return json object and error
    """
    try:
        data = json.loads(buffer)
        return data, False
    except json.decoder.JSONDecodeError :
        return "JSONDecodeError", True
    except Exception as e:
        return e, True


def etcd_member_list(buffer=None):
    """
    Show etcd member list table.
    """
    from . import print_table

    data, err = _load_buffer_as_json(buffer)
    h = data['header']

    print(f"\nClusterID: {h['cluster_id']}, MemberID: {h['member_id']}, RaftTerm: {h['raft_term']}")
    print_table(data=data['members'])


def etcd_endpoint_health(buffer=None):
    """
    Show etcd endpoint health table.
    """
    from . import print_table

    data, err = _load_buffer_as_json(buffer)
    print_table(data=data)


def etcd_endpoint_status(buffer=None):
    """
    Show etcd endpoint status table.
    """
    from . import print_table

    def sizeof_fmt(num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return ("%3.1f %s%s" % (num, unit, suffix))
            num /= 1024.0
        return ("%.1f %s%s" % (num, 'Yi', suffix))

    data, err = _load_buffer_as_json(buffer)
    headers_map = [
        "ENDPOINT", "ID", "VERSION", "DB SIZE", "IS LEADER",
        "IS LEARNER", "RAFT TERM", "RAFT INDEX", "RAFT APPLIED INDEX",
        "ERRORS", "DB IN USE"
    ]
    rows = []
    for d in data:
        row = []
        row.append(d['Endpoint'])
        row.append(d['Status']['header']['cluster_id'])
        row.append(d['Status']['version'])
        row.append(sizeof_fmt(d['Status']['dbSize']))
        # is leader
        if d['Status']['leader'] == d['Status']['header']['member_id']:
            row.append('true')
        else:
            row.append('false')
        # is learning
        if d['Status']['raftTerm'] == d['Status']['header']['revision']:
            row.append('true')
        else:
            row.append('false')
        row.append(d['Status']['raftTerm'])
        row.append(d['Status']['raftIndex'])
        row.append(d['Status']['raftAppliedIndex'])
        if 'Errors' in d:
            row.append(d['Errors'])
        else:
            row.append('')
        row.append(sizeof_fmt(d['Status']['dbSizeInUse']))

        rows.append(row)

    return print_table(headers=headers_map, rows=rows)


def etcd_show_all(buffer=None):
    """
    Show all etcd commands.
    """
    from . import (
        parser_map, file_reader 
    )

    etcd_cmds = []
    for cmd in parser_map.keys():
        if not cmd.startswith('etcd'):
            continue
        if cmd.startswith('etcd-all'):
            continue
        etcd_cmds.append(parser_map[cmd])

    for cmd in etcd_cmds:
        buffer, err = file_reader(cmd['file_in'])
        parser_map[cmd['command']]["fn_out"](buffer)
    
    return
