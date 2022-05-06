import pytest
from omg.config import config
from omg.config.logging import setup_logging


setup_logging(loglevel="normal")


def test_config_load_no_config(caplog):
    with pytest.raises(config.NoMgSelected):
        config._load_config("/non/exitent/file")


def test_config_dump(tmpdir):
    dump_file = tmpdir.join("dump_file.txt")
    config._dump_config(
        {'testkey': 'testvalue'},
        dump_file
    )
    assert dump_file.read() == "testkey: testvalue\n"


def test_config_get_no_config(caplog):
    with pytest.raises(SystemExit):
        config.get("/non/exitent/file")
    assert "You have not selected a must-gather" in caplog.text


def test_config_save_get(tmpdir):
    omg_config = tmpdir.join(".omgconfig")
    config.save(
        paths=["/test/path"],
        project="testproject",
        cfile=omg_config
    )
    cfg = config.get(cfile=omg_config)

    assert cfg["paths"] == ["/test/path"]
    assert cfg["project"] == "testproject"
