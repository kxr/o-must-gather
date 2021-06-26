import json


def alerts_summary(buffer=None):
    """
    Show summary of alerts exported by must-gather.
    For more details (message details, open the json file)
    """
    from . import print_table

    data = json.loads(buffer)
    alerts = []
    for g in data['data']['groups']:
        for r in g['rules']:
            alerts.append({
                "GroupName": g['name'],
                "Name": r['name'],
                "State": r['state'],
                "AlertsCount": len(r['alerts']),
                "Health": r['health']
            })
    print_table(data=alerts)


def alerts_firing(buffer=None):
    """
    Show alerts firing (with labels) exported by must-gather.
    """
    from . import print_table

    data = json.loads(buffer)
    alerts = []
    for g in data['data']['groups']:

        for r in g['rules']:
            if len(r['alerts']) <= 0:
                continue

            for a in r['alerts']:
                details = ""

                for l in a['labels'].keys():
                    details += (f" {l}={a['labels'][l]}\n")
                alerts.append({
                    "Group/AlertName": (f"{g['name']}/{r['name']}"),
                    "ActiveAt": a['activeAt'],
                    "State": a['state'],
                    "Details": details
                })
    print_table(data=alerts)
