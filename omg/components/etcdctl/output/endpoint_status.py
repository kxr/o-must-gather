import json
from tabulate import tabulate
from omg.utils.dget import dget
from omg.utils.size import num2human


def etcdctl_out(j_data, output):
    if output == "json":
        print(json.dumps(j_data, indent=2))
    else:
        head = [
            "ENDPOINT", "ID", "VERSION", "DB SIZE/IN USE",
            "IS LEADER", "IS LEARNER", "RAFT TERM", "RAFT INDEX",
            "RAFT APPLIED INDEX", "ERRORS"
        ]
        body = []
        for jd in j_data:
            member_id = dget(jd, ["Status", "header", "member_id"])
            leader_id = dget(jd, ["Status", "leader"])
            body.append([
                dget(jd, ["Endpoint"], "?"),
                "{:x}".format(int(member_id)),
                dget(jd, ["Status", "version"], "?"),
                "{}/{}".format(
                    num2human(dget(jd, ["Status", "dbSize"], "0")),
                    num2human(dget(jd, ["Status", "dbSizeInUse"], "0"))
                ),
                "true" if member_id == leader_id else "false",
                dget(jd, ["isLearner"], "false"),
                dget(jd, ["Status", "raftTerm"], "?"),
                dget(jd, ["Status", "raftIndex"], "?"),
                dget(jd, ["Status", "raftAppliedIndex"], "?"),
                dget(jd, ["Status", "errors"], ""),
            ])
        if output == "table":
            print(tabulate(body, head, tablefmt="psql"))
        elif output is None or output == "simple":
            for row in body:
                print(", ".join([str(r) for r in row]))
