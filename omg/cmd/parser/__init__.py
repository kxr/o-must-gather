import os
from tabulate import tabulate

from omg.common.config import Config
from .etcd_out import etcd_member_list
from .etcd_out import etcd_endpoint_health
from .etcd_out import etcd_endpoint_status
from .etcd_out import etcd_show_all


parser_map = {
    "etcd-member-list": 
        {
            "command": "etcd-member-list",
            "helper": "Parser etcd member list from must-gather etcd_info/member_list.json",
            "file_in": "etcd_info/member_list.json",
            "fn_out": etcd_member_list
        },
    "etcd-endpoint-health": 
        {
            "command": "etcd-endpoint-health",
            "helper": "Parser etcd endpoint health from must-gather etcd_info/endpoint_status.json",
            "file_in": "etcd_info/endpoint_health.json",
            "fn_out": etcd_endpoint_health
        },
    "etcd-endpoint-status": 
        {
            "command": "etcd-endpoint-status",
            "helper": "Parser etcd endpoint status from must-gather etcd_info/endpoint_status.json",
            "file_in": "etcd_info/endpoint_status.json",
            "fn_out": etcd_endpoint_status
        },
    "etcd-all": 
        {
            "command": "etcd-all",
            "helper": "Parser etcd endpoint status from must-gather etcd_info/endpoint_status.json",
            "file_in": "",
            "fn_out": etcd_show_all
        }
}


def help():
    """
    Display parser helper for available commands.
    """
    header = [
        'command', 'helper'
    ]    
    output_res=[[]]
    output_res[0].extend([h.upper() for h in header])

    for m in parser_map.keys():
        row = []
        for mk in header:
            row.append(parser_map[m][mk])
        output_res.append(row)

    print(tabulate(output_res, tablefmt="plain"))


def file_reader(path):
    """
    Read a file to be parsed and return raw buffer.
    """
    try:
        full_path = os.path.join(Config().path, path)
        with open(full_path, 'r') as f:
            return f.read()
    except IsADirectoryError as e:
        print("WANING: ignoring file reader; Is a directory")
        return ""
    except:
        raise


def print_table(data=None, headers=[], rows=[], fmt="psql"):
    """
    Print a generic table. When headers and rows are defined, it will
    have precedence from data, otherwise the headers and rows will
    be extracted from it.
    """
    if (len(headers)) and (len(rows) > 0):
        return print(tabulate(rows, headers, tablefmt=fmt))

    if data is None:
        return print("ERROR: data buffer not found.")

    # extract headers from firs data fields
    headers = [h for h in data[0].keys()]
    rows = []

    for d in data:
        row = []
        for dk in d.keys():
            row.append(d[dk])
        rows.append(row)

    return print(tabulate(rows, headers, tablefmt=fmt))


# The high level function that gets called for any "get" command
def parser_main(command=None, show=None):
    """
    Main cli for parser option.
    """
    if show:
        return help()

    if command is None:
        print(f"Missing command argument, avaiable commands: ")
        return help()

    try:
        cmd = command[0]
        buffer = file_reader(parser_map[cmd]['file_in'])
        return parser_map[cmd]["fn_out"](buffer)
    except KeyError:
        print(f"Command [{command}] not found, avaiable commands: ")
        return help()
    except:
        raise
    
    return print("No resources was found")
