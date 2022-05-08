import json
from tabulate import tabulate
from omg.utils.dget import dget


def etcdctl_out(j_data, output):
    if output == "json":
        print(json.dumps(j_data, indent=2))
    else:
        head = ["ID", "STATUS", "NAME", "PEER ADDRS", "CLIENT ADDRS", "IS LEARNER"]
        body = []
        for jd in dget(j_data, ["members"]):
            name = dget(jd, ["name"], "")
            body.append([
                "{:x}".format(int(dget(jd, ["ID"]))),
                "started" if len(name) > 0 else "unstarted",
                name,
                ",".join(dget(jd, ["peerURLs"], "?")),
                ",".join(dget(jd, ["clientURLs"], "?")),
                dget(jd, ["isLearner"], "false")
            ])
        if output == "table":
            print(tabulate(body, head, tablefmt="psql"))
        elif output is None or output == "simple":
            for row in body:
                print(", ".join([str(r) for r in row]))
