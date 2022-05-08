import json


def etcdctl_out(j_data, output):
    print(json.dumps(j_data, indent=2))
