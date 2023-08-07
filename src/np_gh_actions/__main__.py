import logging
import click
import pathlib
from rich.console import Console
from github import Auth, Github

console = Console()

logger = logging.getLogger(__name__)

@click.group(name="np-gh-actions")
@click.version_option()
def main():
    """NP GitHub Actions"""""


GH_ACTIONS = [
    "black",
    "pytest",
    "pypi",
]

@main.command()
@click.option("--project-root", type=click.Path(exists=True), prompt="Project root", help="Location of project root to install actions.")
@click.option("--access-token", type=str, prompt="Github access token (classic)", help="Github access token associated with github user with sufficient permissions.")
@click.option("--github-repo", default="mochic/np-github-actions", type=str, prompt="Full github repository name.", help="Github repository to fetch actions from.")
@click.option("--branch-name", default="master", type=str, prompt="Github repository branch name.", help="Github repostory branch to fetch actions from.")
@click.option("--debug", default=False, is_flag=True, prompt="Run in debug mode", help="Show debug logs.")
def add_actions(project_root, access_token, github_repo, branch_name, debug):
    if debug:
        logger.setLevel(logging.DEBUG)

    github_dir = pathlib.Path(project_root) / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    github_workflows_dir = github_dir / "workflows"
    github_workflows_dir.mkdir(parents=True, exist_ok=True)

    logger.debug("Using github access token: %s" % access_token)
    auth = Auth.Token(access_token)
    gh_client = Github(auth=auth)
    repository = gh_client.get_repo(github_repo)
    for action in GH_ACTIONS:
        action_file = pathlib.Path(".github") / "workflows" / f"/{action}.yml"
        action_file = pathlib.Path("Makefile")
        workflow_file = repository.get_contents(action_file.name, ref=branch_name)
        workflow_file_content = workflow_file.decoded_content.decode()
        action_file.write_text(workflow_file_content)
        logger.debug("Wrote gh action file: %s", action_file)

if __name__ == "__main__":
    main()
