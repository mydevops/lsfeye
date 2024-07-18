import multiprocessing
import os
from typing import Any
from typing import Optional

import click
import psutil

from src.lib import const
from src.lib.gunicorn_runner import GunicornApplication


VERSION_INFO = (0, 0, 1)
DEFAULT_CONFIG_PATH = "/etc/src.conf"
LAST_CONFIG_PATH_FILE = "/var/run/lsfeye/last_config_path"
PID_FILE = "/var/run/lsfeye/service.pid"


def run_gunicorn() -> None:
    from src.lib.config import settings

    app = GunicornApplication(
        app=const.MAIN_APP_PATH,
        host=settings.basic.host,
        port=settings.basic.port,
        workers=settings.basic.workers_count,
        loglevel=settings.loguru.level.lower(),
        factory=True,
    )
    app.run()


@click.command()
@click.option("-v", "--version", is_flag=True, help="show version and exit")
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True),
    help="set configuration file (default: /etc/src.conf)",
)
@click.option(
    "-s",
    "--signal",
    type=click.Choice(["reload", "stop"]),
    help="send signal to a src process: stop, reload",
)
@click.option(
    "-t", "--status", is_flag=True, help="show status of the src service"
)
@click.pass_context
def cli(
    ctx: Any, version: str, config: str, signal: str, status: bool
) -> None:
    """manage the src service"""

    config = config or get_last_config_path() or DEFAULT_CONFIG_PATH
    os.environ[const.CONFIG_FILE_PATH_ENVIRONMENT_VARIABLE_NAME] = config

    if version:
        click.echo(
            f'lsfeye version: lsfeye/{".".join([str(v) for v in VERSION_INFO])}'
        )
        return

    if not os.path.exists(config):
        click.echo(f"configuration file {config} does not exist.")
        return

    if status:
        show_service_status(PID_FILE)
    elif signal:
        control_service(signal, config)
    else:
        start_service(PID_FILE, config)


def get_last_config_path() -> Optional[str]:
    """get the last used configuration file path"""
    if os.path.exists(LAST_CONFIG_PATH_FILE):
        with open(LAST_CONFIG_PATH_FILE, "r") as f:
            return f.read().strip()
    return None


def save_last_config_path(config: str) -> None:
    """save the last used configuration file path"""
    os.makedirs(os.path.dirname(LAST_CONFIG_PATH_FILE), exist_ok=True)
    with open(LAST_CONFIG_PATH_FILE, "w") as f:
        f.write(config)


def control_service(action: str, config: str) -> None:
    """control the service: start, stop, and reload"""
    if action == "start":
        if is_service_running(PID_FILE):
            click.echo("service is already runiung")
        start_service(PID_FILE, config)
    elif action == "stop":
        stop_service(PID_FILE)
    elif action == "reload":
        reload_service(PID_FILE, config)


def is_service_running(pid_file: str) -> bool:
    """check if the service is running by checking the existence of PID file."""
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            try:
                pid = int(f.read().strip())
                return psutil.pid_exists(pid)
            except ValueError:
                return False
    return False


def start_service(pid_file: str, config: str) -> None:
    """start the service"""
    click.echo("starting service...")
    click.echo(f"using configuration file: {config}")
    if is_service_running(pid_file):
        click.echo("service is already running")
        return
    try:
        os.makedirs(os.path.dirname(pid_file), exist_ok=True)

        proc = multiprocessing.Process(target=run_gunicorn)
        proc.start()

        with open(pid_file, "w") as f:
            f.write(str(proc.pid))
        save_last_config_path(config)
    except Exception as e:
        click.echo(f"service failed to start: {e}")


def kill_process_tree(pid: int) -> None:
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    parent.kill()


def stop_service(pid_file: str) -> None:
    """stop the service"""
    click.echo("stopping service...")
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            try:
                pid = int(f.read().strip())
                kill_process_tree(pid)
            except ProcessLookupError:
                click.echo(
                    "service not running, but PID file exists. removing PID file"
                )
            except ValueError:
                click.echo("invalid PID file content")
            except PermissionError:
                click.echo("no permission to stop the service")
            except Exception as e:
                click.echo(f"error stopping service: {e}")
        os.remove(pid_file)
    else:
        click.echo("PID file not found, service may not be running")


def reload_service(pid_file: str, config: str) -> None:
    """reload the service"""
    click.echo("reloading service...")
    click.echo(f"using configuration file: {config}")
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            try:
                pid = int(f.read().strip())
                kill_process_tree(pid)
                os.remove(pid_file)
                start_service(pid_file, config)
                save_last_config_path(config)
            except ProcessLookupError:
                click.echo(
                    "service not running, but PID file exists. restarting service"
                )
                os.remove(pid_file)
                start_service(pid_file, config)
            except ValueError:
                click.echo("invalid PID file content. restarting service")
                os.remove(pid_file)
                start_service(pid_file, config)
            except PermissionError:
                click.echo("no permission to reload the service")
            except Exception as e:
                click.echo(f"error reloading service: {e}")
    else:
        click.echo(
            "PID file not found, service may not be running. attempting to start service"
        )
        start_service(pid_file, config)


def show_service_status(pid_file: str) -> None:
    """show status of the service"""
    click.echo("checking service status...")
    if os.path.exists(pid_file):
        with open(pid_file) as f:
            try:
                pid = int(f.read().strip())
                if psutil.pid_exists(pid):
                    click.echo(f"src service is running (PID: {pid})")
                else:
                    click.echo("src service is not running")
            except ValueError:
                click.echo("invalid PID file content")
    else:
        click.echo("src service is not running")


if __name__ == "__main__":
    cli()
