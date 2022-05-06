import os
from loguru import logger as lg
from omg.must_gather.exceptions import NoValidMgFound


def scan_mg(tdirs):
    """Scan directories for valid must-gather/inspect directories

    Args:
        tdirs (tuple[str]): Non-empty tuple of directory paths to scan

    Returns:
        list: List of valid (absolute) must-gather/inspect directories
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    valid_dirs = []
    for tdir in tdirs:
        vdirs = []
        if os.path.isdir(tdir):
            scan_q = [tdir]
            while len(scan_q) > 0:
                lg.debug('scan_q: ' + str(scan_q))
                wdir = scan_q.pop()
                subdirs = [d for d in os.listdir(wdir)
                           if os.path.isdir(os.path.join(wdir, d))]
                if ('cluster-scoped-resources' in subdirs
                   or 'namespaces' in subdirs):
                    lg.debug('Valid dir found: ' + str(wdir))
                    vdirs.append(os.path.abspath(wdir))
                else:
                    lg.debug('Not valid dir scanning deeper: ' + str(wdir))
                    scan_q.extend([os.path.join(wdir, d) for d in subdirs])
        if vdirs:
            valid_dirs.extend(vdirs)
        else:
            lg.warning('Not a valid must-gather: ' + str(tdir))
    if len(valid_dirs) > 0:
        lg.debug("valid_dirs: {}".format(valid_dirs))
        try:
            # Put the primary must-gather path on top of the paths list
            # Optional but good to do in multidir mode
            pmgs = [
                pmg for pmg in valid_dirs
                if "quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256" in pmg
            ]
            lg.debug("primary mgs: {}".format(pmgs))
            if len(pmgs) > 1:
                lg.warning("Multiple primary must-gather directories selected")
            # if not pmgs:
            #     lg.warning("No primary must-gather directory selected")
            for pmg in pmgs:
                valid_dirs.insert(
                    0, valid_dirs.pop(
                        valid_dirs.index(pmg)
                    )
                )
        except Exception:
            pass
        return valid_dirs
    else:
        raise NoValidMgFound("No valid must-gather(s) found!")
