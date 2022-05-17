# -*- coding: utf-8 -*-
from datetime import datetime
from omg.utils.dget import dget
from dateutil.parser import parse
from omg.utils.age import age


def _col_image_repository(res):
    return dget(res, ["res", "status", "publicDockerImageRepository"])


def _col_tags(res):
    tags = [
        tag["tag"]
        for tag in
        dget(res, ["res", "status", "tags"], [])
        if "tag" in tag
    ]
    tag_string = ""
    while len(tags) > 0:
        t = tags.pop()
        if len(tag_string) + len(t) <= 30:
            if tag_string:
                tag_string = ",".join([tag_string, t])
            else:
                tag_string = t
        else:
            tag_string = "{} + {} more...".format(
                tag_string,
                len(tags) + 1
            )
            break
    return tag_string


def _col_updated(res):
    creation_ts = []
    tags = dget(res, ["res", "status", "tags"], [])
    if tags:
        for tag in tags:
            items = dget(tag, ["items"], [])
            if items:
                for item in items:
                    created = dget(item, ["created"])
                    if created:
                        creation_ts.append(created)
    latest = None
    if creation_ts:
        for cts in creation_ts:
            if isinstance(cts, datetime):
                cts = cts.isoformat()
            p_cts = parse(cts)
            if (
                latest is None or
                p_cts > latest
            ):
                latest = p_cts
    if latest:
        return age(latest.isoformat(), dget(res, ["yfile_ts"]))


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "IMAGE REPOSITORY": _col_image_repository,
    "TAGS": _col_tags,
    "UPDATED": _col_updated
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
