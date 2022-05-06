from omg.must_gather.generate_rdefs import generate_rdefs
from loguru import logger as lg
from omg.config import config
from omg.must_gather.exceptions import NoValidMgFound
from omg.use.show_mg_info import show_mg_info
from omg.must_gather.scan_mg import scan_mg


def cmd(mg_paths=None, cwd=False, cfile=None):
    """Landing function for `omg use`

    Args:
        mg_paths (string, optional): Path to extracted must-gather.
                                     Defaults to None.
        cwd (bool, optional): --cwd flag.
                              Defaults to False.

    Returns:
        int: return code 0/1 (success/failure)
    """
    lg.debug(str(locals()))
    if not mg_paths:
        # --cwd
        if cwd:
            try:
                config.save(paths=['.'], cfile=cfile)
            except Exception as e:
                lg.error(e)
                return 1
            else:
                lg.opt(colors=True).success(
                    "<e>[CWD Mode]</> Assuming your working directory as must-gather")
                return 0
        # No args passed
        else:
            show_mg_info(cfile)
            return 0
    else:
        # One or more dirs are passed via mg_paths,
        # scan and save the valid directories
        try:
            valid_mg_paths = scan_mg(mg_paths)
        except NoValidMgFound as e:
            lg.error(e)
            return 1

        # Foce re-generate rdefs for all discovered paths
        for path in valid_mg_paths:
            try:
                generate_rdefs(path)
            except Exception:
                # lg.warning("Failed generating rdef for {}: {}".format(path, e))
                pass

        # Save paths in config
        config.save(paths=valid_mg_paths, cfile=cfile)

        # Show selected must-gather paths to user
        show_mg_info(cfile)

        return 0
