"""Test cases for the __main__ module."""
import os
import pytest
import dotenv
from click.testing import CliRunner

from np_gh_actions import __main__


dotenv.load_dotenv()

GH_ACCESS_TOKEN = os.environ["GH_ACCESS_TOKEN"]


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_add_actions(runner: CliRunner, tmpdir_factory) -> None:
    project_dir = tmpdir_factory.mktemp("project")
    result = runner.invoke(
        __main__.add_actions,
        [
            f"--project-root={project_dir}",
            f"--access-token={GH_ACCESS_TOKEN}",
        ],
    )
    assert result.exit_code == 0, "Unexpected exit code."
    print(project_dir.listdir())
    assert (project_dir / ".github" / "workflows" / "black.yml").exists()
    assert (project_dir / ".github" / "workflows" / "pypi.yml").exists()
    assert (project_dir / ".github" / "workflows" / "pytest.yml").exists()