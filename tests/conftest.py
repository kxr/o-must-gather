import os
import logging
import pytest
import tarfile
from _pytest.logging import caplog as _caplog
from loguru import logger


_ = _caplog  # to satisfy flake8


@pytest.fixture
def caplog(_caplog):
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), level=25, format="{message}")
    yield _caplog
    logger.remove(handler_id)


@pytest.fixture
def simple_must_gather(tmpdir):
    mg_tar = tarfile.open("samples/must-gather.46i.tgz")
    mg_tar.extractall(tmpdir)
    mg_tar.close()
    return os.path.join(tmpdir)


@pytest.fixture
def omgconfig(tmpdir):
    return os.path.join(str(tmpdir), ".omgconfig")
