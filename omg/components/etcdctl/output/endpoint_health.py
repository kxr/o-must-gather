import json
from tabulate import tabulate
from omg.utils.dget import dget


def etcdctl_out(j_data, output):
    if output == "json":
        print(json.dumps(j_data, indent=2))
    else:
        head = ["ENDPOINT", "HEALTH", "TOOK", "ERROR"]
        body = []
        for jd in j_data:
            body.append([
                dget(jd, ["endpoint"], "?"),
                dget(jd, ["health"], "?"),
                dget(jd, ["took"], "?"),
                dget(jd, ["error"], ""),
            ])
        if output == "table":
            print(tabulate(body, head, tablefmt="psql"))
        elif output is None or output == "simple":
            for row in body:
                if row[3] == "":
                    print(
                        "{} is healthy: "
                        "successfully committed proposal: took = {}"
                        .format(row[0], row[2])
                    )
                else:
                    print(
                        "{} is unhealthy: "
                        "failed to commit proposal: {}"
                        .format(row[0], row[3])
                    )
