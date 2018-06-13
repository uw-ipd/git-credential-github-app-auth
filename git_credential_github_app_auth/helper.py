import logging
from typing import Callable
from .identity import AppIdentity

import requests

logger = logging.getLogger(__name__)

def app_session_for(app: AppIdentity) -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Authorization":"Bearer %s" % app.jwt(),
        "Accept": "application/vnd.github.machine-man-preview+json"
    })

    return session

def installation_token_for(account: str, app: AppIdentity):
    session = app_session_for(app)
    installations = session.get("https://api.github.com/app/installations")
    installations.raise_for_status()

    ids_by_account = { i["account"]["login"] : i["id"] for i in installations.json() }

    if account not in ids_by_account:
        return None

    token = session.post("https://api.github.com/app/installations/%i/access_tokens" % ids_by_account[account])
    token.raise_for_status()
    return token.json()

def credential_helper(credential_input: str, get_token_for_account: Callable[[str], str] ) -> str:
    """git-credential helper implementation

    Maps 'https://github.com/<account>' into """
    logger.info("credential_input: %s", credential_input)

    cvals = dict(l.strip().split("=", 1) for l in credential_input.split("\n") if l.strip())
    logger.debug("cvals: %s", cvals)

    if not cvals.get("host", None) == "github.com":
        logger.debug("Host does not match github.com")
        return credential_input
    if not cvals.get("protocol", "").startswith("http"):
        logger.debug("Protocol does not match http*")
        return credential_input

    if not cvals.get("path", ""):
        logger.debug("Not path provided.")
        return credential_input

    account = cvals.get("path", "").split("/")[0]
    token = get_token_for_account(account)
    if not token:
        return credential_input

    cvals["username"]="x-access-token"
    cvals["password"]=token

    return "\n".join("=".join(i) for i in cvals.items())
