import os
import yaml
from omg.use import use
from omg.config.logging import setup_logging


setup_logging(loglevel="normal")


def test_use_invalid_paths(caplog):
    use.cmd(
        mg_paths=('/non/exitent/path',)
    )
    assert "No valid must-gather(s) found in ('/non/exitent/path',)" in caplog.text


def test_use_simple_must_gather(caplog, omgconfig, simple_must_gather):
    use.cmd(
        mg_paths=(simple_must_gather,),
        cfile=omgconfig
    )
    with open(omgconfig, "r") as omgcfg:
        cfg = yaml.load(omgcfg.read(), Loader=yaml.SafeLoader)
    for path in cfg["paths"]:
        assert os.path.isdir(path)
        assert (
            os.path.isdir(
                os.path.join(path, "namespaces"))
            or
            os.path.isdir(
                os.path.join(path, "cluster-scoped-resources"))
        )

    assert "quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256*" in caplog.text
    assert "Cluster API URL: ['https://api.ocp46.v.kxr.me:6443']" in caplog.text
    assert "Cluster Platform: ['VSphere']" in caplog.text
    assert "Cluster ID: ['51611b91-5e45-4246-8b64-b3da2ed6ad22']" in caplog.text
    assert "Desired Version: ['4.6.16']" in caplog.text


# TODO: test_use_multidir_must_gather


def test_use_cwd(caplog, omgconfig):
    use.cmd(
        cwd=True,
        cfile=omgconfig
    )
    assert "[CWD Mode] Assuming your working directory as must-gather" in caplog.text
    with open(omgconfig, "r") as omgcfg:
        assert omgcfg.read() == "paths:\n- .\nproject: null\n"
