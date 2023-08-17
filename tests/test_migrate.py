import os

import pytest

from migrate import migrate


# this test is meant to run locally during development only
@pytest.mark.skip(reason="requires external maven project to run")
def test_migrate():
    src_path = os.path.expanduser("~/Projects/git/vino9org/vino-java-base/vino-demo-svc")
    if not os.path.exists(src_path):
        pytest.skip(reason="requires external maven project to run")

    migrate(src_path, ".")
