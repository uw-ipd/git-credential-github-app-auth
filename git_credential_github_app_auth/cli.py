import logging
import json

import click

from .identity import AppIdentity
from .helper import app_session_for, installation_token_for, credential_helper

logger = logging.getLogger(__name__)

#https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-a-github-app
pass_appidentity = click.make_pass_decorator(AppIdentity, ensure=True)


@click.group()
@click.option(
    '--app_id',
    help=("Integer app id, or path to file containing id. "
          "Resolved from $%s." % AppIdentity.APP_ID_ENV_VAR),
    envvar=AppIdentity.APP_ID_ENV_VAR,
)
@click.option(
    '--private_key',
    help=("App private key, or path to private key file. "
          "Resolved from $%s." % AppIdentity.PRIVATE_KEY_ENV_VAR),
    envvar=AppIdentity.PRIVATE_KEY_ENV_VAR,
)
@click.option(
    '-v',
    '--verbose',
    count=True,
    help="'-v' for logging, '-vv' for debug logging. "
    "Resolved via $GITHUB_APP_AUTH_DEBUG ('1' or '2').",
    envvar="GITHUB_APP_AUTH_DEBUG",
)
@click.pass_context
def cli(ctx, app_id, private_key, verbose):
    if verbose:
        logging.basicConfig(
            level=logging.INFO if verbose == 1 else logging.DEBUG,
            format="%(name)s %(message)s",
        )

    ctx.obj = AppIdentity(app_id=app_id, private_key=private_key)


@cli.add_command
@click.command(help="Resolve app id/key and check app authentication.")
@pass_appidentity
def current(appidentity):
    session = app_session_for(appidentity)
    installations = session.get("https://api.github.com/app")
    installations.raise_for_status()
    print(json.dumps(installations.json(), indent=2))


@cli.add_command
@click.command(help="Generate access token for installation.")
@pass_appidentity
@click.argument('account')
def token(appidentity, account):
    print(json.dumps(installation_token_for(account, appidentity)))


@cli.add_command
@click.command(help="Credential storage helper implementation.")
@pass_appidentity
@click.argument('input', type=click.File('r'), default="-")
@click.argument('output', type=click.File('w'), default="-")
def get(appidentity, input, output):
    # https://git-scm.com/docs/git-credential
    logger.debug("get id: %s input: %s output: %s", appidentity, input, output)

    def token_for_account(account):
        return installation_token_for(account, appidentity)["token"]

    output.write(credential_helper(input.read(), token_for_account))
    output.write("\n")


@cli.command(help="no-op git-credential interface")
def store():
    pass


@cli.command(help="no-op git-credential interface")
def erase():
    pass


if __name__ == "__main__":
    cli()
