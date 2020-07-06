# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import click

from ...e2e import create_interface, get_configured_envs
from ...testing import complete_active_checks, complete_configured_envs
from ..console import CONTEXT_SETTINGS, abort, echo_failure, echo_info, echo_success


@click.command('shell', context_settings=CONTEXT_SETTINGS, short_help='Run a shell inside agent container')
@click.argument('check', autocompletion=complete_active_checks)
@click.argument('env', autocompletion=complete_configured_envs, required=False)
def shell(check, env):
    """Restart an Agent to detect environment changes."""
    envs = get_configured_envs(check)
    if not envs:
        echo_failure(f'No active environments found for `{check}`.')
        echo_info(f'See what is available to start via `ddev env ls {check}`.')
        abort()

    if not env:
        if len(envs) > 1:
            echo_failure(f'Multiple active environments found for `{check}`, please specify one.')
            echo_info('See what is active via `ddev env ls`.')
            abort()

        env = envs[0]

    if env not in envs:
        echo_failure(f'`{env}` is not an active environment.')
        echo_info('See what is active via `ddev env ls`.')
        abort()

    environment = create_interface(check, env)

    if environment.ENV_TYPE == 'local':
        abort('Shell subcommand only available for docker e2e environments')

    result = environment.shell()

    if result.code:
        abort(result.stdout + result.stderr, code=result.code)
