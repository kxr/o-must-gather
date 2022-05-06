import pytest
import os
from omg.lib.mg_ops.locate_yamls import locate_yamls
from omg.lib.mg_ops.scan_mg import scan_mg, NoValidMgFound
from omg.config.logging import setup_logging


setup_logging(loglevel="normal")


def test_scan_mg_invalid(tmpdir):
    with pytest.raises(NoValidMgFound):
        scan_mg(
            (str(tmpdir),)
        )


def test_scan_mg_valid(simple_must_gather, omgconfig):
    paths = scan_mg(
        (str(simple_must_gather),)
    )
    assert len(paths) == 1
    for path in paths:
        assert os.path.isdir(path)
        assert (
            os.path.isdir(
                os.path.join(path, "namespaces"))
            or
            os.path.isdir(
                os.path.join(path, "cluster-scoped-resources"))
        )


def test_locate_yamls(simple_must_gather):
    paths = scan_mg(
        (str(simple_must_gather),)
    )
    kind, yamls = locate_yamls(
        paths=paths,
        r_type="infrastructure"
    )
    assert kind == "Infrastructure"
    assert yamls == [
        paths[0] + "/cluster-scoped-resources/config.openshift.io/infrastructures.yaml"
    ]
