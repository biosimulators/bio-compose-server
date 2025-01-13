import subprocess
import sys
import importlib
from typing import Mapping, Any

from shared.log_config import setup_logging


logger = setup_logging(__file__)


def format_dynamic_install(simulators: list[str], package_name: str = None) -> str:
    package = f"{package_name or 'biosimulator-processes'}["
    for i, sim in enumerate(simulators):
        if not i == len(simulators) - 1:
            package += sim + ","
        else:
            package += sim + "]"
    return package


def install_pypi_package(job_id: str, pypi_handle: str, verbose: bool = True) -> int:
    """
    Dynamically installs a given pypi package.

    :param pypi_handle: (`str`) name of the package to install. Anything that would be called with `pip install ...` INCLUDING optional extras if needed dep[a,b,...]
    :param verbose: (`bool`) whether to print progress confirmations
    """
    if verbose:
        print(f"Installing {pypi_handle}...")
    # run pip install
    try:
        # subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", pypi_handle])
        # subprocess.check_call(["poetry", "run", "pip", "uninstall", "biosimulator-processes"])
        # subprocess.check_call(["poetry", "run", sys.executable, "-m", "pip", "install", pypi_handle])
        # subprocess.check_call([
        #     "poetry", "add", f"{pypi_handle}@>=0.3.8,<0.4.0"
        # ])
        subprocess.check_call([
            "conda", "run", "-n", job_id, "poetry", "add", f"{pypi_handle}@>=0.3.8,<0.4.0"
        ])

        if verbose:
            print(f"{pypi_handle} installed successfully.")
        return 0
    except subprocess.CalledProcessError as e:
        logger.error(f">> {str(e)}")
        raise e


def install_request_dependencies(job_id: str, simulators: list[str]) -> int:
    handle = format_dynamic_install(simulators=simulators)
    return install_pypi_package(job_id=job_id, pypi_handle=handle, verbose=False)


def create_dynamic_environment(job: Mapping[str, Any]) -> str:
    job_id = job["job_id"]
    simulators = job["simulators"]

    # create dynamic environment
    subprocess.check_call(["conda", "create", "-n", job_id, "python=3.10", "-y"])

    # install poetry and config no env create
    subprocess.check_call(["conda", "run", "-n", job_id, "pip", "install", "poetry"])
    subprocess.check_call(["conda", "run", "-n", job_id, "poetry", "config", "virtualenvs.create", "false"])

    # install project
    subprocess.check_call(["conda", "run", "-n", job_id, "poetry", "install"])

    install_request_dependencies(job_id=job_id, simulators=simulators)







