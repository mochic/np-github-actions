import pytest
import hashlib


@pytest.fixture(scope="session")
def repo(tmpdir_factory):
    from git import Repo
    from pathlib import Path

    repo = Repo.init(Path(tmpdir_factory.mktemp("repo")))
    black_checksum = hashlib.md5("black".encode("utf-8")).hexdigest()
    return repo, \
        (
            black_checksum,
            1,
            1,
        )


def test_add():
    pass